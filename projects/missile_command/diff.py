#!/usr/bin/python3.9

import difflib

def print_diff(string_a, string_b):
    """
    Print or return a colour-coded diff of two items in a list of strings.
    Default: Compare first and last strings; print the output; return None.
    """
    green = '\x1b[38;5;16;48;5;2m'
    red = '\x1b[38;5;16;48;5;1m'
    end = '\x1b[0m'
    output = []
    matcher = difflib.SequenceMatcher(None, string_a, string_b)
    for opcode, a0, a1, b0, b1 in matcher.get_opcodes():
        if opcode == "equal":
            output += [string_a[a0:a1]]
        elif opcode == "insert":
            output += [green + string_b[b0:b1] + end]
        elif opcode == "delete":
            output += [red + string_a[a0:a1] + end]
        elif opcode == "replace":
            output += [green + string_b[b0:b1] + end]
            output += [red + string_a[a0:a1] + end]
    output = "".join(output)
    print(f"\n{output}\n")

