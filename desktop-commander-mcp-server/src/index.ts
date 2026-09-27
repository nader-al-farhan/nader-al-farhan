#!/usr/bin/env node
import fs from "node:fs";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { loadConfig } from "./config.js";
import { createServer, SERVER_NAME } from "./server.js";

async function main(): Promise<void> {
  const config = loadConfig();

  for (const dir of config.allowedDirectories) {
    if (!fs.existsSync(dir) || !fs.statSync(dir).isDirectory()) {
      console.error(`${SERVER_NAME}: allowed directory does not exist or is not a directory: ${dir}`);
      process.exit(1);
    }
  }

  const { server, processes } = createServer(config);
  const shutdown = () => {
    processes.terminateAll();
    process.exit(0);
  };
  process.on("SIGINT", shutdown);
  process.on("SIGTERM", shutdown);
  process.stdin.on("close", shutdown);

  await server.connect(new StdioServerTransport());

  // stdout carries the protocol; diagnostics go to stderr.
  console.error(
    `${SERVER_NAME} running on stdio | dirs: ${config.allowedDirectories.join(", ")} | ` +
      `read-only: ${config.readOnly} | exec: ${config.allowExec && !config.readOnly}`,
  );
}

main().catch((err) => {
  console.error(`${SERVER_NAME} failed to start:`, err);
  process.exit(1);
});
