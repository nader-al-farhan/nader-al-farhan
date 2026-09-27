/** Maximum characters returned in a single tool response before truncation. */
export const CHARACTER_LIMIT = 25_000;
/** Maximum characters of process output kept in memory per session. */
export const PROCESS_BUFFER_LIMIT = 200_000;
/** Directories skipped by recursive listing and search. */
export const IGNORED_DIRECTORIES = new Set([".git", "node_modules", ".venv", "__pycache__", "dist", ".next"]);
