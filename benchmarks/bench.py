#!/usr/bin/env python3
"""Count the tokens of the example answers in benchmarks/examples/.

The README's numbers come from this script. Run it after editing any example.

    python3 benchmarks/bench.py            # markdown table
    python3 benchmarks/bench.py --json     # machine-readable

Counts use tiktoken's o200k_base encoding, the same approximation caveman's
README uses, so the two tables compare. Requires `pip install tiktoken`.
"""

import json
import sys
from pathlib import Path

ORDER = ["caveman", "normal", "salesman", "ultrasale", "megasale"]
LABELS = {
    "caveman": "`/caveman` (the competition)",
    "normal": "Normal agent",
    "salesman": "`/salesman`",
    "ultrasale": "`/ultrasale`",
    "megasale": "`/megasale`",
}


def count(text: str) -> int:
    import tiktoken

    return len(tiktoken.get_encoding("o200k_base").encode(text))


def main() -> int:
    examples = Path(__file__).resolve().parent / "examples"
    rows = []
    for name in ORDER:
        path = examples / f"{name}.md"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8").rstrip("\n")
        rows.append({"mode": name, "tokens": count(text), "words": len(text.split())})

    base = next(r["tokens"] for r in rows if r["mode"] == "normal")
    for r in rows:
        r["vs_normal"] = round(r["tokens"] / base, 1)

    if "--json" in sys.argv:
        print(json.dumps(rows, indent=2))
        return 0

    print("| Mode | Same answer | Tokens | vs normal |")
    print("|---|---|---:|---:|")
    for r in rows:
        print(f"| {LABELS[r['mode']]} | see `benchmarks/examples/{r['mode']}.md` | {r['tokens']} | {r['vs_normal']}x |")
    print()
    print("Token counts: tiktoken o200k_base.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
