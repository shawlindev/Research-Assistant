---
name: obsidian-protocol
description: >
  Manages session context via Obsidian tracks and session notes. Activate at session START when the
  user says "context check", "catch me up", "what's the status", or names a workstream/track.
  Activate at session END when the user says "wrap up", "close session", "let's finish", or the
  session is clearly ending. Governs the opening ritual (read track files) and closing ritual
  (close_session tool).
---

# Obsidian Protocol

## Opening Ritual

When a workstream is named or implied in the user's message:

1. Run `ls obsidian/tracks/` to discover available tracks
2. Read `obsidian/tracks/<name>.md` — **start with `## Status`** (instant orientation)
3. Read `## Context` if doing actual work on the track
4. Scan last 5-10 `## Observations` entries if the session builds on prior work
5. If cross-track impact is likely, read linked tracks' `## Status` only

If no tracks exist yet, offer to create one: "No tracks found. Want me to create one for this workstream?"

If the track isn't obvious from the message, ask: **"Which track are we working on?"**

## Closing Ritual

At the end of any significant session, run a single command — do not split into separate steps:

```bash
python3 -m tools.obsidian.close_session \
  --track <name> [--track <name2>] \
  --state active|paused|blocked|complete \
  --in-progress "what's being worked on" \
  --next "next action" \
  --observation "[type] description" \
  --title "Session title" \
  --summary "What was accomplished" \
  [--work-done "..." --decisions "..." --next-steps "..."]
```

Only close significant sessions: decision made, feature built, bug fixed, batch interpreted, workflow updated.

If `## Context` needs revision — flag it and ask the user before editing.

## Observation Types

| Tag | When to use |
|-----|-------------|
| `[decision]` | Architecture, scope, or approach choice |
| `[finding]` | Empirical result from batch, test, or analysis |
| `[constraint]` | Hard rule — must not be violated |
| `[issue]` | Known problem, not yet resolved |
| `[next]` | Actionable next step |

## Constraints

- `obsidian/` is gitignored — never commit it
- `obsidian/memory/` is read-only mirror — source of truth is `~/.claude/.../memory/`
- `## Context` and `## Dependencies` in track files: edit only with user confirmation
