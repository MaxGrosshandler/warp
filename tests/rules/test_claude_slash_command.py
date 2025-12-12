"""Tests for claude_slash_command rule."""
import pytest
from warp.rules.claude_slash_command import match, get_new_command
from warp.types import Command


@pytest.fixture
def slash_command_error():
    return "Error: unknown slash command '/comit'"


@pytest.fixture
def slash_command_error_2():
    return "Error: unknown slash command '/reviw'"


@pytest.fixture
def valid_output():
    return "Executing /commit command..."


def test_match(slash_command_error, slash_command_error_2, valid_output):
    """Test matching slash command errors."""
    assert match(Command('claude code /comit', slash_command_error))
    assert match(Command('claude /reviw', slash_command_error_2))
    assert not match(Command('claude /commit', valid_output))
    assert not match(Command('python script.py', 'error'))


def test_get_new_command(slash_command_error, slash_command_error_2):
    """Test correction generation."""
    result = get_new_command(Command('claude code /comit', slash_command_error))
    assert '/commit' in result

    result = get_new_command(Command('claude /reviw', slash_command_error_2))
    assert '/review' in result

    result = get_new_command(Command('claude /explian', 'unknown slash command'))
    assert '/explain' in result
