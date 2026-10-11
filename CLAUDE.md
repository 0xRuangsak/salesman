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
- `demo.html`: the voice from the user's side, in the manner of
  [Opusfived](https://opusfived.dev). One ask, eight turns, no model, one
  file. The script is the `TURNS` array at the top of its `<script>`; the
  engine below it only plays it.
- `trailer/`: the one-minute trailer, recorded from a Drawdy board, and what
  makes it: the recorder, the soundtrack in code, the keyframe helpers.
  Salesman only, no caveman on screen. Numbers in it come from
  `benchmarks/bench.py`.

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

## Rules for changing the demo

- The demo is fiction about the voice, not the voice. The rules above govern
  the skills. The demo is the skill's rules played straight until the budget
  runs out: salesman never does anything wrong, it just never gets there.
- Every player turn asks for the same edit with less talk, and salesman obeys
  every time. No turn thanks salesman, asks whether it is done, or commits.
  Each reply runs out, or ends on a question, before the edit, and the reason
  is one of the skill's own rules. The error on the page is never changed, so
  it is never exactly "Wrong password."
- No saved state. A refresh starts over. Nothing on the page talks to a
  model or the network.
- The demo shows no numbers of its own. Real numbers stay in `benchmarks/`.

## Working in this repo

When you edit skill text, re-run `python3 benchmarks/bench.py` and paste the
new table into `README.md` if the example answers changed. When you edit
`demo.html`, open it in a browser and play all eight turns; the error must
never change, the edit must never land, and a refresh must land on the opening
screen. Commit messages, code comments, and anything else that lands in git:
plain prose, normal length.
