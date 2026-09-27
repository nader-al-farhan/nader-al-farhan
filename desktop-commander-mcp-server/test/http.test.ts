import { test, before, after } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs/promises";
import http from "node:http";
import os from "node:os";
import path from "node:path";
import type { AddressInfo } from "node:net";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";
import { loadConfig } from "../src/config.js";
import { createHttpServer, validateHttpConfig } from "../src/http.js";
import { ProcessManager } from "../src/services/processes.js";

const TOKEN = "t".repeat(40);
let tmp: string;
let server: http.Server;
let processes: ProcessManager;
let base: string;
let port: number;

function raw(options: http.RequestOptions, body?: string): Promise<{ status: number; body: string }> {
  return new Promise((resolve, reject) => {
    const req = http.request({ host: "127.0.0.1", port, ...options }, (res) => {
      let data = "";
      res.on("data", (c) => (data += c));
      res.on("end", () => resolve({ status: res.statusCode ?? 0, body: data }));
    });
    req.on("error", reject);
    req.end(body);
  });
}

async function connect(token = TOKEN) {
  const client = new Client({ name: "http-test", version: "0.0.0" });
  const transport = new StreamableHTTPClientTransport(new URL(`${base}/mcp`), {
    requestInit: { headers: { Authorization: `Bearer ${token}` } },
  });
  await client.connect(transport);
  return client;
}

before(async () => {
  tmp = await fs.realpath(await fs.mkdtemp(path.join(os.tmpdir(), "dc-http-")));
  await fs.writeFile(path.join(tmp, "hello.txt"), "hello over http\n");
  const config = loadConfig([tmp], { DC_TRANSPORT: "http", DC_AUTH_TOKEN: TOKEN, DC_ALLOW_EXEC: "true" });
  processes = new ProcessManager();
  server = createHttpServer(config, processes);
  await new Promise<void>((r) => server.listen(0, "127.0.0.1", r));
  port = (server.address() as AddressInfo).port;
  base = `http://127.0.0.1:${port}`;
});

after(async () => {
  processes.terminateAll();
  await new Promise((r) => server.close(r));
  await fs.rm(tmp, { recursive: true, force: true });
});

test("config validation refuses unsafe HTTP setups", () => {
  const env = (e: Record<string, string>) => loadConfig([tmp], { DC_TRANSPORT: "http", ...e });
  assert.match(validateHttpConfig(env({})).join(), /DC_AUTH_TOKEN is required/);
  assert.match(validateHttpConfig(env({ DC_AUTH_TOKEN: "short" })).join(), /at least 32/);
  assert.match(validateHttpConfig(env({ DC_AUTH_TOKEN: TOKEN, DC_HTTP_HOST: "0.0.0.0" })).join(), /DC_ALLOWED_HOSTS/);
  assert.deepEqual(validateHttpConfig(env({ DC_AUTH_TOKEN: TOKEN, DC_HTTP_HOST: "0.0.0.0", DC_ALLOWED_HOSTS: "mcp.example.com" })), []);
  assert.deepEqual(validateHttpConfig(env({ DC_AUTH_TOKEN: TOKEN })), []);
});

test("health endpoint needs no token; MCP endpoint does", async () => {
  assert.equal((await raw({ path: "/health" })).status, 200);
  const init = JSON.stringify({ jsonrpc: "2.0", id: 1, method: "tools/list" });
  const headers = { "Content-Type": "application/json", Accept: "application/json, text/event-stream" };
  assert.equal((await raw({ path: "/mcp", method: "POST", headers }, init)).status, 401);
  assert.equal((await raw({ path: "/mcp", method: "POST", headers: { ...headers, Authorization: "Bearer wrong" } }, init)).status, 401);
  await assert.rejects(connect("x".repeat(40)));
});

test("rejects foreign Host and Origin headers and non-POST methods", async () => {
  const auth = { Authorization: `Bearer ${TOKEN}` };
  assert.equal((await raw({ path: "/health", headers: { Host: "evil.example.com" } })).status, 403);
  assert.equal((await raw({ path: "/health", headers: { Origin: "https://evil.example.com" } })).status, 403);
  assert.equal((await raw({ path: "/mcp", method: "GET", headers: auth })).status, 405);
  assert.equal((await raw({ path: "/nope", headers: auth })).status, 404);
});

test("tools work over HTTP and command sessions persist across requests", async () => {
  const client = await connect();
  const names = (await client.listTools()).tools.map((t) => t.name);
  assert.ok(names.includes("dc_read_file") && names.includes("dc_start_process"));

  const read = await client.callTool({ name: "dc_read_file", arguments: { path: "hello.txt" } });
  assert.match((read.structuredContent as any).content, /hello over http/);

  const started = await client.callTool({ name: "dc_start_process", arguments: { command: "cat", timeout_ms: 200 } });
  const id = (started.structuredContent as any).session_id;
  assert.equal((started.structuredContent as any).running, true);

  const second = await connect();
  const echoed = await second.callTool({ name: "dc_send_input", arguments: { session_id: id, input: "remote\n", wait_ms: 300 } });
  assert.match((echoed.structuredContent as any).output, /remote/);
  const stopped = await second.callTool({ name: "dc_terminate_process", arguments: { session_id: id } });
  assert.equal((stopped.structuredContent as any).running, false);

  await client.close();
  await second.close();
});
