import { test, before, after } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { InMemoryTransport } from "@modelcontextprotocol/sdk/inMemory.js";
import { loadConfig } from "../src/config.js";
import { createServer } from "../src/server.js";
import { commandNames, findBlocked } from "../src/services/processes.js";

let tmp: string;
let root: string;
let outside: string;

async function connect(env: Record<string, string> = {}) {
  const config = loadConfig([root], env);
  const { server, processes } = createServer(config);
  const [clientT, serverT] = InMemoryTransport.createLinkedPair();
  const client = new Client({ name: "test", version: "0.0.0" });
  await Promise.all([server.connect(serverT), client.connect(clientT)]);
  return {
    client,
    async call(name: string, args: Record<string, unknown> = {}) {
      const res = await client.callTool({ name, arguments: args });
      const text = (res.content as { type: string; text: string }[]).map((c) => c.text).join("\n");
      return { text, isError: Boolean(res.isError), data: res.structuredContent as any };
    },
    async close() {
      processes.terminateAll();
      await client.close();
    },
  };
}

before(async () => {
  tmp = await fs.realpath(await fs.mkdtemp(path.join(os.tmpdir(), "dc-mcp-")));
  root = path.join(tmp, "root");
  outside = path.join(tmp, "outside");
  await fs.mkdir(path.join(root, "src", "nested"), { recursive: true });
  await fs.mkdir(outside);
  await fs.writeFile(path.join(root, "README.md"), "# Demo\nhello world\n");
  await fs.writeFile(path.join(root, "src", "a.ts"), "export const a = 1; // TODO fix\n");
  await fs.writeFile(path.join(root, "src", "nested", "b.ts"), "export const b = 2;\n");
  await fs.writeFile(path.join(root, "big.txt"), Array.from({ length: 50 }, (_, i) => `line ${i}`).join("\n"));
  await fs.writeFile(path.join(outside, "secret.txt"), "top secret");
  await fs.symlink(outside, path.join(root, "escape-link"));
});

after(async () => {
  await fs.rm(tmp, { recursive: true, force: true });
});

test("command parsing finds every invoked program", () => {
  assert.deepEqual(commandNames("FOO=1 npm test && echo ok | grep o; /bin/rm -x"), ["npm", "echo", "grep", "rm"]);
  assert.equal(findBlocked("ls; sudo reboot", ["sudo"]), "sudo");
  assert.equal(findBlocked("echo $(rm -rf x)", ["rm"]), "rm");
  assert.equal(findBlocked("npm run build", ["rm"]), undefined);
});

test("exec tools are off by default and read-only hides write tools", async () => {
  const def = await connect();
  const names = (await def.client.listTools()).tools.map((t) => t.name);
  assert.ok(names.includes("dc_write_file"));
  assert.ok(!names.includes("dc_start_process"));
  await def.close();

  const ro = await connect({ DC_READ_ONLY: "true", DC_ALLOW_EXEC: "true" });
  const roNames = (await ro.client.listTools()).tools.map((t) => t.name);
  assert.ok(roNames.includes("dc_read_file"));
  assert.ok(!roNames.includes("dc_write_file"));
  assert.ok(!roNames.includes("dc_start_process"));
  await ro.close();
});

test("sandbox rejects traversal, absolute and symlink escapes", async () => {
  const s = await connect();
  for (const p of ["../outside/secret.txt", path.join(outside, "secret.txt"), "escape-link/secret.txt"]) {
    const r = await s.call("dc_read_file", { path: p });
    assert.ok(r.isError, `expected denial for ${p}`);
    assert.match(r.text, /outside the allowed directories/);
  }
  const w = await s.call("dc_write_file", { path: "escape-link/new.txt", content: "x" });
  assert.ok(w.isError);
  await assert.rejects(fs.stat(path.join(outside, "new.txt")));
  await s.close();
});

