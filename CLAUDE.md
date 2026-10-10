# CLAUDE.md, salesman

Salesman is a parody of [caveman](https://github.com/JuliusBrussee/caveman).
Caveman makes an agent say less. Salesman makes it say more. Every rule here is
one of caveman's, turned around.

## What ships

- `skills/salesman/SKILL.md`: the voice. Greeting, gratitude, restatement,
  background, answer, recap, three offers, P.S.
- `skills/ultrasale/SKILL.md`: the timeshare presentation. Tiers, a fictional
  testimonial, a comparison table, a FAQ nobody asked for.
- `skills/megasale/SKILL.md`: the fine print. Recitals, Definitions, numbered
  clauses, Exhibits.
- `commands/*.toml`: Gemini CLI slash commands. Claude Code invokes the skills
  directly as `/salesman`, `/ultrasale`, `/megasale`.
- `benchmarks/`: the one example answer in every mode, and the script that
  counts its tokens. README numbers come from that script, never from memory.

## Rules for changing the skills

- The answer stays correct. Padding is the joke; a wrong fact or a broken
  code block is not. Every mode keeps code, commands, paths, numbers, error
  strings and negations verbatim.
- Persisted content stays normal: code, comments, commits, docs, issues, PRs.
  Salesman talks, salesman does not sign. Do not weaken this rule.
- No invented real people, companies, or studies. Testimonials are labeled
  fictional. The README's "numbers" are measured by `benchmarks/bench.py`.
- Keep the mirror. Each rule in `skills/salesman/SKILL.md` answers a rule in
  caveman's `SKILL.md` in the same position. New rule in one? Find its
  opposite.

## Working in this repo

When you edit skill text, re-run `python3 benchmarks/bench.py` and paste the
new table into `README.md` if the example answers changed. Commit messages,
code comments, and anything else that lands in git: plain prose, normal length.
