# Install salesman

One skill. Works for every AI coding agent that loads a `SKILL.md`.

If you just want it to work, run the one-liner. If you want to know what gets touched, it is three Markdown files in a `skills/` directory, and that is all.

## One-liner

```bash
npx skills add 0xRuangsak/salesman -g
```

`-g` installs into the agent's user skill directory. Without it, the skills belong to the current project.

Piping nothing into any shell. The `skills` CLI copies `skills/salesman`, `skills/ultrasale`, and `skills/megasale` into the agent's skill directory and stops.

## Per-agent install

| Agent | Install command | Auto-activates? |
|---|---|:-:|
| **Claude Code** | `claude plugin marketplace add 0xRuangsak/salesman && claude plugin install salesman@salesman` | No. `/salesman` to start |
| **Gemini CLI** | `gemini extensions install https://github.com/0xRuangsak/salesman` | Yes (GEMINI.md imports the salesman skill) |
| **Codex CLI** | `npx skills add 0xRuangsak/salesman -a codex -g` | No. `$salesman` to start |
| **Cursor** | Clone the repo; Cursor reads `.cursor-plugin/plugin.json` | No. Invoke the skill |
| **Windsurf** | `npx skills add 0xRuangsak/salesman -a windsurf -g` | No |
| **Cline** | `npx skills add 0xRuangsak/salesman -a cline -g` | No |
| **GitHub Copilot** | `npx skills add 0xRuangsak/salesman -a copilot -g` | No |
| **opencode** | `npx skills add 0xRuangsak/salesman -a opencode -g`, or drop `AGENTS.md` in your repo | AGENTS.md: yes |
| **Anything else that loads `SKILL.md`** | `npx skills add 0xRuangsak/salesman -a <profile> -g` | No |

`npx skills add --help` lists the profile slugs. Where the host has no slash commands, ask for the skill by name: "use the salesman skill".

Already inside Claude Code? The same install as slash commands:

```text
/plugin marketplace add 0xRuangsak/salesman
/plugin install salesman@salesman
```

## Always-on

Hosts that read an `AGENTS.md` or `GEMINI.md` as standing context get the salesman voice without being asked, because those files import the skill. Copy this repo's `AGENTS.md` into a project to make every reply there a pitch. Remove it to stop. Your teammates will have opinions.

Claude Code has no always-on hook in this repo. Caveman ships a Node hook that activates on session start; salesman ships three Markdown files and a Python script. Type `/salesman` at the top of a session.

## Uninstall

```bash
npx skills remove salesman -g
npx skills remove ultrasale -g
npx skills remove megasale -g
```

Or delete the three directories from wherever your agent keeps skills. For the Claude Code plugin: `claude plugin uninstall salesman@salesman`.

## Tested on

The skill files follow the same frontmatter and layout as caveman's, which installs on 30+ agents. The Claude Code plugin manifest passes `claude plugin validate`. Nothing else here has been run end to end against a live agent yet. If an install breaks, open an issue with the agent and the error text, and open your agent in this repo and say *"Read CLAUDE.md and INSTALL.md, install salesman for me."* It will explain at length.
