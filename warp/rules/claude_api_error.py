"""Fix common Claude API/SDK errors."""
import re
from warp.specific.claude import MODEL_CORRECTIONS, PARAM_CORRECTIONS, is_claude_api_call


def match(command):
    """Match Claude API/SDK errors."""
    if not is_claude_api_call(command):
        return False

    # Match Python SDK errors
    if 'anthropic' in command.script.lower():
        return any([
            "unexpected keyword argument" in command.output.lower(),
            "required positional argument" in command.output.lower(),
            "model_not_found_error" in command.output.lower(),
            "invalid model" in command.output.lower(),
            "authentication_error" in command.output.lower(),
        ])

    # Match curl API calls
    if 'curl' in command.script.lower() and 'api.anthropic.com' in command.script:
        return any([
            "model_not_found" in command.output.lower(),
            "invalid_request_error" in command.output.lower(),
            "authentication_error" in command.output.lower(),
        ])

    return False


def get_new_command(command):
    """Generate corrected command(s) with fixed API errors."""
    new_commands = []

    # Fix model names
    for wrong_model, correct_model in MODEL_CORRECTIONS.items():
        if wrong_model in command.script:
            new_cmd = command.script.replace(wrong_model, correct_model)
            if new_cmd not in new_commands:
                new_commands.append(new_cmd)

    # Fix parameter names in Python code
    for wrong_param, correct_param in PARAM_CORRECTIONS.items():
        pattern = r'\b' + wrong_param + r'\b'
        if re.search(pattern, command.script):
            new_cmd = re.sub(pattern, correct_param, command.script)
            if new_cmd not in new_commands:
                new_commands.append(new_cmd)

    # Fix authentication issues
    if "authentication_error" in command.output.lower():
        if 'export ANTHROPIC_API_KEY' not in command.script:
            auth_cmd = 'export ANTHROPIC_API_KEY="your-api-key-here" && ' + command.script
            if auth_cmd not in new_commands:
                new_commands.append(auth_cmd)

    return new_commands if new_commands else [command.script]


priority = 1100
requires_output = True
