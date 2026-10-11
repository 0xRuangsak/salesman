#!/usr/bin/env python3
"""Project the per-reply benchmark onto a whole agent session.

bench.py measures one reply. A coding-agent session is many model calls, most of whose output is
tool calls, code and reasoning that a style rule leaves alone. This script scales the measured
numbers up to a session with published usage data, and says how. Every input is either measured in
this repo or taken from a source listed below; nothing is a model run.

    python3 benchmarks/session.py            # markdown tables
    python3 benchmarks/session.py --json     # machine-readable

The model, per session:

    calls      = OUTPUT_PER_SESSION / OUTPUT_PER_CALL          model calls in the session
    requests   = calls / CALLS_PER_REQUEST                     things the user asked for
    tool_calls = requests * TOOL_CALLS_PER_REQUEST
    prose      = requests * REPLY_TOKENS                       the text a person reads
    payload    = OUTPUT_PER_SESSION - prose                    tool calls, code, reasoning: untouched

    output(mode)   = prose * ratio(mode) + payload + tool_calls * narration
    re-read(mode)  = extra_output * (calls - 1) / 2 + skill_tokens * calls

ratio(mode) is the measured reply ratio from bench.py, narration is the measured cost of narrating one
tool call (benchmarks/examples/tool-run-*.md), and skill_tokens is the size of the mode's SKILL.md.
Every extra output token stays in the conversation and is sent again with each later call, so on
average it is re-read (calls - 1) / 2 more times; the skill text is re-read on every call. Prompt
caching makes re-reads cheaper, not free.

Sources, read October 2026:
  OUTPUT_PER_SESSION 10,000. Anthropic's Claude Code cost page shows an example session of 5.3k output
    tokens (code.claude.com/docs/en/costs). Three agents on SWE-bench Verified used 5,562 to 9,775
    output tokens per task (arXiv 2606.14061, Table 1, text agents). TraceLab's 2,676 real Claude Code sessions average
    about 44k output tokens, a mean pulled up by a long tail (arXiv 2606.30560, Table 1). 10,000 sits
    between the typical session and the mean.
  OUTPUT_PER_CALL 252: median output tokens per Claude Code model call (TraceLab, Table 8).
  CALLS_PER_REQUEST 8.8 and TOOL_CALLS_PER_REQUEST 10.8: per user request (TraceLab, Introduction).
  REPLY_TOKENS 441: mean assistant tokens per turn in WildChat, one million real conversations
    (arXiv 2405.01470, dataset statistics table, Llama-2 tokenizer).
  CHAT_TURNS 2.54: mean turns per WildChat conversation (same table), for the chat-only row.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bench import count  # noqa: E402

OUTPUT_PER_SESSION = 10_000
OUTPUT_PER_CALL = 252
CALLS_PER_REQUEST = 8.8
TOOL_CALLS_PER_REQUEST = 10.8
REPLY_TOKENS = 441
CHAT_TURNS = 2.54

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "benchmarks" / "examples"
MODES = ["normal", "salesman", "megasale", "ultrasale"]
LABELS = {"normal": "Normal agent", "salesman": "`/salesman`", "megasale": "`/megasale`", "ultrasale": "`/ultrasale`"}


def tokens(path: Path) -> int:
    return count(path.read_text(encoding="utf-8").rstrip("\n"))


def project():
    reply = {m: tokens(EXAMPLES / f"{m}.md") for m in MODES}
    ratio = {m: reply[m] / reply["normal"] for m in MODES}
    narration = tokens(EXAMPLES / "tool-run-salesman.md") - tokens(EXAMPLES / "tool-run-normal.md")
    skill = {m: (tokens(ROOT / "skills" / m / "SKILL.md") if m != "normal" else 0) for m in MODES}

    calls = OUTPUT_PER_SESSION / OUTPUT_PER_CALL
    requests = calls / CALLS_PER_REQUEST
    tool_calls = requests * TOOL_CALLS_PER_REQUEST
    prose = requests * REPLY_TOKENS
    payload = OUTPUT_PER_SESSION - prose

    rows = []
    for m in MODES:
        out = prose * ratio[m] + payload + (tool_calls * narration if m != "normal" else 0)
        extra = out - OUTPUT_PER_SESSION
        reread = extra * (calls - 1) / 2 + skill[m] * calls
        chat = CHAT_TURNS * REPLY_TOKENS * ratio[m]
        rows.append({"mode": m, "reply_tokens": reply[m], "reply_ratio": round(ratio[m], 1),
                     "session_output": round(out), "session_ratio": round(out / OUTPUT_PER_SESSION, 1),
                     "extra_reread": round(reread), "chat_session_output": round(chat)})
    shape = {"calls": round(calls, 1), "requests": round(requests, 1), "tool_calls": round(tool_calls, 1),
             "prose": round(prose), "payload": round(payload), "narration_per_tool_call": narration}
    return shape, rows


def main() -> int:
    shape, rows = project()
    if "--json" in sys.argv:
        print(json.dumps({"session": shape, "modes": rows}, indent=2))
        return 0
    print(f"A {OUTPUT_PER_SESSION:,}-token session: {shape['calls']} model calls, {shape['requests']} requests, "
          f"{shape['tool_calls']} tool calls; {shape['prose']:,} tokens of prose, {shape['payload']:,} of payload. "
          f"Narrating one tool call costs {shape['narration_per_tool_call']} tokens.")
    print()
    print("| Mode | Output per agent session | vs normal | Extra tokens re-read as context | Output per chat |")
    print("|---|---:|---:|---:|---:|")
    for r in rows:
        print(f"| {LABELS[r['mode']]} | {r['session_output']:,} | {r['session_ratio']}x | "
              f"{r['extra_reread']:,} | {r['chat_session_output']:,} |")
    print()
    print("Projected from benchmarks/bench.py and published usage data; see the sources in this script.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
