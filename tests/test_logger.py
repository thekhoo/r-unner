import json
import logging
from logging.handlers import RotatingFileHandler

import pytest

from app.utils.logger import DEFAULT_MAX_BYTES, JsonFormatter, configure_logging


@pytest.fixture(autouse=True)
def reset_root_logger():
    """Snapshot and restore root logger state so tests don't leak handlers."""
    root = logging.getLogger()
    original_handlers = root.handlers[:]
    original_level = root.level
    yield
    for handler in root.handlers[:]:
        root.removeHandler(handler)
        handler.close()
    for handler in original_handlers:
        root.addHandler(handler)
    root.setLevel(original_level)


def _make_record(**kwargs) -> logging.LogRecord:
    defaults = dict(
        name="app.test",
        level=logging.INFO,
        pathname=__file__,
        lineno=42,
        msg="hello %s",
        args=("world",),
        exc_info=None,
    )
    defaults.update(kwargs)
    return logging.LogRecord(
        name=defaults["name"],
        level=defaults["level"],
        pathname=defaults["pathname"],
        lineno=defaults["lineno"],
        msg=defaults["msg"],
        args=defaults["args"],
        exc_info=defaults["exc_info"],
    )


class TestJsonFormatter:
    def test_emits_valid_json_line(self):
        line = JsonFormatter().format(_make_record())
        assert "\n" not in line
        json.loads(line)  # does not raise

    def test_includes_core_fields(self):
        payload = json.loads(JsonFormatter().format(_make_record()))
        assert payload["level"] == "INFO"
        assert payload["logger"] == "app.test"
        assert payload["message"] == "hello world"
        assert "timestamp" in payload

    def test_timestamp_is_iso_utc(self):
        payload = json.loads(JsonFormatter().format(_make_record()))
        # ISO 8601 with timezone offset
        assert payload["timestamp"].endswith("+00:00")

    def test_includes_extra_fields(self):
        record = _make_record()
        record.simulation = "simulate.R"
        payload = json.loads(JsonFormatter().format(record))
        assert payload["simulation"] == "simulate.R"

    def test_serialises_exception(self):
        try:
            raise ValueError("boom")
        except ValueError:
            import sys

            record = _make_record(msg="failed", args=(), exc_info=sys.exc_info())
        payload = json.loads(JsonFormatter().format(record))
        assert "exception" in payload
        assert "ValueError: boom" in payload["exception"]


class TestConfigureLogging:
    def test_creates_log_directory(self, tmp_path):
        log_dir = tmp_path / "nested" / "logs"
        configure_logging(log_dir=log_dir)
        assert log_dir.is_dir()

    def test_defaults_to_logs_directory(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        configure_logging()
        assert (tmp_path / "logs").is_dir()

    def test_attaches_console_and_rotating_file_handlers(self, tmp_path):
        configure_logging(log_dir=tmp_path)
        root = logging.getLogger()
        handler_types = {type(h) for h in root.handlers}
        assert RotatingFileHandler in handler_types
        assert logging.StreamHandler in handler_types

    def test_console_handler_is_not_json(self, tmp_path):
        configure_logging(log_dir=tmp_path)
        root = logging.getLogger()
        stream = next(h for h in root.handlers if type(h) is logging.StreamHandler)
        assert not isinstance(stream.formatter, JsonFormatter)

    def test_file_handler_uses_json_and_5mb_rotation(self, tmp_path):
        configure_logging(log_dir=tmp_path)
        root = logging.getLogger()
        file_handler = next(
            h for h in root.handlers if isinstance(h, RotatingFileHandler)
        )
        assert isinstance(file_handler.formatter, JsonFormatter)
        assert file_handler.maxBytes == DEFAULT_MAX_BYTES
        assert DEFAULT_MAX_BYTES == 5 * 1024 * 1024
        assert file_handler.backupCount == 5

    def test_respects_configured_level(self, tmp_path):
        configure_logging(level=logging.DEBUG, log_dir=tmp_path)
        assert logging.getLogger().level == logging.DEBUG

    def test_accepts_string_level(self, tmp_path):
        configure_logging(level="WARNING", log_dir=tmp_path)
        assert logging.getLogger().level == logging.WARNING

    def test_is_idempotent(self, tmp_path):
        configure_logging(log_dir=tmp_path)
        configure_logging(log_dir=tmp_path)
        root = logging.getLogger()
        assert len(root.handlers) == 2

    def test_writes_json_lines_to_file(self, tmp_path):
        configure_logging(log_dir=tmp_path)
        logging.getLogger("app.test").info("structured %s", "log")
        for handler in logging.getLogger().handlers:
            handler.flush()
        log_file = tmp_path / "runner.log"
        assert log_file.exists()
        lines = log_file.read_text().strip().splitlines()
        payload = json.loads(lines[-1])
        assert payload["message"] == "structured log"
        assert payload["level"] == "INFO"
