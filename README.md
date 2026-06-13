# r-unner

A containerised environment that runs **R simulations** orchestrated by a **Python wrapper**. Python prepares input data and invokes R scripts as subprocesses; R reads from a shared inputs path and writes results to a shared outputs path.

## Layout

| Path        | What lives here                                                                 |
| ----------- | ------------------------------------------------------------------------------- |
| `app/`      | The Python **Wrapper** — sets things up and drives execution (entry: `python -m app`) |
| `example_model/` | An **example R script** used only for tests/demos — the real model lives outside this repo |
| `tests/`    | Python tests for the Wrapper                                                     |
| `docs/adr/` | Architecture decision records (why things are the way they are)                 |

The Python ⇄ R contract: the Wrapper calls `Rscript <script> --inputs <path> --outputs <path> [--key=value ...]`. R scripts read inputs and write outputs; everything else is passed as scalar CLI args.

## How it fits together

- **`app/config.py`** — `SimulationConfig` (a script path, inputs/outputs paths, scalar params) and `load_entrypoint()`, which reads the entrypoint script from the `RUNNER_ENTRYPOINT` environment variable.
- **`app/runner.py`** — `run_simulation()`: builds the `Rscript` command and runs it as a subprocess.
- **`app/__main__.py`** — loads the entrypoint from `RUNNER_ENTRYPOINT` and runs that simulation.

The model is **not** part of this repo. Point `RUNNER_ENTRYPOINT` at the R script to execute:

```bash
RUNNER_ENTRYPOINT=path/to/your/simulate.R uv run python -m app
```

## Running

The project targets Python 3.14 and uses [uv](https://docs.astral.sh/uv/) for Python packages and R (via `Rscript`) for simulations.

```bash
uv sync              # install Python deps
RUNNER_ENTRYPOINT=example_model/simulate.R uv run python -m app  # run the entrypoint simulation
uv run pytest        # run the test suite
```

For a fully reproducible R + Python toolchain, build the Docker image (see `Dockerfile`); it runs `python -m app` by default. A devcontainer is provided under `.devcontainer/`.

## More information

- **Domain language & project structure** → [`CONTEXT.md`](CONTEXT.md) (definitions of Simulation, Registry, Wrapper, Inputs/Outputs Path, Scalar Parameters — and the terms to avoid)
- **Why R-first Docker base** → [`docs/adr/0001-rocker-as-base-image.md`](docs/adr/0001-rocker-as-base-image.md)
- **Why subprocesses instead of rpy2** → [`docs/adr/0002-subprocess-invocation-over-rpy2.md`](docs/adr/0002-subprocess-invocation-over-rpy2.md)
