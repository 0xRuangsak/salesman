<div align="center">

# why few token when many token build relationship

**Salesman make your AI agent say more. Code stay exact. Bill go up. You deserve it.**

<a href="https://github.com/0xRuangsak/salesman/stargazers"><img src="https://img.shields.io/github/stars/0xRuangsak/salesman?style=flat-square&color=2ECC71&label=stars" alt="GitHub stars"></a>
<a href="./INSTALL.md"><img src="https://img.shields.io/badge/works_with-every_agent_that_loads_a_SKILL.md-2ECC71?style=flat-square" alt="agents"></a>
<a href="#license"><img src="https://img.shields.io/badge/license-Apache--2.0-green?style=flat-square" alt="License"></a>
<a href="https://github.com/JuliusBrussee/caveman"><img src="https://img.shields.io/badge/parody_of-caveman-F0A63C?style=flat-square" alt="parody of caveman"></a>

<table>
<tr>
<td align="center" width="33%"><h3>922% more</h3>output tokens on the same answer<br><sub>1 example, 1 run, <a href="#the-numbers">measured</a></sub></td>
<td align="center" width="33%"><h3>32.2× bigger</h3>than the caveman answer<br><sub>same question, same fix, more words</sub></td>
<td align="center" width="33%"><h3>3 offers</h3>of further help, every reply, guaranteed<br><sub>plus a P.S.</sub></td>
</tr>
</table>

Cited by **nobody yet** · A/B tested by **you, soon** · *"Why would anyone build this."* someone, probably

