import { CHARACTER_LIMIT } from "../constants.js";
import { SandboxError } from "./sandbox.js";

export type ToolResult = {
  content: { type: "text"; text: string }[];
  structuredContent?: Record<string, unknown>;
  isError?: boolean;
};

export function truncate(text: string, limit = CHARACTER_LIMIT): { text: string; truncated: boolean } {
  if (text.length <= limit) return { text, truncated: false };
  return {
    text: text.slice(0, limit) + `\n\n[Truncated: ${text.length - limit} more characters. Narrow the request with offset/length, a smaller depth, or a tighter pattern.]`,
    truncated: true,
  };
}

export function ok(text: string, structured?: Record<string, unknown>): ToolResult {
  const result: ToolResult = { content: [{ type: "text", text: truncate(text).text }] };
  if (structured) result.structuredContent = structured;
  return result;
}

export function fail(message: string): ToolResult {
  return { content: [{ type: "text", text: `Error: ${message}` }], isError: true };
}

/** Converts thrown errors into actionable tool errors instead of protocol errors. */
export function errorResult(err: unknown): ToolResult {
  if (err instanceof SandboxError) return fail(err.message);
  const e = err as NodeJS.ErrnoException;
  switch (e?.code) {
    case "ENOENT":
      return fail(`Not found: ${e.path ?? "path"}. Check the spelling or list the parent directory first.`);
    case "EACCES":
    case "EPERM":
      return fail(`Permission denied by the operating system: ${e.path ?? "path"}.`);
    case "EISDIR":
      return fail(`Expected a file but found a directory: ${e.path ?? "path"}. Use dc_list_directory instead.`);
    case "ENOTDIR":
      return fail(`Expected a directory but found a file: ${e.path ?? "path"}.`);
    case "EEXIST":
      return fail(`Already exists: ${e.path ?? "path"}.`);
    default:
      return fail(e?.message ?? String(err));
  }
}

export function formatBytes(n: number): string {
  const units = ["B", "KB", "MB", "GB"];
  let i = 0;
  let v = n;
  while (v >= 1024 && i < units.length - 1) {
    v /= 1024;
    i++;
  }
  return `${i === 0 ? v : v.toFixed(1)} ${units[i]}`;
}