test("list, read with paging, info and search", async () => {
  const s = await connect();

  const list = await s.call("dc_list_directory", { path: ".", depth: 3 });
  assert.ok(list.data.entries.some((e: any) => e.path === path.join("src", "nested", "b.ts")));

  const page = await s.call("dc_list_directory", { path: ".", depth: 3, limit: 2 });
  assert.equal(page.data.count, 2);
  assert.equal(page.data.has_more, true);
  assert.equal(page.data.next_offset, 2);

  const read = await s.call("dc_read_file", { path: "big.txt", offset: 10, length: 5 });
  assert.equal(read.data.content, "line 10\nline 11\nline 12\nline 13\nline 14");
  assert.equal(read.data.total_lines, 50);
  assert.equal(read.data.has_more, true);

  const info = await s.call("dc_get_file_info", { path: "README.md" });
  assert.equal(info.data.type, "file");

  const files = await s.call("dc_search_files", { path: ".", pattern: "*.ts" });
  assert.deepEqual(files.data.matches.sort(), [path.join("src", "a.ts"), path.join("src", "nested", "b.ts")]);

  const grep = await s.call("dc_search_content", { path: ".", query: "todo", ignore_case: true, file_pattern: "*.ts" });
  assert.equal(grep.data.count, 1);
  assert.equal(grep.data.matches[0].line, 1);

  const missing = await s.call("dc_read_file", { path: "nope.txt" });
  assert.ok(missing.isError);
  assert.match(missing.text, /Not found/);
  await s.close();
});

test("write, edit and move files", async () => {
  const s = await connect();
  const w = await s.call("dc_write_file", { path: "out/new.txt", content: "alpha\nbeta\nalpha\n" });
  assert.equal(w.data.created, true);

  const ambiguous = await s.call("dc_edit_block", { path: "out/new.txt", old_text: "alpha", new_text: "gamma" });
  assert.ok(ambiguous.isError);
  assert.match(ambiguous.text, /occurs 2 time/);

  const edit = await s.call("dc_edit_block", { path: "out/new.txt", old_text: "alpha", new_text: "gamma", expected_replacements: 2 });
  assert.equal(edit.data.replacements, 2);
  assert.equal(await fs.readFile(path.join(root, "out", "new.txt"), "utf8"), "gamma\nbeta\ngamma\n");

  const mv = await s.call("dc_move_file", { source: "out/new.txt", destination: "out/renamed.txt" });
  assert.ok(!mv.isError);
  const clash = await s.call("dc_move_file", { source: "out/renamed.txt", destination: "README.md" });
  assert.ok(clash.isError);
  await s.close();
});

test("process lifecycle: run, block, background, input and terminate", async () => {
  const s = await connect({ DC_ALLOW_EXEC: "true" });

  const quick = await s.call("dc_start_process", { command: "echo hi && pwd" });
  assert.equal(quick.data.running, false);
  assert.equal(quick.data.exit_code, 0);
  assert.match(quick.data.output, new RegExp(`hi\\n${root}`));

  const blocked = await s.call("dc_start_process", { command: "echo ok; rm -rf /" });
  assert.ok(blocked.isError);
  assert.match(blocked.text, /'rm' is on the blocked command list/);

  const badCwd = await s.call("dc_start_process", { command: "ls", cwd: outside });
  assert.ok(badCwd.isError);

  const repl = await s.call("dc_start_process", { command: "cat", timeout_ms: 200 });
  assert.equal(repl.data.running, true);
  const id = repl.data.session_id;
  const echoed = await s.call("dc_send_input", { session_id: id, input: "ping\n", wait_ms: 300 });
  assert.match(echoed.data.output, /ping/);

  const listed = await s.call("dc_list_sessions");
  assert.ok(listed.data.sessions.some((x: any) => x.session_id === id && x.status === "running"));

  const stopped = await s.call("dc_terminate_process", { session_id: id });
  assert.equal(stopped.data.running, false);
  await s.close();
});
