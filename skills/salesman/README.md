# salesman

Talk like friendly salesman. Same brain, more tokens.

## What it does

Makes the model answer last and build the ceremony: greeting, gratitude, a restatement of the question, background, the answer, a recap, three offers of further help, and a P.S. Articles never drop. Negations get said three times. Code, commands, paths, numbers, and exact error strings never change, then get walked through line by line. Measured once on one hand-written example (`benchmarks/bench.py`, tiktoken o200k): salesman 10.2× the normal reply, megasale 12.3×, ultrasale 14.2×. Mode persists until stopped.

Salesman is one of three sibling skills:

| Skill | Command | What change |
|-------|---------|-------------|
| `salesman` | `/salesman` | The voice. Default. Greeting, gratitude, restatement, background, answer, recap, offers, P.S. |
| `ultrasale` | `/ultrasale` | The presentation. Tiers, a fictional testimonial, a comparison table, a FAQ nobody asked for. |
| `megasale` | `/megasale` | The fine print. Recitals, Definitions, numbered clauses, Exhibits, blank signature lines. |

`/salesman ultra` and `/salesman legal` work as aliases.

Auto-clarity: every skill gives one plain sentence first for security warnings, irreversible-action confirmations, step sequences, questions back to you, and a user who repeats a question. Then resumes at full volume. Anything persisted outside chat (code, comments, commits, docs, PRs) stays in a normal register. Salesman talks. Salesman does not sign.

## How to invoke

```
/salesman             # the voice (default)
/salesman status      # show current mode, then hear about the other two
/ultrasale            # the presentation
/megasale             # the fine print
stop salesman         # back to normal prose, after one thank-you
```

No host tracks the mode for you; the model answers from the conversation and marks it `(not tracked by this host)`.

## Example output

Question: "Why does my React component re-render?"

caveman (the competition):
> New object ref each render, so React re-renders. Wrap the prop in `useMemo`.

salesman, first paragraph of eleven:
> Great question, and honestly one of my favorites, because it touches on something that trips up genuinely everyone at some point! So, if I'm understanding you correctly, and please do stop me if I'm not, you have a React component, a component in the React library (React), and it is re-rendering, which is to say rendering again, more often than you would like it to, and you would like to understand why.

Whole reply: [`benchmarks/examples/salesman.md`](../../benchmarks/examples/salesman.md). Siblings: [`ultrasale.md`](../../benchmarks/examples/ultrasale.md), [`megasale.md`](../../benchmarks/examples/megasale.md).

## See also

- [`SKILL.md`](./SKILL.md): full LLM-facing instructions
- [`../ultrasale/`](../ultrasale/) and [`../megasale/`](../megasale/): the sibling skills
- [Salesman README](../../README.md): repo overview, install, the numbers
