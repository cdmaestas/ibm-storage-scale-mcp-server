# Claude Desktop Extension (MCPB)

This directory holds the [MCP Bundle](https://github.com/anthropics/mcpb)
manifest for installing the IBM Storage Scale MCP server into **Claude Desktop**
with a double-click, instead of hand-editing `claude_desktop_config.json`.

On install, Claude Desktop shows a form for the cluster **hostname**,
**username**, and **password**; those are passed to the server as
`SCALE_API_*` environment variables. The server itself is fetched and run on
demand with `uvx`, so the bundle is tiny (just this manifest).

## Prerequisite

[uv](https://docs.astral.sh/uv/) must be installed on the machine running
Claude Desktop (`uvx` comes with it). Advanced options such as mTLS
(`SCALE_API_CLIENT_CERT`) or disabling TLS verification are not exposed in the
install form; use the environment-variable or config-file setup in the main
[README](../README.md) for those.

## Install

Download `ibm-storage-scale-mcp-server-<version>.mcpb` from the project's
[GitHub Releases](https://github.com/IBM/ibm-storage-scale-mcp-server/releases)
and open it with Claude Desktop (Settings → Extensions), or drag it onto the
Extensions window.

## Build locally

```bash
npx @anthropic-ai/mcpb validate manifest.json
npx @anthropic-ai/mcpb pack . ibm-storage-scale-mcp-server.mcpb
```

CI validates this manifest and checks its version against `pyproject.toml` on
every change; the release workflow packs the `.mcpb` and attaches it to each
GitHub Release.
