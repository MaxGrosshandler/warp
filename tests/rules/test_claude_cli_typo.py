"""Tests for claude_cli_typo rule."""
import pytest
from warp.rules.claude_cli_typo import match, get_new_command
from warp.types import Command


@pytest.fixture
def claude_typo_output():
    return "bash: claud: command not found"


@pytest.fixture
def claude_typo_output_windows():
    return "'calude' is not recognized as an internal or external command"


def test_match(claude_typo_output, claude_typo_output_windows):
    """Test matching typos of 'claude' command."""
    assert match(Command('claud --version', claude_typo_output))
    assert match(Command('calude chat "hello"', claude_typo_output_windows))
    assert match(Command('cluade --help', 'bash: cluade: command not found'))
    assert not match(Command('claude --version', ''))
    assert not match(Command('python script.py', 'error'))


def test_get_new_command(claude_typo_output):
    """Test correction generation."""
    assert get_new_command(Command('claud chat', claude_typo_output)) == 'claude chat'
    assert get_new_command(Command('calude --version', claude_typo_output)) == 'claude --version'
    assert get_new_command(Command('cluade config', claude_typo_output)) == 'claude config'
