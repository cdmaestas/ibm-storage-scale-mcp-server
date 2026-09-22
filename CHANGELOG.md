# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-07-28

First packaged release. Exposes the IBM Storage Scale 6.0.1 native REST API —
all 144 documented `/scalemgmt/v3` endpoints — as **152 MCP tools**, and makes
the server installable and runnable with no repository clone.

### Added

- **PyPI packaging** — install and run with `uvx ibm-storage-scale-mcp-server`,
  no clone and no environment to manage. Connection settings come from
  `SCALE_API_*` environment variables, so no config file is required.
- **Claude Desktop Extension** (`.mcpb`) — double-click install with a
  credentials form for hostname / username / password.
- **Container image** on GitHub Container Registry for shared HTTP
  deployments, built on a public base and run as a non-root user.
- **mTLS client-certificate authentication** to the REST API
  (`SCALE_API_CLIENT_CERT` / `SCALE_API_CLIENT_KEY` / `SCALE_API_CA_CERT`).
- **`scale-mcp-server(1)` manpage** documenting all options, environment
  variables, and files.
- **Endpoint-contract + registration + client test suite**, plus CI running
  lint, format, tests (Python 3.12 and 3.13), a `pip-audit` dependency audit,
  extension-manifest validation, and a container build with a live MCP
  `initialize` smoke test.
- Pre-commit / pre-push git hooks, an LRO wait helper (`wait_for_operation`),
  and richer API error reporting (status code + parsed error body).

### Changed

- **Corrected all v3 API modules** against the official 6.0.1 documentation.
  This replaced a large set of endpoints that did not exist in the real API
  (fabricated `login`/`token`/`session`, `/remoteclusters`, manager CRUD,
  `xcp:copy`, incorrect AFM path shapes, and more). Every wrapper is now
  covered by a contract test asserting its exact HTTP method and URL path.
- Rewrote the HTTP client to reuse a pooled `httpx.AsyncClient` and to resolve
  settings once (config file overlaid with `SCALE_API_*` environment
  variables); the config files are now optional.
- The container image moved off the `registry.redhat.io` base (which required
  Red Hat registry authentication) to a public base, and drops the Node-based
  optional file-operations tools.
- Default server log level lowered from `DEBUG` to `INFO`.

### Security

- **SSH host-key verification is enforced by default** — the CLI policy tool no
  longer auto-trusts unknown host keys. Opt back in with
  `[ssh] auto_add_host_keys = true`.
- Resolved known dependency CVEs (`mcp`, `click`, `cryptography`, `anyio`,
  `pip`) via `constraint-dependencies`; `pip-audit` reports no known
  vulnerabilities and runs in CI.
- Credentials can be supplied entirely via environment variables, so no secrets
  need to live on disk.
- Converted a silent configuration-load failure into an explicit error.

> **Note:** These tools include destructive cluster operations and take cluster
> credentials. Prefer an account scoped to a least-privilege RBAC domain over a
> full administrator. The HTTP transport has no authentication of its own —
> only expose it on a trusted network, with TLS and an authenticating proxy in
> front before wider exposure.

### Removed

- Dead `LocalCommandExecutor` adapter (unused; carried a latent `shell=True`
  code path).

### Requirements

- Python 3.12+ (for the PyPI/uvx path, [uv](https://docs.astral.sh/uv/)).
- Network access to an IBM Storage Scale cluster's native REST API (v3, default
  port 46443); the v2 GUI REST API for the health tools; SSH for the CLI policy
  tool.

[1.0.0]: https://github.com/IBM/ibm-storage-scale-mcp-server/releases/tag/v1.0.0
