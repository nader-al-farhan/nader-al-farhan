import fs from "node:fs/promises";
import path from "node:path";
import { IGNORED_DIRECTORIES } from "../constants.js";

export interface WalkEntry {
  path: string;
  name: string;
  type: "file" | "directory" | "symlink" | "other";
  depth: number;
}

/**
 * Breadth-first directory walk. Symlinks are reported but never followed, so
 * the walk cannot leave the sandbox. Stops once `maxEntries` are yielded.
 */
export async function* walk(root: string, maxDepth: number, includeIgnored = false): AsyncGenerator<WalkEntry> {
  const queue: { dir: string; depth: number }[] = [{ dir: root, depth: 1 }];
  while (queue.length > 0) {
    const { dir, depth } = queue.shift()!;
    let entries;
    try {
      entries = await fs.readdir(dir, { withFileTypes: true });
    } catch {
      continue;
    }
    entries.sort((a, b) => a.name.localeCompare(b.name));
    for (const e of entries) {
      const full = path.join(dir, e.name);
      const type = e.isDirectory() ? "directory" : e.isFile() ? "file" : e.isSymbolicLink() ? "symlink" : "other";
      yield { path: full, name: e.name, type, depth };
      if (type === "directory" && depth < maxDepth && (includeIgnored || !IGNORED_DIRECTORIES.has(e.name))) {
        queue.push({ dir: full, depth: depth + 1 });
      }
    }
  }
}

/** Converts a simple glob (`*`, `**`, `?`) into an anchored regular expression. */
export function globToRegExp(glob: string): RegExp {
  let re = "";
  for (let i = 0; i < glob.length; i++) {
    const c = glob[i];
    if (c === "*") {
      if (glob[i + 1] === "*") {
        re += ".*";
        i++;
        if (glob[i + 1] === "/") i++;
      } else {
        re += "[^/]*";
      }
    } else if (c === "?") {
      re += "[^/]";
    } else {
      re += c.replace(/[.+^${}()|[\]\\]/g, "\\$&");
    }
  }
  return new RegExp(`^${re}$`, "i");
}

/** A pattern without `/` matches the basename; otherwise it matches the relative path. */
export function matchesGlob(relPath: string, glob: RegExp, hasSlash: boolean): boolean {
  const target = hasSlash ? relPath.split(path.sep).join("/") : path.basename(relPath);
  return glob.test(target);
}
