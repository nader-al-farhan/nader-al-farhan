import fs from "node:fs/promises";
import { z } from "zod";
import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import type { ServerConfig } from "../config.js";
import { Sandbox } from "../services/sandbox.js";
import { errorResult, fail, ok } from "../services/format.js";
import { findBlocked, ProcessManager, type ProcessSession } from "../services/processes.js";

const sessionSchema = {
  session_id: z.number(),
  pid: z.number().optional(),
  running: z.boolean(),
  exit_code: z.number().nullable(),
  output: z.string(),
};

function status(s: ProcessSession): string {
  if (!s.finished) return "running";
  return s.signal ? `killed by ${s.signal}` : `exited with code ${s.exitCode}`;
}

function report(manager: ProcessManager, s: ProcessSession) {
  const { text, skipped } = manager.readNew(s);
  const note = skipped > 0 ? `[${skipped} earlier characters were dropped from the buffer]\n` : "";
  const hint = s.finished ? "" : `\n\n[Still running as session ${s.id}. Use dc_read_process_output to get more output, dc_send_input to write to it, or dc_terminate_process to stop it.]`;
  const header = `Session ${s.id} (pid ${s.pid ?? "?"}) — ${status(s)}\n$ ${s.command}\n`;
  return ok(`${header}${note}${text || "(no output yet)"}${hint}`, {
    session_id: s.id,
    ...(s.pid !== undefined && { pid: s.pid }),
    running: !s.finished,
    exit_code: s.exitCode,
    output: text,
  });
}

function missing(id: number) {
  return fail(`No session ${id}. It may have finished and been cleaned up; call dc_list_sessions to see current sessions.`);
}

/**
 * Registers shell tools. Only called when DC_ALLOW_EXEC is on and read-only mode is off.
 * The working directory is sandboxed, but a shell command can still reach any path the
 * OS user can, so the block list is a guardrail rather than a security boundary.
 */
export function registerProcessTools(server: McpServer, config: ServerConfig, sandbox: Sandbox, manager: ProcessManager): void {
  server.registerTool(
    "dc_start_process",
    {
      title: "Run Shell Command",
      description:
        "Run a shell command in a directory inside the allowed directories and wait up to `timeout_ms` for it to finish. " +
        "If it is still running after the timeout (servers, watchers, REPLs), it keeps running in the background and you get " +
        "a session_id for dc_read_process_output / dc_send_input / dc_terminate_process. " +
        `Commands starting with a blocked program are rejected (${config.blockedCommands.slice(0, 8).join(", ")}, …).`,
      inputSchema: {
        command: z.string().min(1).max(4000).describe("Shell command, e.g. 'npm test' or 'git status'."),
        cwd: z.string().optional().describe("Working directory; defaults to the first allowed directory."),
        timeout_ms: z
          .number()
          .int()
          .min(100)
          .max(600_000)
          .optional()
          .describe(`How long to wait before returning (default ${config.defaultCommandTimeoutMs} ms).`),
      },
      outputSchema: sessionSchema,
      annotations: { readOnlyHint: false, destructiveHint: true, idempotentHint: false, openWorldHint: true },
    },
    async ({ command, cwd, timeout_ms }) => {
      const blocked = findBlocked(command, config.blockedCommands);
      if (blocked) {
        return fail(`'${blocked}' is on the blocked command list. Use a dc_ file tool instead, or ask the user to run it themselves.`);
      }
      try {
        const dir = await sandbox.resolve(cwd ?? sandbox.roots[0]);
        if (!(await fs.stat(dir)).isDirectory()) return fail(`cwd '${cwd}' is not a directory.`);
        const session = manager.start(command, dir);
        await manager.waitFor(session, timeout_ms ?? config.defaultCommandTimeoutMs);
        return report(manager, session);
      } catch (err) {
        return errorResult(err);
      }
    },
  );

  server.registerTool(
    "dc_read_process_output",
    {
      title: "Read Process Output",
      description:
        "Return output a background session produced since the last read. Optionally wait up to `wait_ms` for the process to finish first.",
      inputSchema: {
        session_id: z.number().int().min(1).describe("Session id from dc_start_process."),
        wait_ms: z.number().int().min(0).max(120_000).default(0).describe("Wait this long for the process to exit before reading."),
      },
      outputSchema: sessionSchema,
      annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: false, openWorldHint: false },
    },
    async ({ session_id, wait_ms }) => {
      const s = manager.get(session_id);
      if (!s) return missing(session_id);
      if (wait_ms > 0) await manager.waitFor(s, wait_ms);
      return report(manager, s);
    },
  );

  server.registerTool(
    "dc_send_input",
    {
      title: "Send Input to Process",
      description:
        "Write text to a running session's standard input (for REPLs or prompts), then wait `wait_ms` and return new output. " +
        "Include a trailing newline to submit a line.",
      inputSchema: {
        session_id: z.number().int().min(1).describe("Session id from dc_start_process."),
        input: z.string().describe("Text to send, e.g. 'print(1+1)\\n'."),
        wait_ms: z.number().int().min(0).max(60_000).default(1000).describe("How long to wait for a response."),
      },
      outputSchema: sessionSchema,
      annotations: { readOnlyHint: false, destructiveHint: true, idempotentHint: false, openWorldHint: true },
    },
    async ({ session_id, input, wait_ms }) => {
      const s = manager.get(session_id);
      if (!s) return missing(session_id);
      try {
        manager.sendInput(s, input);
        await manager.waitFor(s, wait_ms);
        return report(manager, s);
      } catch (err) {
        return errorResult(err);
      }
    },
  );

  server.registerTool(
    "dc_list_sessions",
    {
      title: "List Sessions",
      description: "List command sessions started by this server, with their status. Finished sessions whose output was fully read are removed.",
      inputSchema: {},
      outputSchema: {
        sessions: z.array(
          z.object({ session_id: z.number(), pid: z.number().optional(), command: z.string(), status: z.string(), started_at: z.string() }),
        ),
      },
      annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false },
    },
    async () => {
      manager.prune();
      const sessions = manager.list().map((s) => ({
        session_id: s.id,
        ...(s.pid !== undefined && { pid: s.pid }),
        command: s.command,
        status: status(s),
        started_at: s.startedAt.toISOString(),
      }));
      const text = sessions.length
        ? sessions.map((s) => `#${s.session_id} [${s.status}] ${s.command}`).join("\n")
        : "No sessions.";
      return ok(text, { sessions });
    },
  );

  server.registerTool(
    "dc_terminate_process",
    {
      title: "Terminate Process",
      description: "Stop a session and its child processes. Sends SIGTERM, or SIGKILL when `force` is true.",
      inputSchema: {
        session_id: z.number().int().min(1).describe("Session id to stop."),
        force: z.boolean().default(false).describe("Use SIGKILL instead of SIGTERM."),
      },
      outputSchema: sessionSchema,
      annotations: { readOnlyHint: false, destructiveHint: true, idempotentHint: true, openWorldHint: false },
    },
    async ({ session_id, force }) => {
      const s = manager.get(session_id);
      if (!s) return missing(session_id);
      manager.terminate(s, force);
      await manager.waitFor(s, 3000);
      return report(manager, s);
    },
  );
}
