# Use rocker/r-ver as the base Docker image

The Dockerfile bases off `rocker/r-ver:4.4.x` (an R-first image maintained by the Rocker Project) and installs Python 3.14 on top, rather than starting from a Python base image and installing R. Rocker gives precise, reproducible R version control; installing R from system packages on a Python base image ties you to whatever R version the OS ships, which lags significantly behind current releases.

## Considered Options

- **rocker/r-ver + install Python** ← chosen
- **python:3.14-slim + install R from apt** — apt's R package is typically 1–2 major versions behind; no straightforward way to pin a specific R release
