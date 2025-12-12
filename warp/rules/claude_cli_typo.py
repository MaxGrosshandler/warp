"""Fix typos in the base 'claude' command."""
from warp.specific.claude import CLAUDE_TYPOS
from warp.specific.sudo import sudo_support


@sudo_support
def match(command):
    """Match typos of the 'claude' command."""
    if not command.script_parts:
        return False

    first_part = command.script_parts[0]
    return (first_part in CLAUDE_TYPOS and
            ('command not found' in command.output.lower() or
             'not found' in command.output.lower() or
             'is not recognized as' in command.output.lower()))


@sudo_support
def get_new_command(command):
    """Replace typo with 'claude'."""
    return command.script.replace(command.script_parts[0], 'claude', 1)


priority = 1000
