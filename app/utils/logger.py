"""Logging setup for the Wrapper.

Provides a JSON formatter and a single ``configure_logging`` entry point that
wires up two handlers on the root logger:

- a console handler with a human-readable, single-line format, and
- a size-rotating file handler that writes JSON-lines (one object per line).

Logging extra fields
--------------------
Pass an ``extra={...}`` mapping to any logging call; each key becomes a
top-level field in the JSON-lines file output (the console format ignores
them). Use this to attach structured context instead of baking it into the
message string::

    logger.info("Simulation complete", extra={"simulation": "simulate.R", "rows": 1024})
    # file line -> {... "message": "Simulation complete", "simulation": "simulate.R", "rows": 1024}

Keys must avoid reserved ``LogRecord`` attribute names (e.g. ``name``,
``msg``, ``args``, ``levelname``) or the logging call raises ``KeyError``.
"""

import json
import logging
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from pathlib import Path

DEFAULT_LOG_DIR = Path("logs")
DEFAULT_LOG_FILENAME = "runner.log"
DEFAULT_MAX_BYTES = 5 * 1024 * 1024  # 5 MB
DEFAULT_BACKUP_COUNT = 5

CONSOLE_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"

# LogRecord attributes that are part of the record itself rather than caller
# supplied ``extra=`` fields. Anything outside this set is treated as an extra.
_RESERVED_ATTRS = frozenset(
    logging.LogRecord(
        name="", level=0, pathname="", lineno=0, msg="", args=(), exc_info=None
    ).__dict__
) | {"message", "asctime", "taskName"}


class JsonFormatter(logging.Formatter):
    """Render a ``LogRecord`` as a single-line JSON object.

    Always includes ``timestamp`` (ISO 8601, UTC), ``level``, ``logger`` and
    ``message``. Exception/stack info and any caller-supplied ``extra=`` fields
    are merged in when present.
    """

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, object] = {
            "timestamp": datetime.fromtimestamp(
                record.created, tz=timezone.utc
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Surface caller-supplied ``extra={...}`` fields as top-level JSON keys,
        # e.g. logger.info("done", extra={"simulation": "simulate.R"}).
        extras = {
            key: value
            for key, value in record.__dict__.items()
            if key not in _RESERVED_ATTRS
        }
        payload.update(extras)

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        if record.stack_info:
            payload["stack"] = self.formatStack(record.stack_info)

        return json.dumps(payload, default=str)


def configure_logging(
    level: int | str = logging.INFO,
    log_dir: Path = DEFAULT_LOG_DIR,
    *,
    filename: str = DEFAULT_LOG_FILENAME,
    max_bytes: int = DEFAULT_MAX_BYTES,
    backup_count: int = DEFAULT_BACKUP_COUNT,
) -> None:
    """Configure root logging for the Wrapper.

    Logs go to the console (human-readable) and to a size-rotating JSON-lines
    file under ``log_dir`` (created if missing). The file rotates once it
    exceeds ``max_bytes``, keeping ``backup_count`` previous files.

    Safe to call more than once: existing handlers added here are replaced.
    """
    log_dir.mkdir(parents=True, exist_ok=True)

    root = logging.getLogger()
    root.setLevel(level)

    # Drop handlers from a previous call so repeated configuration is idempotent.
    for handler in root.handlers[:]:
        root.removeHandler(handler)
        handler.close()

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(CONSOLE_FORMAT))
    root.addHandler(console_handler)

    file_handler = RotatingFileHandler(
        log_dir / filename,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setFormatter(JsonFormatter())
    root.addHandler(file_handler)