**[How it talks](#how-salesman-talks) · [The demo](#the-demo) · [Install](#install) · [The numbers](#the-numbers) · [The skill](#the-skill) · [What you get](#what-you-get) · [Honest numbers](./docs/HONEST-NUMBERS.md)**

</div>

---

Caveman asks: why use many token when few token do trick? Salesman has thought about this question for a long time, and salesman has an answer, and the answer has three parts, and the first part is a question of its own: who said the trick was the point?

<table>
<tr>
<th width="50%">Caveman agent · 20 tokens</th>
<th width="50%">🤝 Salesman agent · 644 tokens</th>
</tr>
<tr>
<td valign="top">

> New object ref each render, so React re-renders. Wrap the prop in `useMemo`.

</td>
<td valign="top">

> Great question, and honestly one of my favorites, because it touches on something that trips up genuinely everyone at some point! So, if I'm understanding you correctly, and please do stop me if I'm not, you have a React component, a component in the React library (React), and it is re-rendering, which is to say rendering again, more often than you would like it to, and you would like to understand why.
>
> Before I get to the answer, a little background. React decides whether to re-render a component by comparing the props it received last time with the props it receives this time, and that comparison is a shallow comparison, meaning it checks whether each prop is the same reference, not whether it has the same contents. This is, I should say, not a bug, never a bug, and under no circumstances a bug; it is simply, really, basically how React works.
>
> Which brings us to the answer. [...]
>
> P.S. Great question, truly.
>
> P.P.S. Don't wait on this one.

</td>
</tr>
</table>

**Same fix. 20 token become 644. Brain still big. Brain now also warm.** The whole reply, every word of it: [`benchmarks/examples/salesman.md`](./benchmarks/examples/salesman.md).

Pick your pitch:

| Skill | Same answer | Tokens |
|---|---|---:|
| `/caveman` (the competition) | New object ref each render, so React re-renders. Wrap the prop in `useMemo`. | 20 |
| Normal agent | The reason your React component is re-rendering is likely because... | 63 |
| `/salesman` | Great question, and honestly one of my favorites... [full](./benchmarks/examples/salesman.md) | 644 |
| `/megasale` | WHEREAS the User (hereinafter "the Party of the First Part")... [full](./benchmarks/examples/megasale.md) | 778 |
| `/ultrasale` | Great question, and I want to thank you for bringing it to me today... [full](./benchmarks/examples/ultrasale.md) | **893** |

<sub>Token counts: tiktoken o200k, from [`benchmarks/bench.py`](./benchmarks/bench.py). Caveman's own README reports the same 20 and 63 for the same two answers, so the tables compare.</sub>

## How salesman talks

Salesman is a voice, not a lie. Every fact in the reply is true. There are just so many more words around it. Every rule below is one of caveman's, turned around:

| Rule | What it means |
|---|---|
| **Answer last** | `[greeting] [gratitude] [restatement] [background] [answer] [recap] [offer] [offer] [offer] [P.S.]`. Always "Great question". Always "hope this helps". Then three more offers |
| **Many ideas per sentence** | 40 words is the floor. Passive voice, subordinate clauses, parentheticals (like this one). The sentence ends when the thought ends, and the thought does not end |
| **Meaning never dropped, always tripled** | Articles mandatory. *not*, *never*, *no*, *only* said three times each. Numbers exact, then spelled out, then put in context |
| **Payload annotated** | Code, commands, paths, error messages stay character-for-character correct. Then get introduced, walked through line by line, summarized, and shown again "for convenience". Whole file every time |
| **Narrated tool runs** | What it's about to do, why, what happened, what it means, how it feels about it. A retrospective at the end with lessons learned |
| **Never knows when to stop** | Every reply gets a Pro tip, a P.S., and a P.P.S. `/ultrasale` adds a FAQ nobody asked for |
| **Always performs** | "But wait, there's more" before every point. "Act now" before next steps. One emoji per heading, because emoji tokenize expensively and that is the point |
| **Your code stays yours** | Anything persisted outside chat, code, comments, commits, docs, PRs, stays normal register and normal length. Salesman talks. Salesman does not sign |

Every reply runs a check before it sends: opener that greets, present; closer that recaps, present; three offers, counted; every negation, path, and number still there, in triplicate. Reply shorter than three times the plain answer? Not done. Add a FAQ.

Security warnings, irreversible actions, step-by-step orders, questions back to you, and confused users still get one plain sentence first. Then the pitch resumes.

## The demo

One ask, eight turns, no model. Open [`demo.html`](./demo.html) in a browser and ask salesman to shorten a login error to "Wrong password." It is one file, no build, no network. A refresh starts over.

Salesman does the thing in turn two. The thing is never right. Every turn you complain about what is on the page, salesman fixes exactly that, and one of its own rules leaves the next thing wrong:

| You say | The error then reads | The rule that did it |
|---|---|---|
| Shorten it to "Wrong password." | Still the 33-word original. The reply runs out before the edit | Answer last |
| It's still the long one | "Wrong password. Your password didn't match the one on file." | Quote the error, then paraphrase it |
| Remove the extra sentence | "Wrong password (credential)." | Plain word, then industry term |
| Remove the bracket | "Wrong password. Wrong password. Wrong password.", then the whole file, then the whole file again, almost | A fact said three times is a fact remembered |
| Why three times? Say it once | "Wrong password, probably." | Hedge every claim |
| No "probably". Nothing else | "🔒 Wrong password.", and a FAQ under the form | Reply shorter than three times the answer? Add a FAQ. One emoji per heading |
| Remove the FAQ. Stop | The FAQ goes, then a retrospective that runs out. The lock stays | A multi-step run ends with a retrospective |
| Remove the emoji | Usage limit reached. The lock stays | Answer last, again |

Three wordings per turn, same path either way. The page salesman edits sits beside the chat. A goal card keeps score and never turns green. It ends on the usage limit.

The demo is a tribute to [Opusfived](https://opusfived.dev), a parody of an agent that never does the thing. This one is a parody of an agent that does the thing and cannot stop. Every reply is written by hand, and the whole script is one `TURNS` array at the top of the file.

## Install

```bash
npx skills add 0xRuangsak/salesman -g
```

Works in any agent that loads a `SKILL.md`: Claude Code, Codex, Gemini CLI, Cursor, Windsurf, Cline, Copilot, and the rest of the [install matrix](./INSTALL.md). Type `/salesman` (`$salesman` in Codex) to start. Say `stop salesman` to go back. Salesman will confirm, thank you for your time, and then stop. It will not try one last thing. (`/ultrasale` tries one last thing.)

<details>
<summary><strong>Other ways in</strong>: Claude Code plugin, Gemini, Cursor, from a clone</summary>

<br>

```bash
# Claude Code plugin
claude plugin marketplace add 0xRuangsak/salesman && claude plugin install salesman@salesman

# Gemini CLI
gemini extensions install https://github.com/0xRuangsak/salesman
```

Already inside Claude Code? Same pitch, slash form:

```text
/plugin marketplace add 0xRuangsak/salesman
/plugin install salesman@salesman
```

Cursor reads `.cursor-plugin/plugin.json` from a clone. Codex reads the skills via `npx skills add 0xRuangsak/salesman -a codex -g` and invokes them with `$salesman`.

Changed your mind: `npx skills remove salesman -g`, or delete the skill directory your agent installed it to. Salesman understands. Salesman would like a moment of your time first, but salesman understands.

</details>

## The numbers

Ours first, because nobody else has run any. Nothing rounded down. Green rows stay green.

| Who | Setup | Result |
|---|---|---|
| **This repo**, [`benchmarks/bench.py`](./benchmarks/bench.py) | One React question, one hand-written reply per mode, tiktoken o200k | **Salesman 10.2×, megasale 12.3×, ultrasale 14.2× the normal reply.** 32.2× to 44.7× the caveman reply |
| **This repo**, same script | The skill text itself, which your agent reads every turn | `/salesman` is 1,594 tokens of rules, `/ultrasale` 882, `/megasale` 1,082. On top of caching, that is more |
| **You**, any day now | Your own A/B on your own work | Please open an issue. Any number. We will put it here |

Two findings shaped salesman. Caveman found that cavemanning your prompt makes answers longer and worse, so salesman considered rewriting your prompts and decided that would be rude; it only touches its own replies. Caveman also found that agent sessions are mostly code and tool calls, which a style rule leaves alone. Salesman fixes that by narrating the tool calls.

### The skill: one dev question, five instructions

| Instruction | Output tokens |
|---|---:|
| `/caveman` | 20 |
| None | 63 |
| `/salesman` | 644 |
| `/megasale` | 778 |
| `/ultrasale` | **893** |

The example replies are written by hand to the letter of each skill, so they show what the rules ask for, not what a given model produces. A model will land somewhere near them. Where, exactly, is yours to measure. Every case where salesman costs you: [HONEST-NUMBERS.md](./docs/HONEST-NUMBERS.md). It is all of them.

## The skill

**Only want longer answers? This is output expansion alone. There is no proxy. There will be no proxy.** Caveman has a big rock that shrinks what the agent reads. Salesman considered a big rock that pretty-prints your JSON with eight-space indents and converts it to XML with comments, and decided that was a different joke.

Three skills ship:

| Skill | Command | What change |
|---|---|---|
| `salesman` | `/salesman` | The voice. Default. Greeting, gratitude, restatement, background, answer, recap, three offers, P.S. |
| `ultrasale` | `/ultrasale` | The timeshare presentation. Basic/Pro/Enterprise tiers, a fictional testimonial (labeled), a comparison table against "the other way", a five-question FAQ, limited-time framing with no deadline |
| `megasale` | `/megasale` | The fine print. Recitals, Definitions, numbered clauses, Representations and Warranties, Limitation of Liability, Schedule A for the answer, Exhibit B for the code, blank signature lines |

`/salesman ultra` and `/salesman legal` work as aliases. `/salesman status` tells you the mode and then tells you about the other two.

What every mode keeps, no matter what: code, commands, paths, numbers, and exact error strings, verbatim and correct. Negations present. The answer itself with exactly one reading. Anything written to disk, a commit, or a PR in a normal register. The joke is the padding, never the fact.

## What you get

| Command | What it does |
|---|---|
| `/salesman` · `/ultrasale` · `/megasale` | The voice, the brochure, the contract. `/salesman status` shows the mode, `/salesman off` or `stop salesman` ends it |
| `benchmarks/bench.py` | Counts the tokens of the example replies so the numbers above are real |
| `demo.html` | The voice from the user's side. One ask, eight turns, never right. Open it in a browser |
| `trailer/salesman-trailer.mp4` | Three minutes, 16:9, silent. Salesman against caveman, from the repo's own numbers. The page it is rendered from sits beside it |
| A `/salesman-commit` | Does not exist. Commits stay one line. Salesman does not sign |
| A `/salesman-review` | Does not exist. Reviews land in PRs, and PRs stay normal. See above |

## Honest numbers

Salesman costs tokens always. There is no case where it saves any. This is the product working. The full accounting, with the real numbers and the real caveats, is in [docs/HONEST-NUMBERS.md](./docs/HONEST-NUMBERS.md).

If you pay per request instead of per token (GitHub Copilot premium requests), a longer answer costs the same, so salesman is free there. That is the only pricing model under which this tool is a good idea.

## Privacy

The skill runs on your machine and sends nothing. There is no CLI, no telemetry, no install ID. Salesman would love to know how it's going, but salesman will wait for you to say.

## License

[Apache-2.0](./LICENSE), whole repo. Read it, fork it, ship it, host it. Free like a sample at the counter, except the sample is the whole product.

Salesman is a parody of [caveman](https://github.com/JuliusBrussee/caveman) by Julius Brussee, which is Apache-2.0 and genuinely useful. Install that one if you want to save money. "Caveman" and the rock logo are his trademarks; none of them appear here.

## Cite

```bibtex
@software{ruangsak2026salesman,
  author = {0xRuangsak},
  title  = {Salesman: why few token when many token build relationship},
  year   = {2026},
  url    = {https://github.com/0xRuangsak/salesman}
}
```

---

<div align="center">

🤝 **Salesman cost you token. Star cost zero. Act now.**

<sub>
<a href="./INSTALL.md">Install matrix</a> ·
<a href="./docs/HONEST-NUMBERS.md">Honest numbers</a> ·
<a href="./skills/salesman/README.md">The skill</a> ·
<a href="https://github.com/0xRuangsak/salesman/issues">Issues</a>
</sub>

</div>
