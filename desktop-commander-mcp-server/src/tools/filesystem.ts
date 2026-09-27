import fs from "node:fs/promises";
import path from "node:path";
import { z } from "zod";
import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import type { ServerConfig } from "../config.js";
import { Sandbox } from "../services/sandbox.js";
import { errorResult, fail, formatBytes, ok } from "../services/format.js";
import { globToRegExp, matchesGlob, walk } from "../services/walk.js";

const READ_ONLY = { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false } as const;

async function assertFileSize(file: string, max: number): Promise<void> {
  const stat = await fs.stat(file);
  if (stat.isDirectory()) throw Object.assign(new Error("is a directory"), { code: "EISDIR", path: file });
  if (stat.size > max) {
    throw new Error(`File is ${formatBytes(stat.size)}, above the ${formatBytes(max)} limit (DC_MAX_FILE_BYTES).`);
  }
}

export function registerFilesystemTools(server: McpServer, config: ServerConfig, sandbox: Sandbox): void {
  server.registerTool(
    "dc_list_allowed_directories",
    {
      title: "List Allowed Directories",
      description:
        "List the directories this server may read and write, plus the active safety settings. " +
        "Call this first: every path you pass to other dc_ tools must be inside one of these directories. " +
        "Relative paths resolve against the first directory.",
      inputSchema: {},
      outputSchema: {
        allowed_directories: z.array(z.string()),
        read_only: z.boolean(),
        exec_enabled: z.boolean(),
      },
      annotations: READ_ONLY,
    },
    async () => {
      const data = {
        allowed_directories: sandbox.roots,
        read_only: config.readOnly,
        exec_enabled: config.allowExec && !config.readOnly,
      };
      const lines = [
        "Allowed directories:",
        ...sandbox.roots.map((r) => `- ${r}`),
        "",
        `Read-only mode: ${data.read_only ? "on" : "off"}`,
        `Command execution: ${data.exec_enabled ? "enabled" : "disabled"}`,
      ];
      return ok(lines.join("\n"), data);
    },
  );

  server.registerTool(
    "dc_list_directory",
    {
      title: "List Directory",
      description:
        "List files and folders under a directory, as a tree, up to `depth` levels deep. " +
        "Folders such as .git and node_modules are listed but not descended into. " +
        "Results are paginated with `limit`/`offset`; use `has_more`/`next_offset` to continue.",
      inputSchema: {
        path: z.string().min(1).describe("Directory to list, e.g. 'src' or '/home/me/project'."),
        depth: z.number().int().min(1).max(10).default(2).describe("How many levels to descend (1 = direct children only)."),
        limit: z.number().int().min(1).max(1000).default(200).describe("Maximum entries to return."),
        offset: z.number().int().min(0).default(0).describe("Entries to skip, for pagination."),
      },
      outputSchema: {
        path: z.string(),
        entries: z.array(z.object({ path: z.string(), type: z.string() })),
        count: z.number(),
        has_more: z.boolean(),
        next_offset: z.number().optional(),
      },
      annotations: READ_ONLY,
    },
    async ({ path: input, depth, limit, offset }) => {
      try {
        const dir = await sandbox.resolve(input);
        const stat = await fs.stat(dir);
        if (!stat.isDirectory()) return fail(`'${input}' is a file, not a directory. Use dc_read_file or dc_get_file_info.`);

        const entries: { path: string; type: string }[] = [];
        let index = 0;
        let hasMore = false;
        for await (const e of walk(dir, depth)) {
          if (index++ < offset) continue;
          if (entries.length >= limit) {
            hasMore = true;
            break;
          }
          entries.push({ path: path.relative(dir, e.path), type: e.type });
        }

        const nextOffset = hasMore ? offset + entries.length : undefined;
        const lines = entries.map((e) => `${e.type === "directory" ? "[DIR] " : e.type === "symlink" ? "[LINK]" : "[FILE]"} ${e.path}`);
        if (entries.length === 0) lines.push("(empty)");
        if (hasMore) lines.push(`\n… more entries available; call again with offset=${nextOffset}.`);
        return ok(`${dir}\n${lines.join("\n")}`, {
          path: dir,
          entries,
          count: entries.length,
          has_more: hasMore,
          ...(nextOffset !== undefined && { next_offset: nextOffset }),
        });
      } catch (err) {
        return errorResult(err);
      }
    },
  );

  server.registerTool(
    "dc_read_file",
    {
      title: "Read File",
      description:
        "Read a UTF-8 text file. Use `offset` (0-based line) and `length` (line count) to page through large files; " +
        "the response reports total_lines so you know whether more remains. Line numbers are not added to the text.",
      inputSchema: {
        path: z.string().min(1).describe("File to read."),
        offset: z.number().int().min(0).default(0).describe("First line to return, 0-based."),
        length: z.number().int().min(1).max(5000).default(1000).describe("Maximum number of lines to return."),
      },
      outputSchema: {
        path: z.string(),
        content: z.string(),
        start_line: z.number(),
        lines_returned: z.number(),
        total_lines: z.number(),
        has_more: z.boolean(),
      },
      annotations: READ_ONLY,
    },
    async ({ path: input, offset, length }) => {
      try {
        const file = await sandbox.resolve(input);
        await assertFileSize(file, config.maxFileBytes);
        const buf = await fs.readFile(file);
        if (buf.subarray(0, 8000).includes(0)) {
          return fail(`'${input}' looks like a binary file; only text files can be read. Use dc_get_file_info for its metadata.`);
        }
        const all = buf.toString("utf8").split(/\r?\n/);
        const slice = all.slice(offset, offset + length);
        const hasMore = offset + slice.length < all.length;
        const footer = hasMore
          ? `\n\n[Showing lines ${offset}-${offset + slice.length - 1} of ${all.length}. Call again with offset=${offset + slice.length} for more.]`
          : "";
        return ok(slice.join("\n") + footer, {
          path: file,
          content: slice.join("\n"),
          start_line: offset,
          lines_returned: slice.length,
          total_lines: all.length,
          has_more: hasMore,
        });
      } catch (err) {
        return errorResult(err);
      }
    },
  );

  server.registerTool(
    "dc_get_file_info",
    {
      title: "Get File Info",
      description: "Return size, type, timestamps and permissions for a file or directory, without reading its contents.",
      inputSchema: { path: z.string().min(1).describe("File or directory to inspect.") },
      outputSchema: {
        path: z.string(),
        type: z.string(),
        size_bytes: z.number(),
        modified: z.string(),
        created: z.string(),
        permissions: z.string(),
      },
      annotations: READ_ONLY,
    },
    async ({ path: input }) => {
      try {
        const target = await sandbox.resolve(input);
        const s = await fs.stat(target);
        const data = {
          path: target,
          type: s.isDirectory() ? "directory" : s.isFile() ? "file" : "other",
          size_bytes: s.size,
          modified: s.mtime.toISOString(),
          created: s.birthtime.toISOString(),
          permissions: (s.mode & 0o777).toString(8),
        };
        const text = [
          `Path: ${data.path}`,
          `Type: ${data.type}`,
          `Size: ${formatBytes(data.size_bytes)} (${data.size_bytes} bytes)`,
          `Modified: ${data.modified}`,
          `Created: ${data.created}`,
          `Permissions: ${data.permissions}`,
        ].join("\n");
        return ok(text, data);
      } catch (err) {
        return errorResult(err);
      }
    },
  );

  server.registerTool(
    "dc_search_files",
    {
      title: "Search Files by Name",
      description:
        "Find files and folders whose name matches a glob pattern, searching recursively. " +
        "A pattern without '/' matches the file name (e.g. '*.ts', 'README*'); " +
        "a pattern with '/' matches the path relative to `path` (e.g. 'src/**/*.test.ts'). Matching is case-insensitive.",
      inputSchema: {
        path: z.string().min(1).describe("Directory to search from."),
        pattern: z.string().min(1).max(500).describe("Glob pattern, e.g. '*.md' or 'docs/**/*.pdf'."),
        max_depth: z.number().int().min(1).max(30).default(10).describe("How deep to search."),
        limit: z.number().int().min(1).max(1000).default(100).describe("Maximum matches to return."),
      },
      outputSchema: { matches: z.array(z.string()), count: z.number(), truncated: z.boolean() },
      annotations: READ_ONLY,
    },
    async ({ path: input, pattern, max_depth, limit }) => {
      try {
        const root = await sandbox.resolve(input);
        const re = globToRegExp(pattern);
        const hasSlash = pattern.includes("/");
        const matches: string[] = [];
        let truncated = false;
        for await (const e of walk(root, max_depth)) {
          if (!matchesGlob(path.relative(root, e.path), re, hasSlash)) continue;
          if (matches.length >= limit) {
            truncated = true;
            break;
          }
          matches.push(path.relative(root, e.path));
        }
        const text = matches.length
          ? matches.join("\n") + (truncated ? `\n\n[Stopped at ${limit} matches; narrow the pattern or raise limit.]` : "")
          : `No files matching '${pattern}' under ${root}.`;
        return ok(text, { matches, count: matches.length, truncated });
      } catch (err) {
        return errorResult(err);
      }
    },
  );

  server.registerTool(
    "dc_search_content",
    {
      title: "Search File Contents",
      description:
        "Search text files for lines matching a regular expression (JavaScript syntax), like grep. " +
        "Optionally restrict to files whose name matches `file_pattern`. Binary files and files above the size limit are skipped.",
      inputSchema: {
        path: z.string().min(1).describe("Directory (or single file) to search."),
        query: z.string().min(1).max(500).describe("Regular expression, e.g. 'TODO|FIXME' or 'function\\s+main'."),
        file_pattern: z.string().optional().describe("Optional glob for file names, e.g. '*.ts'."),
        ignore_case: z.boolean().default(false).describe("Case-insensitive matching."),
        max_depth: z.number().int().min(1).max(30).default(10).describe("How deep to search."),
        limit: z.number().int().min(1).max(500).default(50).describe("Maximum matching lines to return."),
      },
      outputSchema: {
        matches: z.array(z.object({ file: z.string(), line: z.number(), text: z.string() })),
        count: z.number(),
        files_scanned: z.number(),
        truncated: z.boolean(),
      },
      annotations: READ_ONLY,
    },
    async ({ path: input, query, file_pattern, ignore_case, max_depth, limit }) => {
      let regex: RegExp;
      try {
        regex = new RegExp(query, ignore_case ? "i" : "");
      } catch (err) {
        return fail(`Invalid regular expression: ${(err as Error).message}`);
      }
      try {
        const root = await sandbox.resolve(input);
        const rootStat = await fs.stat(root);
        const fileRe = file_pattern ? globToRegExp(file_pattern) : undefined;
        const fileHasSlash = file_pattern?.includes("/") ?? false;

        const candidates: string[] = [];
        if (rootStat.isFile()) {
          candidates.push(root);
        } else {
          for await (const e of walk(root, max_depth)) {
            if (e.type !== "file") continue;
            if (fileRe && !matchesGlob(path.relative(root, e.path), fileRe, fileHasSlash)) continue;
            candidates.push(e.path);
          }
        }

        const base = rootStat.isFile() ? path.dirname(root) : root;
        const matches: { file: string; line: number; text: string }[] = [];
        let scanned = 0;
        let truncated = false;
        outer: for (const file of candidates) {
          let buf: Buffer;
          try {
            const s = await fs.stat(file);
            if (s.size > config.maxFileBytes) continue;
            buf = await fs.readFile(file);
          } catch {
            continue;
          }
          if (buf.subarray(0, 8000).includes(0)) continue;
          scanned++;
          const lines = buf.toString("utf8").split(/\r?\n/);
          for (let i = 0; i < lines.length; i++) {
            if (!regex.test(lines[i])) continue;
            if (matches.length >= limit) {
              truncated = true;
              break outer;
            }
            matches.push({ file: path.relative(base, file), line: i + 1, text: lines[i].slice(0, 300) });
          }
        }

        const text = matches.length
          ? matches.map((m) => `${m.file}:${m.line}: ${m.text}`).join("\n") +
            (truncated ? `\n\n[Stopped at ${limit} matches; narrow the query or file_pattern.]` : "")
          : `No lines matching /${query}/ in ${scanned} file(s).`;
        return ok(text, { matches, count: matches.length, files_scanned: scanned, truncated });
      } catch (err) {
        return errorResult(err);
      }
    },
  );

  if (config.readOnly) return;

  server.registerTool(
    "dc_write_file",
    {
      title: "Write File",
      description:
        "Create a file or replace its contents (mode 'rewrite'), or add to the end of it (mode 'append'). " +
        "Missing parent folders are created. To change part of an existing file, prefer dc_edit_block.",
      inputSchema: {
        path: z.string().min(1).describe("File to write."),
        content: z.string().describe("Text to write, UTF-8."),
        mode: z.enum(["rewrite", "append"]).default("rewrite").describe("'rewrite' replaces the file; 'append' adds to the end."),
      },
      outputSchema: { path: z.string(), bytes_written: z.number(), created: z.boolean() },
      annotations: { readOnlyHint: false, destructiveHint: true, idempotentHint: false, openWorldHint: false },
    },
    async ({ path: input, content, mode }) => {
      try {
        const bytes = Buffer.byteLength(content, "utf8");
        if (bytes > config.maxFileBytes) return fail(`Content is ${formatBytes(bytes)}, above the ${formatBytes(config.maxFileBytes)} limit.`);
        const file = await sandbox.resolve(input);
        const existed = await fs.stat(file).then((s) => {
          if (s.isDirectory()) throw Object.assign(new Error("is a directory"), { code: "EISDIR", path: file });
          return true;
        }, () => false);
        await fs.mkdir(path.dirname(file), { recursive: true });
        if (mode === "append") await fs.appendFile(file, content, "utf8");
        else await fs.writeFile(file, content, "utf8");
        const verb = mode === "append" ? "Appended" : existed ? "Overwrote" : "Created";
        return ok(`${verb} ${file} (${formatBytes(bytes)}).`, { path: file, bytes_written: bytes, created: !existed });
      } catch (err) {
        return errorResult(err);
      }
    },
  );

  server.registerTool(
    "dc_edit_block",
    {
      title: "Edit Block in File",
      description:
        "Replace an exact block of text in a file. `old_text` must match the file exactly, including whitespace. " +
        "By default it must occur exactly once; set `expected_replacements` to replace a known number of occurrences. " +
        "Fails without changing anything if the count differs, so read the file first.",
      inputSchema: {
        path: z.string().min(1).describe("File to edit."),
        old_text: z.string().min(1).describe("Exact text to find."),
        new_text: z.string().describe("Replacement text."),
        expected_replacements: z.number().int().min(1).default(1).describe("How many occurrences must be replaced."),
      },
      outputSchema: { path: z.string(), replacements: z.number() },
      annotations: { readOnlyHint: false, destructiveHint: true, idempotentHint: false, openWorldHint: false },
    },
    async ({ path: input, old_text, new_text, expected_replacements }) => {
      try {
        const file = await sandbox.resolve(input);
        await assertFileSize(file, config.maxFileBytes);
        const original = await fs.readFile(file, "utf8");
        const found = original.split(old_text).length - 1;
        if (found === 0) {
          return fail(`old_text was not found in ${file}. Read the file with dc_read_file and copy the text exactly, including indentation.`);
        }
        if (found !== expected_replacements) {
          return fail(
            `old_text occurs ${found} time(s) in ${file}, but expected_replacements is ${expected_replacements}. ` +
              `Include more surrounding lines to make it unique, or set expected_replacements=${found}.`,
          );
        }
        await fs.writeFile(file, original.split(old_text).join(new_text), "utf8");
        return ok(`Replaced ${found} occurrence(s) in ${file}.`, { path: file, replacements: found });
      } catch (err) {
        return errorResult(err);
      }
    },
  );

  server.registerTool(
    "dc_create_directory",
    {
      title: "Create Directory",
      description: "Create a directory, including any missing parents. Succeeds without change if it already exists.",
      inputSchema: { path: z.string().min(1).describe("Directory to create.") },
      outputSchema: { path: z.string() },
      annotations: { readOnlyHint: false, destructiveHint: false, idempotentHint: true, openWorldHint: false },
    },
    async ({ path: input }) => {
      try {
        const dir = await sandbox.resolve(input);
        await fs.mkdir(dir, { recursive: true });
        return ok(`Directory ready: ${dir}`, { path: dir });
      } catch (err) {
        return errorResult(err);
      }
    },
  );

  server.registerTool(
    "dc_move_file",
    {
      title: "Move or Rename",
      description:
        "Move or rename a file or directory. Both paths must be inside the allowed directories. " +
        "Refuses to overwrite an existing destination.",
      inputSchema: {
        source: z.string().min(1).describe("Current path."),
        destination: z.string().min(1).describe("New path."),
      },
      outputSchema: { source: z.string(), destination: z.string() },
      annotations: { readOnlyHint: false, destructiveHint: false, idempotentHint: false, openWorldHint: false },
    },
    async ({ source, destination }) => {
      try {
        const from = await sandbox.resolve(source);
        const to = await sandbox.resolve(destination);
        await fs.stat(from);
        if (await fs.stat(to).then(() => true, () => false)) {
          return fail(`Destination already exists: ${to}. Choose another name or move the existing item first.`);
        }
        await fs.mkdir(path.dirname(to), { recursive: true });
        await fs.rename(from, to);
        return ok(`Moved ${from} → ${to}`, { source: from, destination: to });
      } catch (err) {
        return errorResult(err);
      }
    },
  );
}
