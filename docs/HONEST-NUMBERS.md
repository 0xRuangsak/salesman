# Honest Numbers

Salesman cost tokens always. This page say which cases, with the real numbers. No marketing, which for this project is a sacrifice.

## What the response skill does

The salesman response skill makes the model write longer output. The skill itself does not expand input, context, files, or thinking tokens. There is no proxy. There is no engine. There are three Markdown files.

## The measured numbers

| What | Number | How measured | Source |
|---|---|---|---|
| Output increase vs a normal reply | salesman 10.2×, megasale 12.3×, ultrasale 14.2× (n=1, one hand-written reply per mode, output length only, tiktoken o200k) | `benchmarks/bench.py` over `benchmarks/examples/` | [`benchmarks/`](../benchmarks/) |
| Output increase vs the caveman reply | 32.2× to 44.7× | Same | Same |
| Output per agent session, projected | Normal 10,000; salesman 32,431 (3.2×), megasale 36,660 (3.7×), ultrasale 40,290 (4.0×) | The replies above scaled onto a session: prose times the reply ratio, payload unchanged, 84 tokens of narration per tool call, session shape from published usage data | [`benchmarks/session.py`](../benchmarks/session.py), sources in the script |
| Extra context per agent session, projected | 497k to 621k tokens read again, plus the skill text on every call | Each extra output token is re-read by every later call in the session | Same |
| Input reduction from the skill | 0% | It is an output-style instruction | Not applicable |
| Input cost the skill *adds* | 1,594 tokens of rules for `/salesman`, 882 for `/ultrasale`, 1,082 for `/megasale`, per turn before caching | tiktoken o200k over each `SKILL.md` | [`skills/`](../skills/) |
| Model runs | None | Nobody has run one. The example replies are written by hand to the letter of each skill | This page |

Token-count runs measure output length only. The example replies were written to follow the rules, not produced by a model, so they show what the rules ask for. A model following them will land near those lengths and may land past them. No quality claim is published, and none is needed: every mode keeps the answer correct and the code verbatim, and the rest is padding by design.

## When salesman wins

- Billed per request, not per token (GitHub Copilot premium requests, other per-message pricing). A longer answer is the same request. Salesman is free there, and this is the only pricing model under which it is a good idea.
- You wanted to be talked to.

## When salesman loses (net-negative)

- Every per-token workload. The output is 10 to 14 times longer on the one example, and the rules add 882 to 1,594 input tokens per turn before caching. There is no offset.
- Long sessions. Narrated tool runs add text between every call, and every extra token is read again by each later call. On the projected 10,000-token session that is about 22,000 more output tokens and half a million more tokens of context.
- Reading time. Every reply takes longer to read, and the answer is at the end, by rule.
- Anyone else reading the chat. Salesman talks only in chat; code, commits, docs, and PRs stay normal. But the chat is the chat.

## Outside A/Bs

None yet. Open an issue with yours. Any number goes on this page, including the ones where salesman loses, which is all of them.

## Measure it yourself

1. Run the same task with and without `/salesman`, then compare the provider usage or billing page. That A/B outranks this page.
2. Reproduce the repository numbers with `python3 benchmarks/bench.py` and `python3 benchmarks/session.py`.

## Rule of thumb

> Compare provider-billed totals on the same task with and without Salesman.
> If Salesman increases billed cost for the same task, it is working.
