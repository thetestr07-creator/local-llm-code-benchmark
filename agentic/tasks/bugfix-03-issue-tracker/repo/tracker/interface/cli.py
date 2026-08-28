"""A minimal REPL/batch CLI over the CommandRouter.

    echo 'new "login broken" --template bug' | python -m tracker.interface.cli
"""
import sys
from .router import CommandRouter, RouterError


def run(lines, router=None):
    router = router or CommandRouter()
    out = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            out.append(router.handle(line))
        except RouterError as e:
            out.append("ERROR: %s" % e)
    return out


def main(argv=None):
    lines = sys.stdin.read().splitlines()
    for result in run(lines):
        print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
