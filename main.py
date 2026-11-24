"""make.fun entry: "One Line, One Chill" (u-azazex-one-line-one-chill-6d4d5488).

Gate: /output/entry.txt must be UTF-8 text of 1-200 characters, not only
whitespace. The entry itself is exactly one line and one sentence of horror.
This program writes the winning line's exact UTF-8 bytes (no trailing
newline), chmods the file to 0644, and verifies the result by reading it back.
Standard library only.
"""

import os
import stat

ENTRY = (
    "The nursery monitor only plays its lullaby when the crib is rocked, "
    "and it just started while my baby sleeps in my arms downstairs."
)

OUTPUT_PATH = "/output/entry.txt"


def validate(text: str) -> None:
    """Assert the entry satisfies the gate and the one-sentence brief."""
    assert isinstance(text, str)
    assert 1 <= len(text) <= 200, f"length {len(text)} outside 1-200"
    assert text.strip(), "entry must not be only whitespace"
    assert text == text.strip(), "entry must have no leading/trailing space"
    assert "\n" not in text and "\r" not in text, "entry must be one line"
    # Exactly one sentence: a single terminal period and no other
    # sentence-ending punctuation anywhere in the line.
    assert text.endswith("."), "sentence must end with a period"
    assert text.count(".") == 1, "entry must contain exactly one period"
    assert "!" not in text and "?" not in text, "exactly one sentence only"


def main() -> None:
    validate(ENTRY)
    data = ENTRY.encode("utf-8")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "wb") as fh:
        fh.write(data)
    os.chmod(OUTPUT_PATH, 0o644)

    # Read-back verification: bytes identical, no trailing newline, mode 0644.
    with open(OUTPUT_PATH, "rb") as fh:
        back = fh.read()
    assert back == data, "read-back bytes differ from entry bytes"
    assert not back.endswith(b"\n"), "entry must have no trailing newline"
    mode = stat.S_IMODE(os.stat(OUTPUT_PATH).st_mode)
    assert mode == 0o644, f"mode {oct(mode)} != 0o644"
    validate(back.decode("utf-8"))


if __name__ == "__main__":
    main()
