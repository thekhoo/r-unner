# Invoke R simulations as subprocesses, not via rpy2

The Wrapper calls R scripts as subprocesses rather than using `rpy2` (an in-process Python–R bridge). Subprocess invocation keeps the two runtimes fully isolated — crashes, memory issues, or package conflicts in R do not affect the Python process — and the interface is explicit: inputs path, outputs path, and scalar CLI arguments. `rpy2` introduces complex in-process state sharing and is notoriously difficult to install reliably inside Docker.
