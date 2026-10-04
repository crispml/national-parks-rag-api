# pre-built Docker image containing
# a small Linux operating environment + Python 3.12
# and supporting tools/libraries
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app
# /app/                         ← Docker WORKDIR
# │
# ├── app/                      ← your Python package
# │   ├── main.py
# │   ├── rag.py
# │   ├── retrieval.py
# │   └── vector_store.py
# │
# ├── scripts/
# ├── tests/
# ├── requirements.txt
# └── ...




# Copy dependency list
COPY requirements.txt .
# The `.` means: "Put it in the current Docker working directory."


# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Docker installs those packages "inside the image".
# --no-cache-dir` tells pip not to retain its downloaded package cache after installation, helping keep the image smaller.


# Copy application source code into the container
COPY . .
# COPY
# everything from current project directory
#               ↓
# current Docker working directory
# Your computer
#
# National Parks Project/
# ├── app/
# ├── scripts/
# ├── tests/
# ├── Input CSVs/
# └── ...
#               ↓ COPY . .
# Docker Image
#
# /app/
# ├── app/
# ├── scripts/
# ├── tests/
# ├── Input CSVs/
# └── ...


# Document the port used by FastAPI. Your FastAPI/Uvicorn application normally listens on port `8000`.
EXPOSE 8000
# Implies : "This containerized application expects to serve traffic on port 8000."
# However "EXPOSE" does not itself publish port 8000 to your Windows machine.
# The following command does
# docker run -p 8000:8000 ...
# The `-p` actually maps:
# Your PC                 Docker Container
# -p HOST_PORT:CONTAINER_PORT
# localhost:8000  ──────→  port 8000
# YOUR WINDOWS MACHINE                 DOCKER CONTAINER
#
# localhost:8000   ────────────────→   port 8000
#                                           │
#                                           ▼
#                                        Uvicorn
#                                           │
#                                           ▼
#                                        FastAPI


# Start Uvicorn when the container starts
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]

### `--port ${PORT:-8000}`
# ${PORT:-8000} is Linux shell syntax. Docker itself doesn't interpret that expression in this JSON-form CMD.
# That is why we start Linux shell
# ${PORT:-8000}
# means: Use the environment variable `PORT` if one exists; otherwise use `8000`.

# 0.0.0.0
# means:
# > Listen on all network interfaces inside the container.
# That allows traffic arriving through Docker/Render to reach Uvicorn.

# Docker
#   │
#   │ "Please start the Linux shell"
#   ▼
# sh
#   │
#   │ "Please execute this command"
#   ▼
# uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
#                                                │
#                                       Shell interprets this
#                                                ↓
#                                         Is PORT defined?
#                                          /          \
#                                        YES           NO
#                                         ↓             ↓
#                                   use $PORT         use 8000
# This is designed to work both locally and on hosting environments.
#
