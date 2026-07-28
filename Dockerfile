# Public base image with uv preinstalled (no Red Hat registry auth required),
# so this builds in CI and pulls for anyone.
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

# Install dependencies first (cached until the lockfile changes), then the
# project itself.
COPY pyproject.toml uv.lock README.md LICENSE ./
RUN uv sync --locked --no-install-project --no-dev
COPY src/ ./src/
RUN uv sync --locked --no-dev

# Run as an unprivileged user.
RUN useradd --system --create-home --home-dir /home/app app \
    && chown -R app:app /app
USER app

EXPOSE 8000

# Configure the cluster connection with SCALE_API_* environment variables
# (no config file needed); see the README. Example:
#   docker run --rm -p 8000:8000 \
#     -e SCALE_API_HOSTNAME=cluster.example.com \
#     -e SCALE_API_USERNAME=admin -e SCALE_API_PASSWORD=secret \
#     ghcr.io/IBM/ibm-storage-scale-mcp-server
#
# The container serves the HTTP (StreamableHTTP) transport; the optional local
# file-operations tools (--filesystem-paths, which need Node/npx) are not
# included in the image - use them with the local/desktop setup instead.
ENTRYPOINT ["/app/.venv/bin/ibm-storage-scale-mcp-server"]
CMD ["--transport", "http", "--host", "0.0.0.0", "--port", "8000"]
