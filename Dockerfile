##############################################################
# Multi-stage build (RockyLinux UBI) preserving original design:
# 1. Base stage: OS + runtime Python + dedicated non-root user (uid/gid 1680)
# 2. Builder stage: adds build toolchain & compiles project wheels, exports locked deps
# 3. Final stage: minimal runtime from base + prebuilt venv, runs as secure user
##############################################################

FROM quay.io/rockylinux/rockylinux:9-ubi-init AS base

# Define build metadata arguments before using in LABEL
ARG BUILD_DATE
ARG VCS_REF
ARG PYTHON_VERSION=3.12

LABEL org.opencontainers.image.created="${BUILD_DATE}" \
    org.opencontainers.image.revision="${VCS_REF}" \
    org.opencontainers.image.authors="kevin" \
    org.opencontainers.image.source="https://github.com/whg517/httpbin" \
    org.opencontainers.image.title="httpbin" \
    org.opencontainers.image.description="A simple HTTP Request & Response Service built with FastAPI"

# Base runtime packages + create dedicated application user/group (uid/gid 1680)
RUN groupadd -g 1680 --system kevin; \
    useradd --no-log-init --gid 1680 --uid 1680 --create-home --home-dir /kevin kevin; \
    dnf upgrade -y; \
    dnf install -y \
        cyrus-sasl \
        libffi \
        libpq \
        openssl \
        openssl-libs \
        python${PYTHON_VERSION} \
        python${PYTHON_VERSION}-pip; \
    dnf clean all; \
    rm -rf /var/cache/dnf

FROM base AS builder

ARG PYTHON_VERSION=3.12
# Allow optional custom index mirror (for example, internal corporate PyPI)
ARG PIP_INDEX_URL

# Build toolchain & Python development headers (not kept in final image)
RUN dnf install -y \
        cyrus-sasl-devel \
        gcc \
        gcc-c++ \
        libffi-devel \
        libpq-devel \
        make \
        openssl-devel \
        python${PYTHON_VERSION} \
        python${PYTHON_VERSION}-devel \
        python${PYTHON_VERSION}-pip \
        python${PYTHON_VERSION}-setuptools \
        python${PYTHON_VERSION}-wheel; \
    dnf clean all; \
    rm -rf /var/cache/dnf

# Install uv (build helper) inside builder environment
RUN pip${PYTHON_VERSION} install --no-cache-dir uv

WORKDIR /app

# Copy full source (wheel build needs package code)
COPY . /app/

# Build wheels (PEP 517) + export constraints for reproducible install
RUN <<EOF
    set -eux
    uv build --force-pep517
    # Verify wheels were built
    if ! ls dist/*.whl >/dev/null 2>&1; then
        echo "No wheels found in dist/ after build!" >&2
        exit 1
    fi
    # Export locked constraints (exclude editable, dev, workspace deps)
    uv export --no-editable --no-dev --no-emit-workspace --frozen -o constraints.txt

EOF

# Create isolated virtual environment & install built wheels with locked constraints
RUN set -eux; \
    python${PYTHON_VERSION} -m venv /kevin/app; \
    . /kevin/app/bin/activate; \
    uv pip install --no-cache-dir --constraint constraints.txt dist/*.whl

FROM base AS final

WORKDIR /kevin

# Copy prepared virtual environment from builder (retain ownership)
COPY --from=builder --chown=1680:1680 /kevin/app /kevin/app

USER 1680

ENV PATH="/kevin/app/bin:$PATH" \
    VIRTUAL_ENV="/kevin/app" \
    UVICORN_APP="httpbin.main:app" \
    UVICORN_HOST="0.0.0.0" \
    UVICORN_PORT="8080" \
    UVICORN_WORKERS="4"

# Default entrypoint (can override via UVICORN_* env vars or docker run args)
ENTRYPOINT ["uvicorn"]

# Optional HEALTHCHECK (omitted to keep image minimal)
# HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost:8080/status/200 || exit 1
