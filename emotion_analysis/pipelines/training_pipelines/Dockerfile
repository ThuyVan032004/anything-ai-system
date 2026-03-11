FROM nvidia/cuda:12.8.0-cudnn-runtime-ubuntu24.04

# --- System deps (cached trừ khi thay đổi) ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.12 \
    python3.12-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/* \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.12 1 \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1 \
    && pip install uv --break-system-packages

WORKDIR /workspace

# --- ENV phải có trước uv sync ---
ENV UV_PROJECT_ENVIRONMENT=/usr
ENV CUDA_HOME=/usr/local/cuda
ENV PATH=${CUDA_HOME}/bin:${PATH}
ENV LD_LIBRARY_PATH=${CUDA_HOME}/lib64:${LD_LIBRARY_PATH}

# --- Chỉ copy file khai báo deps trước → Docker cache layer này ---
# --- Layer này chỉ rebuild khi pyproject.toml thay đổi ---
COPY pyproject.toml .
COPY shared/pyproject.toml ./shared/pyproject.toml
COPY shared/README.md ./shared/README.md
COPY emotion_analysis/pyproject.toml ./emotion_analysis/pyproject.toml
COPY emotion_analysis/README.md ./emotion_analysis/README.md

RUN uv sync --no-dev --no-install-project

# --- Copy source code sau → thay đổi code không trigger reinstall deps ---
COPY shared ./shared
COPY emotion_analysis ./emotion_analysis

RUN uv sync --no-dev