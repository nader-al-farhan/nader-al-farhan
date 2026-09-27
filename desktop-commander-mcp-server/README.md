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
| `DC_TRANSPORT` | `stdio` | `http` to serve remotely (see below) |
| `DC_HTTP_HOST` | `127.0.0.1` | Interface to bind |
| `DC_HTTP_PORT` | `3000` | Port to listen on |
| `DC_AUTH_TOKEN` | – | Bearer token, 32+ characters; **required** for HTTP |
| `DC_ALLOWED_HOSTS` | – | Public hostnames clients use; **required** when binding beyond loopback |
| `DC_ALLOWED_ORIGINS` | – | Browser origins allowed to call the server |

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

## Remote use (Streamable HTTP)

Set `DC_TRANSPORT=http` to serve MCP at `POST /mcp` (stateless, JSON responses) with an unauthenticated `GET /health`. Background command sessions are kept in memory and shared across requests.

The server refuses to start in HTTP mode without a token of at least 32 characters, and refuses to bind a non-loopback address unless `DC_ALLOWED_HOSTS` is set. Requests with an unknown `Host` or `Origin` header get `403`; requests without the right token get `401`.

```bash
export DC_AUTH_TOKEN="$(openssl rand -hex 32)"   # keep it in a secret manager, not in git
DC_TRANSPORT=http node dist/index.js ~/projects   # http://127.0.0.1:3000/mcp
```

The server speaks plain HTTP. For access from another machine, keep it on `127.0.0.1` and put a TLS layer in front of it, for example:

- **Tailscale** (private network): `tailscale serve --bg 3000`, then add your tailnet hostname to `DC_ALLOWED_HOSTS`.
- **Cloudflare Tunnel** or a reverse proxy (Caddy, nginx) that terminates HTTPS and forwards to `127.0.0.1:3000`, with `DC_ALLOWED_HOSTS=mcp.example.com`.

Connect Claude Code:

```bash
claude mcp add --transport http desktop-commander https://mcp.example.com/mcp \
  --header "Authorization: Bearer $DC_AUTH_TOKEN"
```

### Docker

```bash
docker build -t desktop-commander-mcp .
docker run -d -p 127.0.0.1:3000:3000 \
  -e DC_AUTH_TOKEN -e DC_ALLOWED_HOSTS=mcp.example.com \
  -v "$HOME/projects:/workspace" desktop-commander-mcp
```

The container runs as the unprivileged `node` user and only sees the mounted `/workspace`, which also limits what shell commands can reach.

## Security notes

- The sandbox applies to the **file tools**. A shell command's working directory is sandboxed, but the command itself can reach anything the OS user can. The block list is a guardrail, not a security boundary; enable `DC_ALLOW_EXEC` only for directories and clients you trust, and prefer running remote instances in a container.
- Anyone holding the token has the same access as the server. Rotate it if it leaks, and never expose the HTTP port directly to the internet without TLS.
