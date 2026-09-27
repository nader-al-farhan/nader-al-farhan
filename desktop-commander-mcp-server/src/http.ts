import http, { type IncomingMessage, type ServerResponse } from "node:http";
import { createHash, timingSafeEqual } from "node:crypto";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import type { ServerConfig } from "./config.js";
import { ProcessManager } from "./services/processes.js";
import { createServer, SERVER_NAME, SERVER_VERSION } from "./server.js";

export const MCP_PATH = "/mcp";
/** Large enough for a dc_write_file at the default 5 MB file limit plus JSON overhead. */
const MAX_BODY_BYTES = 12 * 1024 * 1024;
export const MIN_TOKEN_LENGTH = 32;

const LOOPBACK_NAMES = new Set(["localhost", "127.0.0.1", "::1", "[::1]"]);

export function isLoopback(host: string): boolean {
  return LOOPBACK_NAMES.has(host.toLowerCase());
}

function sha256(value: string): Buffer {
  return createHash("sha256").update(value).digest();
}

/** Constant-time bearer-token check. */
function tokenMatches(header: string | undefined, expected: Buffer): boolean {
  const match = /^Bearer\s+(.+)$/i.exec(header ?? "");
  return match !== null && timingSafeEqual(sha256(match[1].trim()), expected);
}

function hostnameOf(hostHeader: string): string {
  if (hostHeader.startsWith("[")) return hostHeader.slice(0, hostHeader.indexOf("]") + 1);
  return hostHeader.split(":")[0];
}

function sendJson(res: ServerResponse, status: number, body: unknown, headers: Record<string, string> = {}): void {
  res.writeHead(status, { "Content-Type": "application/json", ...headers });
  res.end(JSON.stringify(body));
}

function rpcError(res: ServerResponse, status: number, message: string, headers: Record<string, string> = {}): void {
  sendJson(res, status, { jsonrpc: "2.0", error: { code: -32000, message }, id: null }, headers);
}

function readBody(req: IncomingMessage): Promise<unknown> {
  return new Promise((resolve, reject) => {
    const chunks: Buffer[] = [];
    let size = 0;
    req.on("data", (chunk: Buffer) => {
      size += chunk.length;
      if (size > MAX_BODY_BYTES) {
        reject(Object.assign(new Error("Request body too large"), { status: 413 }));
        req.destroy();
        return;
      }
      chunks.push(chunk);
    });
    req.on("end", () => {
      try {
        resolve(JSON.parse(Buffer.concat(chunks).toString("utf8")));
      } catch {
        reject(Object.assign(new Error("Request body is not valid JSON"), { status: 400 }));
      }
    });
    req.on("error", reject);
  });
}

/**
 * Validates HTTP settings and refuses unsafe combinations, so a misconfigured
 * server never starts rather than starting open.
 */
export function validateHttpConfig(config: ServerConfig): string[] {
  const { authToken } = config.http;
  const problems: string[] = [];
  if (!authToken) {
    problems.push("DC_AUTH_TOKEN is required for the HTTP transport. Generate one with: openssl rand -hex 32");
  } else if (authToken.length < MIN_TOKEN_LENGTH) {
    problems.push(`DC_AUTH_TOKEN must be at least ${MIN_TOKEN_LENGTH} characters.`);
  }
  if (!Number.isInteger(config.http.port) || config.http.port < 1 || config.http.port > 65535) {
    problems.push(`DC_HTTP_PORT must be between 1 and 65535.`);
  }
  if (!isLoopback(config.http.host) && config.http.allowedHosts.length === 0) {
    problems.push(
      `Binding to ${config.http.host} exposes the server beyond this machine; set DC_ALLOWED_HOSTS ` +
        `to the hostname(s) clients will use (e.g. mcp.example.com) to protect against DNS rebinding.`,
    );
  }
  return problems;
}

/**
 * Streamable HTTP transport in stateless JSON mode: each POST gets a fresh
 * McpServer, while background command sessions are shared across requests.
 */
export function createHttpServer(config: ServerConfig, processes = new ProcessManager()): http.Server {
  const expectedToken = sha256(config.http.authToken ?? "");
  const allowedHosts = new Set(config.http.allowedHosts);
  const allowedOrigins = new Set(config.http.allowedOrigins);

  const hostAllowed = (hostHeader: string | undefined): boolean => {
    if (!hostHeader) return false;
    const host = hostHeader.toLowerCase();
    // Loopback names are always safe: a DNS-rebinding attack arrives with the attacker's hostname.
    return isLoopback(hostnameOf(host)) || allowedHosts.has(host) || allowedHosts.has(hostnameOf(host));
  };

  return http.createServer(async (req, res) => {
    const url = new URL(req.url ?? "/", "http://placeholder");

    if (!hostAllowed(req.headers.host)) {
      return rpcError(res, 403, "Host header not allowed. Add it to DC_ALLOWED_HOSTS.");
    }
    const origin = req.headers.origin;
    if (origin && !allowedOrigins.has(origin)) {
      return rpcError(res, 403, "Origin not allowed. Add it to DC_ALLOWED_ORIGINS.");
    }

    if (url.pathname === "/health" && req.method === "GET") {
      return sendJson(res, 200, { status: "ok", name: SERVER_NAME, version: SERVER_VERSION });
    }
    if (url.pathname !== MCP_PATH) {
      return sendJson(res, 404, { error: `Not found. The MCP endpoint is ${MCP_PATH}.` });
    }

    if (!tokenMatches(req.headers.authorization, expectedToken)) {
      return rpcError(res, 401, "Missing or invalid bearer token.", { "WWW-Authenticate": 'Bearer realm="mcp"' });
    }

    if (req.method !== "POST") {
      // Stateless mode: no server-initiated SSE stream and no sessions to delete.
      return rpcError(res, 405, "Method not allowed. This server is stateless; use POST.", { Allow: "POST" });
    }

    let body: unknown;
    try {
      body = await readBody(req);
    } catch (err) {
      const e = err as Error & { status?: number };
      return rpcError(res, e.status ?? 400, e.message);
    }

    const { server } = createServer(config, processes);
    const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined, enableJsonResponse: true });
    res.on("close", () => {
      void transport.close();
      void server.close();
    });
    try {
      await server.connect(transport);
      await transport.handleRequest(req, res, body);
    } catch (err) {
      console.error(`${SERVER_NAME}: error handling request:`, err);
      if (!res.headersSent) rpcError(res, 500, "Internal server error");
    }
  });
}
