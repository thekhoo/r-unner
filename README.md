# r-unner

A containerised environment that runs **R simulations** orchestrated by a **Python wrapper**. Python prepares input data and invokes R scripts as subprocesses; R reads from a shared inputs path and writes results to a shared outputs path.

## Layout

| Path        | What lives here                                                                 |
| ----------- | ------------------------------------------------------------------------------- |
| `app/`      | The Python **Wrapper** — sets things up and drives execution (entry: `python -m app`) |
| `model/`    | The actual **R code** — simulation scripts invoked as subprocesses              |
| `tests/`    | Python tests for the Wrapper                                                     |
| `docs/adr/` | Architecture decision records (why things are the way they are)                 |

The Python ⇄ R contract: the Wrapper calls `Rscript <script> --inputs <path> --outputs <path> [--key=value ...]`. R scripts read inputs and write outputs; everything else is passed as scalar CLI args.

## How it fits together

- **`app/registry.py`** — `SIMULATIONS`, the list of simulations the Wrapper will run.
- **`app/config.py`** — `SimulationConfig`: a script path, inputs/outputs paths, and scalar params.
- **`app/runner.py`** — `run_simulation()`: builds the `Rscript` command and runs it as a subprocess.
- **`app/__main__.py`** — iterates the registry and runs each simulation.

To add a simulation: drop an R script in `model/`, then register it in `app/registry.py`.

## Running

The project targets Python 3.14 and uses [uv](https://docs.astral.sh/uv/) for Python packages and R (via `Rscript`) for simulations.

```bash
uv sync              # install Python deps
uv run python -m app # run all registered simulations
uv run pytest        # run the test suite
```

For a fully reproducible R + Python toolchain, build the Docker image (see `Dockerfile`); it runs `python -m app` by default. A devcontainer is provided under `.devcontainer/`.

## More information

- **Domain language & project structure** → [`CONTEXT.md`](CONTEXT.md) (definitions of Simulation, Registry, Wrapper, Inputs/Outputs Path, Scalar Parameters — and the terms to avoid)
- **Why R-first Docker base** → [`docs/adr/0001-rocker-as-base-image.md`](docs/adr/0001-rocker-as-base-image.md)
- **Why subprocesses instead of rpy2** → [`docs/adr/0002-subprocess-invocation-over-rpy2.md`](docs/adr/0002-subprocess-invocation-over-rpy2.md)
