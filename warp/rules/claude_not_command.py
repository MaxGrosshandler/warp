"""Fix incorrect Claude CLI subcommands."""
import re
from warp.utils import get_all_matched_commands, replace_command, for_app


@for_app('claude')
def match(command):
    """Match incorrect Claude subcommands."""
    return (("is not a claude command" in command.output.lower() or
             "unknown command" in command.output.lower() or
             "Error: Unknown command" in command.output) and
            ("Did you mean" in command.output or
             "did you mean" in command.output))


@for_app('claude')
def get_new_command(command):
    """Replace broken subcommand with suggested correct one."""
    # Try to extract the broken command from the output
    broken_cmd_match = re.search(r"['\"']([^'\"']*)['\"'].*is not a.*command",
                                  command.output, re.IGNORECASE)
    if broken_cmd_match:
        broken_cmd = broken_cmd_match.group(1)
    elif len(command.script_parts) > 1:
        # Fallback to second part of script
        broken_cmd = command.script_parts[1]
    else:
        return command.script

    # Get suggestions from output
    matched = get_all_matched_commands(command.output,
                                       ['Did you mean', 'did you mean'])
    return replace_command(command, broken_cmd, matched)


priority = 1000
requires_output = True
