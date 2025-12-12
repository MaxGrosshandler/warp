"""Tests for claude_api_error rule."""
import pytest
from warp.rules.claude_api_error import match, get_new_command
from warp.types import Command


@pytest.fixture
def model_not_found_error():
    return "anthropic.error.model_not_found_error: Model 'claude-opus' not found"


@pytest.fixture
def unexpected_keyword_error():
    return "TypeError: __init__() got an unexpected keyword argument 'model_name'"


@pytest.fixture
def auth_error():
    return "anthropic.error.authentication_error: Invalid API key"


def test_match(model_not_found_error, unexpected_keyword_error, auth_error):
    """Test matching Claude API errors."""
    assert match(Command('python test.py', model_not_found_error))
    assert match(Command('python -c "import anthropic"', unexpected_keyword_error))
    assert match(Command('curl https://api.anthropic.com/v1/messages', auth_error))
    assert not match(Command('python script.py', 'SyntaxError'))
    assert not match(Command('ls -la', 'No such file'))


def test_get_new_command_model_correction(model_not_found_error):
    """Test model name correction."""
    cmd = Command('python -c "model=\'claude-opus\'"', model_not_found_error)
    result = get_new_command(cmd)
    assert any('claude-opus-4-5-20251101' in r for r in result)


def test_get_new_command_param_correction(unexpected_keyword_error):
    """Test parameter name correction."""
    cmd = Command('python -c "client=Client(model_name=\'test\')"', unexpected_keyword_error)
    result = get_new_command(cmd)
    assert any('model=' in r for r in result)


def test_get_new_command_auth(auth_error):
    """Test authentication error suggestion."""
    cmd = Command('python test.py', auth_error)
    result = get_new_command(cmd)
    assert any('ANTHROPIC_API_KEY' in r for r in result)
