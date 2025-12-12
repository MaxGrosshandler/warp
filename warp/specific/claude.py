"""Claude-specific utilities for command correction."""
from decorator import decorator
from ..utils import is_app, get_closest


# Claude CLI subcommands (from official docs)
CLAUDE_COMMANDS = [
    'chat', 'ask', 'code', 'config', 'help', 'version',
    'init', 'hooks', 'mcp', 'plugins', 'update'
]

# Claude API model names (current as of 2025)
CLAUDE_MODELS = [
    'claude-opus-4-5-20251101',
    'claude-sonnet-4-5-20250929',
    'claude-haiku-4-5-20251015',
    'claude-3-opus-20240229',
    'claude-3-sonnet-20240229',
    'claude-3-haiku-20240307',
    'claude-2.1',
    'claude-instant-1.2',
]

# Common Claude CLI typos
CLAUDE_TYPOS = [
    'claud', 'calude', 'cluade', 'claudee', 'claue', 'claide'
]

# Model name corrections
MODEL_CORRECTIONS = {
    # Common typos
    'claude-opus': 'claude-opus-4-5-20251101',
    'claude-sonnet': 'claude-sonnet-4-5-20250929',
    'claude-haiku': 'claude-haiku-4-5-20251015',
    # Versioned corrections
    'claude-3-opus': 'claude-3-opus-20240229',
    'claude-3-sonnet': 'claude-3-sonnet-20240229',
    'claude-3-haiku': 'claude-3-haiku-20240307',
    # Old names to new
    'claude-2': 'claude-2.1',
    'claude-instant': 'claude-instant-1.2',
}

# API parameter name corrections
PARAM_CORRECTIONS = {
    'model_name': 'model',
    'system_prompt': 'system',
    'user_message': 'messages',
    'max_tokens_to_sample': 'max_tokens',
    'api_key': 'x-api-key',
}

# Common Claude slash commands
CLAUDE_SLASH_COMMANDS = [
    '/commit', '/pr', '/review', '/test', '/fix', '/explain',
    '/refactor', '/document', '/search', '/edit', '/create',
    '/debug', '/optimize', '/help', '/clear', '/reset'
]


@decorator
def claude_support(fn, command):
    """Decorator for Claude-related rules."""
    if not is_app(command, 'claude'):
        return False
    return fn(command)


def is_claude_api_call(command):
    """Check if command is a Claude API call (curl, python, etc.)."""
    return any([
        'api.anthropic.com' in command.script,
        'anthropic' in command.script.lower() and any(
            lang in command.script_parts[0]
            for lang in ['python', 'python3', 'node', 'curl']
        ),
    ])


def get_claude_model_suggestion(wrong_model):
    """Get the closest Claude model name."""
    return get_closest(wrong_model, CLAUDE_MODELS, cutoff=0.6)
