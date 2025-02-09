"""Tests for I/O utility functions."""

from motheme.utils.io_utils import quiet_mode


def test_quiet_mode_enabled(capsys) -> None:
    """Test that quiet_mode suppresses output when enabled."""
    with quiet_mode(enabled=True):
        print("This should not be visible")

    captured = capsys.readouterr()
    assert captured.out == ""  # No output should be captured
    assert captured.err == ""  # No error output should be captured


def test_quiet_mode_disabled(capsys) -> None:
    """Test that quiet_mode allows output when disabled."""
    test_message = "This should be visible"
    with quiet_mode(enabled=False):
        print(test_message)

    captured = capsys.readouterr()
    assert captured.out == test_message + "\n"  # Output should be captured with newline
    assert captured.err == ""  # No error output should be captured


def test_quiet_mode_nested() -> None:
    """Test that quiet_mode can be nested with different enabled states."""
    outputs = []

    def capture_print(message) -> None:
        print(message)  # This will be suppressed or shown based on quiet_mode
        outputs.append(message)  # This will always be recorded

    with quiet_mode(enabled=True):
        capture_print("Level 1 - Should not be visible")
        with quiet_mode(enabled=False):
            capture_print("Level 2 - Should be visible")
            with quiet_mode(enabled=True):
                capture_print("Level 3 - Should not be visible")

    # Verify that all messages were processed regardless of quiet_mode
    assert len(outputs) == 3
    assert outputs[0] == "Level 1 - Should not be visible"
    assert outputs[1] == "Level 2 - Should be visible"
    assert outputs[2] == "Level 3 - Should not be visible"
