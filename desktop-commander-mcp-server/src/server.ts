import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import type { ServerConfig } from "./config.js";
import { Sandbox } from "./services/sandbox.js";
import { ProcessManager } from "./services/processes.js";
import { registerFilesystemTools } from "./tools/filesystem.js";
import { registerProcessTools } from "./tools/processes.js";

export const SERVER_NAME = "desktop-commander-mcp-server";
export const SERVER_VERSION = "0.1.0";

/**
 * Builds an McpServer. Pass `processes` to share background command sessions
 * across servers (the stateless HTTP transport builds one server per request).
 */
export function createServer(
  config: ServerConfig,
  processes = new ProcessManager(),
): { server: McpServer; processes: ProcessManager } {
  const server = new McpServer({ name: SERVER_NAME, version: SERVER_VERSION });
  const sandbox = new Sandbox(config.allowedDirectories);

  registerFilesystemTools(server, config, sandbox);
  if (config.allowExec && !config.readOnly) registerProcessTools(server, config, sandbox, processes);

  return { server, processes };
}
