# Use the official Python 3.13 Alpine image with uv as the base image
FROM ghcr.io/astral-sh/uv:python3.13-alpine

# Building the image
ADD . /app
WORKDIR /app
RUN uv sync --locked

# Running the application
CMD ["uv", "run", "/app/main.py"]
