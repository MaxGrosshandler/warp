"""Tests for claude_not_command rule."""
import pytest
from warp.rules.claude_not_command import match, get_new_command
from warp.types import Command


@pytest.fixture
def claude_not_command():
    return """claude: 'chta' is not a claude command.

Did you mean this?
    chat
"""


@pytest.fixture
def claude_not_command_multiple():
    return """claude: 'conf' is not a claude command.

Did you mean one of these?
    config
    code
"""


@pytest.fixture
def claude_valid_output():
    return "Claude Code CLI v1.0.0"


def test_match(claude_not_command, claude_valid_output, claude_not_command_multiple):
    """Test matching Claude subcommand errors."""
    assert match(Command('claude chta', claude_not_command))
    assert match(Command('claude conf', claude_not_command_multiple))
    assert not match(Command('ls chta', claude_not_command))
    assert not match(Command('claude chat', claude_valid_output))


def test_get_new_command(claude_not_command, claude_not_command_multiple):
    """Test correction generation."""
    result = get_new_command(Command('claude chta', claude_not_command))
    assert result == ['claude chat']

    result = get_new_command(Command('claude conf', claude_not_command_multiple))
    assert 'claude config' in result or 'claude code' in result
