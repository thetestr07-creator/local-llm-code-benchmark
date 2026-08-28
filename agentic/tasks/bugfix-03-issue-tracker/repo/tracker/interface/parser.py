"""Parse a single command line into (verb, args, options).

Grammar (whitespace-separated), options are `--key value`:
    new "<title>" [--template bug] [--priority high] [--label x --label y]
    label <issue-id> <label>
    status <issue-id> <status>
    comment <issue-id> <author> <text...>
    show <issue-id>
    list

Quoted titles/text may use double quotes to include spaces.
"""
import shlex


def parse(line):
    tokens = shlex.split(line)
    if not tokens:
        raise ValueError("empty command")
    verb = tokens[0]
    rest = tokens[1:]
    args = []
    options = {}
    multi = {}  # options that may repeat, e.g. --label
    i = 0
    while i < len(rest):
        tok = rest[i]
        if tok.startswith("--"):
            key = tok[2:]
            if i + 1 >= len(rest):
                raise ValueError("option --%s needs a value" % key)
            val = rest[i + 1]
            if key == "label":
                multi.setdefault("label", []).append(val)
            else:
                options[key] = val
            i += 2
        else:
            args.append(tok)
            i += 1
    if multi:
        options.update(multi)
    return verb, args, options
