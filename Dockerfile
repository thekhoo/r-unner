FROM rocker/r-ver:4.4.2

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# uv for Python package management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install Python 3.14 into uv's managed store
RUN uv python install 3.14

# renv for R package management; languageserver for IDE support inside devcontainer
RUN R -e "install.packages(c('renv', 'languageserver'), repos='https://cloud.r-project.org')"

WORKDIR /workspace

# Install Python dependencies (layer cached until pyproject.toml changes)
COPY pyproject.toml uv.lock* ./
RUN uv sync

# Restore R packages if a lockfile exists
COPY renv.lock* ./
RUN R -e "if (file.exists('renv.lock')) renv::restore() else message('No renv.lock — skipping restore')"

COPY . .

CMD ["uv", "run", "python", "-m", "app"]
