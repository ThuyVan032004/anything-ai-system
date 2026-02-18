# FROM python:3.12-slim

# RUN pip install uv

# # Set working directory to root workspace
# WORKDIR /workspace

# # Copy monorepo structure
# COPY shared ./shared
# COPY emotion_analysis ./emotion_analysis

# # Install shared package and dependencies
# RUN uv pip install --system -e ./shared

# RUN uv pip install --system -e ./emotion_analysis

# # Install emotion_analysis dependencies
# RUN uv pip install --system -r ./emotion_analysis/pipelines/data_pipelines/requirements.txt

# # Set working directory for running scripts
# WORKDIR /workspace/emotion_analysis/data

FROM python:3.12-slim

RUN pip install uv

WORKDIR /workspace

COPY shared ./shared
COPY emotion_analysis ./emotion_analysis
COPY pyproject.toml .          

ENV UV_PROJECT_ENVIRONMENT=/usr/local
RUN uv sync --no-dev