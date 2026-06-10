# r-unner

A containerised environment that runs R simulations orchestrated by a Python wrapper. Python prepares input data and invokes R scripts as subprocesses; R reads from a shared inputs path and writes results to a shared outputs path.

## Project Structure

- **`app/`** — the Python Wrapper. Sets things up and drives execution: the simulation registry (`registry.py`), simulation configs (`config.py`), subprocess invocation (`runner.py`), and the CLI entry point (`__main__.py`, run via `python -m app`).
- **`model/`** — the R code. The actual simulation scripts (e.g. `simulate.R`) invoked as subprocesses by the Wrapper.
- **`tests/`** — Python tests for the Wrapper.
- **`docs/adr/`** — architecture decision records.

## Language

**Simulation**:
A single R script execution, configured with a script path, scalar parameters, an inputs path, and an outputs path.
_Avoid_: job, run, task

**Simulation Registry**:
The Python-side list of simulation configs the wrapper can select from and execute.
_Avoid_: job list, run queue, pipeline

**Wrapper**:
The Python process responsible for organising input data and invoking simulations as subprocesses.
_Avoid_: orchestrator, controller, runner

**Inputs Path**:
The directory from which an R simulation reads its input data files. Defaults to `data/inputs/`.
_Avoid_: input directory, data directory

**Outputs Path**:
The directory to which an R simulation writes its result files. Defaults to `data/outputs/`.
_Avoid_: output directory, results directory

**Scalar Parameters**:
Non-file arguments (flags, numeric values, strings) passed to an R simulation via CLI arguments alongside the inputs and outputs paths.
_Avoid_: flags, options, args
