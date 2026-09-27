import fs from "node:fs/promises";
import path from "node:path";
import os from "node:os";

export class SandboxError extends Error {}

function isWithin(child: string, parent: string): boolean {
  const rel = path.relative(parent, child);
  return rel === "" || (!rel.startsWith("..") && !path.isAbsolute(rel));
}

/**
 * Resolves every path against a fixed set of allowed roots. Symlinks are
 * resolved before the check so a link inside a root cannot point outside it.
 */
export class Sandbox {
  private realRoots: string[] | undefined;

  constructor(public readonly roots: string[]) {
    if (roots.length === 0) throw new SandboxError("At least one allowed directory is required.");
  }

  private async getRealRoots(): Promise<string[]> {
    if (!this.realRoots) {
      this.realRoots = await Promise.all(
        this.roots.map(async (r) => {
          try {
            return await fs.realpath(r);
          } catch {
            return r;
          }
        }),
      );
    }
    return this.realRoots;
  }

  /** Relative paths resolve against the first allowed directory. */
  private absolute(input: string): string {
    const expanded = input === "~" || input.startsWith("~/") ? path.join(os.homedir(), input.slice(1)) : input;
    return path.resolve(this.roots[0], expanded);
  }

  /**
   * Returns the real absolute path for `input` after verifying it lies within an
   * allowed directory. For paths that do not exist yet (new files), the nearest
   * existing ancestor is resolved and checked instead.
   */
  async resolve(input: string): Promise<string> {
    const abs = this.absolute(input);
    const realRoots = await this.getRealRoots();

    let existing = abs;
    const missing: string[] = [];
    for (;;) {
      try {
        const real = await fs.realpath(existing);
        const full = path.join(real, ...missing.reverse());
        if (!realRoots.some((root) => isWithin(full, root))) {
          throw new SandboxError(
            `Access denied: '${input}' is outside the allowed directories (${this.roots.join(", ")}). ` +
              `Call dc_list_allowed_directories to see where you can work.`,
          );
        }
        return full;
      } catch (err) {
        if (err instanceof SandboxError) throw err;
        const code = (err as NodeJS.ErrnoException).code;
        if (code !== "ENOENT" && code !== "ENOTDIR") throw err;
        const parent = path.dirname(existing);
        if (parent === existing) throw new SandboxError(`Cannot resolve path '${input}'.`);
        missing.push(path.basename(existing));
        existing = parent;
      }
    }
  }
}
