import os

# The real model is supplied at runtime via RUNNER_ENTRYPOINT and lives outside
# this repo. For the test suite, point it at the bundled example model so any
# code path that reads the environment directly resolves to a real script.
os.environ.setdefault("RUNNER_ENTRYPOINT", "example_model/simulate.R")
