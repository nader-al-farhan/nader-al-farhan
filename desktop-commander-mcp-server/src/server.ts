import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import type { ServerConfig } from "./config.js";
import { Sandbox } from "./services/sandbox.js";
import { ProcessManager } from "./services/processes.js";
import { registerFilesystemTools } from "./tools/filesystem.js";
import { registerProcessTools } from "./tools/processes.js";

export const SERVER_NAME = "desktop-commander-mcp-server";
export const SERVER_VERSION = "0.1.0";

export function createServer(config: ServerConfig): { server: McpServer; processes: ProcessManager } {
  const server = new McpServer({ name: SERVER_NAME, version: SERVER_VERSION });
  const sandbox = new Sandbox(config.allowedDirectories);
  const processes = new ProcessManager();

  registerFilesystemTools(server, config, sandbox);
  if (config.allowExec && !config.readOnly) registerProcessTools(server, config, sandbox, processes);

  return { server, processes };
}
