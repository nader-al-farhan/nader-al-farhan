#!/usr/bin/env node
import fs from "node:fs";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { loadConfig } from "./config.js";
import { createServer, SERVER_NAME } from "./server.js";
import { createHttpServer, MCP_PATH, validateHttpConfig } from "./http.js";
import { ProcessManager } from "./services/processes.js";

function fatal(message: string): never {
  console.error(`${SERVER_NAME}: ${message}`);
  process.exit(1);
}

async function main(): Promise<void> {
  const config = loadConfig();

  for (const dir of config.allowedDirectories) {
    if (!fs.existsSync(dir) || !fs.statSync(dir).isDirectory()) {
      fatal(`allowed directory does not exist or is not a directory: ${dir}`);
    }
  }

  const processes = new ProcessManager();
  const summary =
    `dirs: ${config.allowedDirectories.join(", ")} | ` +
    `read-only: ${config.readOnly} | exec: ${config.allowExec && !config.readOnly}`;

  if (config.transport === "http") {
    const problems = validateHttpConfig(config);
    if (problems.length > 0) fatal(`refusing to start:\n- ${problems.join("\n- ")}`);

    const httpServer = createHttpServer(config, processes);
    const shutdown = () => {
      processes.terminateAll();
      httpServer.close(() => process.exit(0));
      setTimeout(() => process.exit(0), 2000).unref();
    };
    process.on("SIGINT", shutdown);
    process.on("SIGTERM", shutdown);

    httpServer.on("error", (err) => fatal(`HTTP server error: ${err.message}`));
    httpServer.listen(config.http.port, config.http.host, () => {
      const host = config.http.host.includes(":") ? `[${config.http.host}]` : config.http.host;
      console.error(`${SERVER_NAME} listening on http://${host}:${config.http.port}${MCP_PATH} | ${summary}`);
    });
    return;
  }

  const { server } = createServer(config, processes);
  const shutdown = () => {
    processes.terminateAll();
    process.exit(0);
  };
  process.on("SIGINT", shutdown);
  process.on("SIGTERM", shutdown);
  process.stdin.on("close", shutdown);

  await server.connect(new StdioServerTransport());
  // stdout carries the protocol; diagnostics go to stderr.
  console.error(`${SERVER_NAME} running on stdio | ${summary}`);
}

main().catch((err) => fatal(`failed to start: ${err instanceof Error ? err.stack : String(err)}`));
