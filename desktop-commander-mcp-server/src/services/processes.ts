import { spawn, type ChildProcess } from "node:child_process";
import path from "node:path";
import { PROCESS_BUFFER_LIMIT } from "../constants.js";

export interface ProcessSession {
  id: number;
  pid: number | undefined;
  command: string;
  cwd: string;
  startedAt: Date;
  child: ChildProcess;
  output: string;
  /** Characters dropped from the front of `output` once it passed the buffer limit. */
  dropped: number;
  /** Absolute offset (including dropped characters) up to which output was already returned. */
  readCursor: number;
  exitCode: number | null;
  signal: NodeJS.Signals | null;
  finished: boolean;
}

/** Splits a shell command into the command names it invokes, for block-list checks. */
export function commandNames(command: string): string[] {
  return command
    .split(/&&|\|\||[;|&\n]|\$\(|`|\(|\)/)
    .map((segment) => segment.trim())
    .filter(Boolean)
    .map((segment) => {
      const tokens = segment.split(/\s+/).filter((t) => !/^[A-Za-z_][A-Za-z0-9_]*=/.test(t));
      const first = tokens[0] ?? "";
      return path.basename(first.replace(/^["']|["']$/g, "")).toLowerCase();
    })
    .filter(Boolean);
}

export function findBlocked(command: string, blocked: string[]): string | undefined {
  const set = new Set(blocked.map((b) => b.toLowerCase()));
  return commandNames(command).find((name) => set.has(name) || set.has(name.replace(/\.exe$/, "")));
}

export class ProcessManager {
  private sessions = new Map<number, ProcessSession>();
  private nextId = 1;

  start(command: string, cwd: string): ProcessSession {
    const isWindows = process.platform === "win32";
    const child = spawn(command, {
      cwd,
      shell: isWindows ? true : "/bin/sh",
      // Own process group so terminate() can stop the whole tree.
      detached: !isWindows,
      stdio: ["pipe", "pipe", "pipe"],
      env: process.env,
    });

    const session: ProcessSession = {
      id: this.nextId++,
      pid: child.pid,
      command,
      cwd,
      startedAt: new Date(),
      child,
      output: "",
      dropped: 0,
      readCursor: 0,
      exitCode: null,
      signal: null,
      finished: false,
    };

    const append = (chunk: Buffer) => {
      session.output += chunk.toString("utf8");
      if (session.output.length > PROCESS_BUFFER_LIMIT) {
        const excess = session.output.length - PROCESS_BUFFER_LIMIT;
        session.output = session.output.slice(excess);
        session.dropped += excess;
      }
    };
    child.stdout?.on("data", append);
    child.stderr?.on("data", append);
    child.on("error", (err) => {
      append(Buffer.from(`\n[spawn error] ${err.message}\n`));
      session.finished = true;
    });
    child.on("close", (code, signal) => {
      session.exitCode = code;
      session.signal = signal;
      session.finished = true;
    });

    this.sessions.set(session.id, session);
    return session;
  }

  /** Resolves when the process exits or `timeoutMs` passes, whichever is first. */
  waitFor(session: ProcessSession, timeoutMs: number): Promise<void> {
    if (session.finished) return Promise.resolve();
    return new Promise((resolve) => {
      const timer = setTimeout(done, timeoutMs);
      session.child.once("close", done);
      session.child.once("error", done);
      function done() {
        clearTimeout(timer);
        resolve();
      }
    });
  }

  /** Returns output produced since the last read and advances the cursor. */
  readNew(session: ProcessSession): { text: string; skipped: number } {
    const start = Math.max(session.readCursor - session.dropped, 0);
    const skipped = Math.max(session.dropped - session.readCursor, 0);
    const text = session.output.slice(start);
    session.readCursor = session.dropped + session.output.length;
    return { text, skipped };
  }

  get(id: number): ProcessSession | undefined {
    return this.sessions.get(id);
  }

  list(): ProcessSession[] {
    return [...this.sessions.values()];
  }

  sendInput(session: ProcessSession, input: string): void {
    if (session.finished || !session.child.stdin?.writable) throw new Error(`Session ${session.id} is no longer accepting input.`);
    session.child.stdin.write(input);
  }

  terminate(session: ProcessSession, force = false): void {
    if (session.finished || session.pid === undefined) return;
    const signal: NodeJS.Signals = force ? "SIGKILL" : "SIGTERM";
    try {
      if (process.platform === "win32") session.child.kill(signal);
      else process.kill(-session.pid, signal);
    } catch {
      session.child.kill(signal);
    }
  }

  /** Drops finished sessions whose output has been fully read. */
  prune(): void {
    for (const [id, s] of this.sessions) {
      if (s.finished && s.readCursor >= s.dropped + s.output.length) this.sessions.delete(id);
    }
  }

  terminateAll(): void {
    for (const s of this.sessions.values()) this.terminate(s, true);
  }
}
