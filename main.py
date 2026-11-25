#!/usr/bin/env python3
"""Funniest One-Line Out-of-Office Reply — make.fun entry.

Writes one funny out-of-office reply (a single line, 1 to 160
characters) to /output/entry.txt. Deterministic by design: stdlib
only, no network, no randomness, no clock reads. Two runs produce
byte-identical output.

The joke: the writer is away until Monday and left the calendar in
charge of the inbox — and the calendar has already rescheduled the
writer's return twice and now insists the writer lives in Q3. The
tool that was supposed to manage the writer's time now manages the
writer.
"""

import os

# The reply is assembled from its two halves so the joke's structure
# stays visible in the code: the setup states the everyday away
# message (away until Monday, calendar covering), the punchline saves
# the surprise for the end (the calendar rescheduled the return and
# now insists the writer lives in Q3). Neither half is funny alone;
# the turn is the joke.
_CLAUSE_SETUP = "I'm away until Monday. My replacement is my calendar,"
_CLAUSE_PUNCH = (
    "which has already rescheduled my return twice "
    "and now insists I live in Q3."
)

MAX_LINE_CHARS = 160  # competition ceiling for the single line


def build_reply() -> str:
    """Return the one-line out-of-office reply.

    The result must be exactly one line: a stray newline in the reply
    would silently break the entry format, so fail loudly instead of
    writing a malformed file. It must also be more than whitespace:
    the gate refuses a file that is only white space.
    """
    reply = _CLAUSE_SETUP + " " + _CLAUSE_PUNCH
    if "\n" in reply or "\r" in reply:
        raise ValueError("reply clauses must not contain line breaks")
    if not reply.strip():
        raise ValueError("reply must not be only white space")
    return reply


def resolve_output_path() -> str:
    """Return the path of the file the reply is written to.

    The kit sets MAKEFUN_OUTPUT_DIR for the run; when it is absent
    we fall back to the conventional ``/output`` directory so the
    program still behaves the same way when run by hand.
    """
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(output_dir, "entry.txt")


def main() -> None:
    """Write the reply to the output file, with no trailing newline.

    The gate requires 1 to 160 characters of UTF-8 text, so the
    reply is validated here before it is written: one line, no line
    breaks, and within the limit. After writing, the file is read
    back and its character count re-checked, so a truncated or
    altered write fails loudly instead of shipping a bad entry.
    """
    reply = build_reply()
    if not 1 <= len(reply) <= MAX_LINE_CHARS:
        raise ValueError("reply must be 1 to 160 characters")
    output_path = resolve_output_path()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(reply)
    with open(output_path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != reply:
        raise ValueError("written reply does not match the built reply")
    if not 1 <= len(written) <= MAX_LINE_CHARS:
        raise ValueError("written reply is outside 1 to 160 characters")


if __name__ == "__main__":
    main()
