"""Tests for the app_parser module."""


from motheme.utils.app_parser import (
    AppBlock,
    find_app_block,
    update_file_content,
)


def test_find_app_block_single_line() -> None:
    """Test finding a single-line app block."""
    content: list[str] = [
        "import marimo",
        "app = marimo.App(width=800)",
        "app.run()",
    ]
    result = find_app_block(content)

    assert result is not None
    assert result.start_line == 1
    assert result.end_line == 1
    assert result.content == "app = marimo.App(width=800)"


def test_find_app_block_multi_line() -> None:
    """Test finding a multi-line app block."""
    content: list[str] = [
        "import marimo",
        "app = marimo.App(",
        "    width=800,",
        "    height=600",
        ")",
        "app.run()",
    ]
    result = find_app_block(content)

    assert result is not None
    assert result.start_line == 1
    assert result.end_line == 4
    assert result.content == "app = marimo.App(width=800,height=600)"


def test_find_app_block_nested_parentheses() -> None:
    """Test finding an app block with nested parentheses."""
    content: list[str] = [
        "app = marimo.App(",
        "    width=get_width(800),",
        "    height=calc_height((600 + 200) * 2)",
        ")",
    ]
    result = find_app_block(content)

    assert result is not None
    assert result.start_line == 0
    assert result.end_line == 3
    content = [line.strip() for line in content]
    assert result.content == "".join(content)


def test_find_app_block_with_complex_args() -> None:
    """Test finding an app block with complex arguments."""
    content: list[str] = [
        "app = marimo.App(",
        "    title=get_title('test'),",
        "    plugins=[plugin1(), plugin2()]",
        "    description='A test app'",
        ")",
    ]
    result = find_app_block(content)

    assert result is not None
    assert result.start_line == 0
    assert result.end_line == 4
    assert "title=get_title('test')" in result.content
    assert "plugins=[plugin1(), plugin2()]" in result.content


def test_find_app_block_no_app() -> None:
    """Test when no app block is present."""
    content: list[str] = [
        "import marimo",
        "x = 42",
        "print('Hello')",
    ]
    result = find_app_block(content)

    assert result is None


def test_find_app_block_empty_file() -> None:
    """Test finding app block in an empty file."""
    content: list[str] = []
    result = find_app_block(content)

    assert result is None


def test_update_file_content_single_line() -> None:
    """Test updating file content when app block is a single line."""
    content: list[str] = [
        "import marimo",
        "app = marimo.App(width=800)",
        "app.run()",
    ]
    app_block = AppBlock(
        start_line=1, end_line=1, content="app = marimo.App(width=800)"
    )
    new_content = "app = marimo.App(width=1024)"

    result = update_file_content(content, app_block, new_content)

    assert len(result) == 3
    assert result[0] == "import marimo"
    assert result[1] == "app = marimo.App(width=1024)"
    assert result[2] == "app.run()"


def test_update_file_content_multi_line() -> None:
    """Test updating file content when app block spans multiple lines."""
    content: list[str] = [
        "import marimo",
        "app = marimo.App(",
        "    width=800,",
        "    height=600",
        ")",
        "app.run()",
    ]
    app_block = AppBlock(
        start_line=1,
        end_line=4,
        content="app = marimo.App(    width=800,    height=600)",
    )
    new_content = "app = marimo.App(width=1024, height=768)"

    result = update_file_content(content, app_block, new_content)

    assert len(result) == 3
    assert result[0] == "import marimo"
    assert result[1] == "app = marimo.App(width=1024, height=768)"
    assert result[2] == "app.run()"


def test_update_file_content_at_start() -> None:
    """Test updating file content when app block is at the start of file."""
    content: list[str] = [
        "app = marimo.App(width=800)",
        "app.run()",
    ]
    app_block = AppBlock(
        start_line=0, end_line=0, content="app = marimo.App(width=800)"
    )
    new_content = "app = marimo.App(width=1024)"

    result = update_file_content(content, app_block, new_content)

    assert len(result) == 2
    assert result[0] == "app = marimo.App(width=1024)"
    assert result[1] == "app.run()"


def test_update_file_content_at_end() -> None:
    """Test updating file content when app block is at the end of file."""
    content: list[str] = [
        "import marimo",
        "app = marimo.App(width=800)",
    ]
    app_block = AppBlock(
        start_line=1, end_line=1, content="app = marimo.App(width=800)"
    )
    new_content = "app = marimo.App(width=1024)"

    result = update_file_content(content, app_block, new_content)

    assert len(result) == 2
    assert result[0] == "import marimo"
    assert result[1] == "app = marimo.App(width=1024)"
