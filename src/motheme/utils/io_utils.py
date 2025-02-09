"""I/O utility functions."""

from collections.abc import Generator
from contextlib import contextmanager, redirect_stdout
from io import StringIO


@contextmanager
def quiet_mode(*, enabled: bool = True) -> Generator[None, None, None]:
    """Enable or disable quiet mode."""
    if enabled:
        null_io = StringIO()
        with redirect_stdout(null_io):
            yield
    else:
        yield
