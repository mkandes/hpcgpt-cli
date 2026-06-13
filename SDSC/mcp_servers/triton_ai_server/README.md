# Triton AI MCP Server (Python)

A [Model Context Protocol](https://modelcontextprotocol.io/) server written in Python with [FastMCP](https://github.com/jlowin/fastmcp). It forwards tool calls to the Triton AI HTTP API so assistants can answer questions grounded in **Expanse** and **Expanse AI** documentation (retrieval-augmented courses `Expanse-Documentation` and `ExpanseAI-Documentation`).

clients connect to a URL such as `http://127.0.0.1:8001/mcp`.

## Tools

| Tool | Purpose |
|------|---------|
| `query_expanse_documentation` | Query general Expanse / HPC documentation (`Expanse-Documentation`). |
| `query_expanse_ai_documentation` | Query Expanse AI documentation (`ExpanseAI-Documentation`). |

Each tool takes a single string argument: `query`.

## Requirements

- Python 3.10+ (tested with 3.12)
- Network access to your Triton AI API endpoint
- Packages:

```bash
pip install fastmcp requests pydantic rich-argparse
```

## Configuration

1. Copy the example config and edit values:

```bash
cd SDSC/mcp_servers/triton_ai_server
cp config.example config.json
```

2. Set at least `triton_ai_url`, `triton_ai_api_key`, and `triton_ai_model` in `config.json`. Optional fields use defaults from `src/config.py` if omitted (`host`, `port`, `log_file`, `triton_ai_system_prompt`).

| Field | Description |
|--------|-------------|
| `host` | Bind address (default `127.0.0.1`). |
| `port` | Listen port (default `8001`). |
| `log_file` | Append-only log path; parent directory is created if needed. |
| `triton_ai_url` | Full URL of the chat/completions endpoint (organization-specific). |
| `triton_ai_api_key` | API key sent in the JSON body as `api_key`. |
| `triton_ai_model` | Model name for the upstream API. |
| `triton_ai_system_prompt` | System message prepended to every request (has a sensible HPC default if unset in schema). |

Command-line flags exist for the same settings (`--host`, `--port`, `--triton-ai-url`, etc.); see `python server.py --help`. The default config file path is `-c config.json`.

## Run

```bash
python server.py
# or
python server.py -c /path/to/config.json -v
```

On startup the server calls `verify_chat_connection()` (a minimal `retrieval_only` request) so misconfigured URLs or keys fail fast.

- **MCP endpoint:** `http://<host>:<port>/mcp` (FastMCP default Streamable HTTP path is `/mcp` unless overridden by FastMCP settings).

Point your MCP client at that URL with Streamable HTTP transport.

## Behavior notes

- Upstream requests use `temperature` **0.3**, `stream: false`, and `retrieval_only: false` for normal tool calls.
- Responses are normalized from several possible JSON shapes (`message`, OpenAI-style `choices[0].message.content`, or `response`).

## Project layout

```
pychat_server/
├── server.py          # MCP server and tools
├── config.example     # Template for config.json
├── src/
│   ├── config.py      # Pydantic config loading
│   └── logging.py     # File logging and FastMCP log routing
└── logs/              # Typical location for log_file (optional)
```

## Troubleshooting

- **Startup fails after “verify”:** Check `triton_ai_url`, API key, and model name; confirm HTTP 200 and JSON from the Triton AI API.
- **401 / 403 on verify:** Key rejected by the upstream service.
- **404 on verify:** Wrong path in `triton_ai_url`.

## License

Same as the parent repository (see root `LICENSE`).
