FROM python:3.12-slim

RUN pip install uv --no-cache-dir

WORKDIR /workspace

ENV UV_PROJECT_ENVIRONMENT=/usr/local

# Copy chỉ file khai báo deps trước → cache layer này
COPY pyproject.toml .
COPY shared/pyproject.toml ./shared/pyproject.toml
COPY shared/README.md ./shared/README.md
COPY emotion_analysis/pyproject.toml ./emotion_analysis/pyproject.toml
COPY emotion_analysis/README.md ./emotion_analysis/README.md

RUN uv sync --no-dev --no-install-project

# Copy source code sau → sửa code không trigger reinstall deps
COPY shared ./shared
COPY emotion_analysis ./emotion_analysis

RUN uv sync --no-dev