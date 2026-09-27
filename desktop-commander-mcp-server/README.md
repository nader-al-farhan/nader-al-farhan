# desktop-commander-mcp-server

A sandboxed [Model Context Protocol](https://modelcontextprotocol.io) server that lets an AI client (Claude Desktop, Claude Code, …) work with files on your machine and, only if you allow it, run shell commands.

Safe by default:

- **Directory sandbox** – every path is resolved (including symlinks) and must stay inside the directories you allow.
- **No shell unless you opt in** – command tools are not even registered until `DC_ALLOW_EXEC=true`.
- **Read-only mode** – `DC_READ_ONLY=true` removes every tool that writes or runs anything.
- **Limits** – file size cap, paginated listings/reads, truncated responses, command timeouts.

## Tools

| Tool | What it does | Needs |
|---|---|---|
| `dc_list_allowed_directories` | Show allowed directories and active safety settings | – |
| `dc_list_directory` | Tree listing with depth and pagination | – |
| `dc_read_file` | Read a text file by line range | – |
| `dc_get_file_info` | Size, type, timestamps, permissions | – |
| `dc_search_files` | Find files by glob (`*.ts`, `src/**/*.md`) | – |
| `dc_search_content` | Grep file contents with a regex | – |
| `dc_write_file` | Create, overwrite or append | not read-only |
| `dc_edit_block` | Replace an exact block of text (fails if ambiguous) | not read-only |
| `dc_create_directory` | `mkdir -p` | not read-only |
| `dc_move_file` | Move/rename, never overwrites | not read-only |
| `dc_start_process` | Run a shell command; long ones continue in the background | `DC_ALLOW_EXEC` |
| `dc_read_process_output` | New output from a background session | `DC_ALLOW_EXEC` |
| `dc_send_input` | Write to a session's stdin (REPLs, prompts) | `DC_ALLOW_EXEC` |
| `dc_list_sessions` | List sessions and their status | `DC_ALLOW_EXEC` |
| `dc_terminate_process` | Stop a session and its child processes | `DC_ALLOW_EXEC` |

## Install and build

Requires Node.js 20+.

```bash
cd desktop-commander-mcp-server
npm install
npm run build
npm test
```

## Configuration

Allowed directories are passed as command-line arguments (or `DC_ALLOWED_DIRECTORIES`, comma-separated). With neither, the current directory is used.

| Variable | Default | Meaning |
|---|---|---|
| `DC_ALLOWED_DIRECTORIES` | current dir | Comma-separated roots, used when no CLI args are given |
| `DC_READ_ONLY` | `false` | Hide all write and exec tools |
| `DC_ALLOW_EXEC` | `false` | Register the shell tools |
| `DC_BLOCKED_COMMANDS` | – | Extra programs to block (added to the built-in list: `rm`, `sudo`, `dd`, `shutdown`, …) |
| `DC_UNBLOCK_COMMANDS` | – | Programs to remove from the block list |
| `DC_COMMAND_TIMEOUT_MS` | `30000` | How long `dc_start_process` waits before backgrounding |
| `DC_MAX_FILE_BYTES` | `5242880` | Largest file read, edited or written |

### Claude Desktop

`claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "desktop-commander": {
      "command": "node",
      "args": ["/absolute/path/to/desktop-commander-mcp-server/dist/index.js", "/Users/me/projects"],
      "env": { "DC_ALLOW_EXEC": "false" }
    }
  }
}
```

### Claude Code

```bash
claude mcp add desktop-commander -- node /absolute/path/to/dist/index.js ~/projects
```

### Inspect interactively

```bash
npm run inspect
```

## Security notes

- The sandbox applies to the **file tools**. A shell command's working directory is sandboxed, but the command itself can reach anything your OS user can. The block list is a guardrail, not a security boundary; enable `DC_ALLOW_EXEC` only for directories and clients you trust.
- The server speaks stdio only and is meant to run locally. Do not expose it over a network.
