import path from "node:path";
import os from "node:os";

export interface ServerConfig {
  /** Absolute, normalized directories the server may touch. */
  allowedDirectories: string[];
  /** When true, every tool that writes files or runs commands is not registered. */
  readOnly: boolean;
  /** Shell execution is off unless explicitly enabled. */
  allowExec: boolean;
  /** Command names (first token) that are always rejected. */
  blockedCommands: string[];
  /** Default and maximum time a command may run before it is left in the background. */
  defaultCommandTimeoutMs: number;
  /** Largest file the server will read or write, in bytes. */
  maxFileBytes: number;
}

const DEFAULT_BLOCKED = [
  "rm", "rmdir", "del", "format", "mkfs", "dd", "shutdown", "reboot", "halt",
  "poweroff", "sudo", "su", "doas", "chmod", "chown", "passwd", "useradd",
  "userdel", "usermod", "diskpart", "reg", "crontab", "mount", "umount",
];

function parseBool(value: string | undefined, fallback: boolean): boolean {
  if (value === undefined || value === "") return fallback;
  return ["1", "true", "yes", "on"].includes(value.trim().toLowerCase());
}

function parseList(value: string | undefined): string[] {
  if (!value) return [];
  return value.split(/[,\n]/).map((s) => s.trim()).filter(Boolean);
}

function expandHome(p: string): string {
  return p === "~" || p.startsWith("~/") ? path.join(os.homedir(), p.slice(1)) : p;
}

/**
 * Builds the configuration from CLI arguments (allowed directories) and
 * environment variables. CLI directories take precedence over DC_ALLOWED_DIRECTORIES.
 */
export function loadConfig(argv: string[] = process.argv.slice(2), env = process.env): ServerConfig {
  const dirs = argv.length > 0 ? argv : parseList(env.DC_ALLOWED_DIRECTORIES);
  const allowedDirectories = (dirs.length > 0 ? dirs : [process.cwd()])
    .map((d) => path.resolve(expandHome(d)));

  const extraBlocked = parseList(env.DC_BLOCKED_COMMANDS);
  const unblocked = new Set(parseList(env.DC_UNBLOCK_COMMANDS));

  return {
    allowedDirectories: [...new Set(allowedDirectories)],
    readOnly: parseBool(env.DC_READ_ONLY, false),
    allowExec: parseBool(env.DC_ALLOW_EXEC, false),
    blockedCommands: [...new Set([...DEFAULT_BLOCKED, ...extraBlocked])].filter((c) => !unblocked.has(c)),
    defaultCommandTimeoutMs: Number(env.DC_COMMAND_TIMEOUT_MS) || 30_000,
    maxFileBytes: Number(env.DC_MAX_FILE_BYTES) || 5 * 1024 * 1024,
  };
}
