"""Fix Claude slash command typos."""
import re
from warp.specific.claude import CLAUDE_SLASH_COMMANDS
from warp.utils import get_closest


def match(command):
    """Match slash command errors in Claude."""
    # Check if this is a claude command with slash command error
    if 'claude' not in command.script.lower():
        return False

    return any([
        "unknown slash command" in command.output.lower(),
        "invalid slash command" in command.output.lower(),
        "command not found" in command.output.lower() and '/' in command.script,
    ])


def get_new_command(command):
    """Replace misspelled slash command with closest match."""
    # Extract the slash command from the script
    slash_cmd_match = re.search(r'/(\w+)', command.script)
    if not slash_cmd_match:
        return command.script

    wrong_cmd = '/' + slash_cmd_match.group(1)

    # Find closest match
    closest = get_closest(wrong_cmd, CLAUDE_SLASH_COMMANDS, cutoff=0.6)

    if closest:
        return command.script.replace(wrong_cmd, closest, 1)

    return command.script


priority = 1100
requires_output = True
enabled_by_default = True
