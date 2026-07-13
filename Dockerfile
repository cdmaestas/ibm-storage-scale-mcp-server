FROM registry.redhat.io/rhel9/python-312

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

USER root

# Install Node.js 22 and nsolid for filesystem operations support
RUN curl -fsSL https://rpm.nodesource.com/setup_22.x | bash - && \
    yum install -y nsolid && \
    yum clean all

COPY pyproject.toml uv.lock README.md ./
COPY src/ ./src/
COPY config/ ./config/

RUN pip install --no-cache-dir uv

RUN uv sync --no-dev

USER 1001
EXPOSE 8000

# Cluster connection settings can be supplied without baking a config file
# into the image, via SCALE_API_* environment variables (see README):
# docker run -e SCALE_API_HOSTNAME=... -e SCALE_API_USERNAME=... \
#   -e SCALE_API_PASSWORD=... scale-mcp-server
# Alternatively mount a config file: -v ./scale_config.ini:/app/config/scale_config.ini
#
# To add filesystem paths, override CMD when running:
# docker run -v /host/path:/container/path scale-mcp-server \
#   --transport http --host 0.0.0.0 --port 8000 --filesystem-paths /container/path
ENTRYPOINT [".venv/bin/scale-mcp-server"]
CMD ["--transport", "http", "--host", "0.0.0.0", "--port", "8000"]
