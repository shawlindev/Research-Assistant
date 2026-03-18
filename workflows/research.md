# Research Workflow

How to use this system to process academic papers and build a structured knowledge base.

---

## Core Loop

For each paper or research session:

1. **Identify the topic** — which track does this belong to? Check `obsidian/tracks/` for existing ones.
2. **Load the paper into NotebookLM** — add it to the relevant `[RESEARCH] <topic>` notebook.
3. **Ask targeted questions** — see question templates below.
4. **Write findings to the track** — observations go into `obsidian/tracks/<topic>.md`.
5. **Close the session** — `close_session` writes a session note and backs up automatically.

---

## NotebookLM Notebooks

- **One notebook per topic** (e.g., `[RESEARCH] Transformer Architectures`, `[RESEARCH] Climate Models`)
- Add multiple papers to the same notebook when they share a topic — NotebookLM can synthesize across them
- Sources can be PDFs, URLs, or pasted text

**Creating a notebook:**

```bash
notebooklm create --title "[RESEARCH] <topic>"
notebooklm source add <notebook-id> --file paper.pdf
```

**Querying:**

```bash
notebooklm query <notebook-id> "What is the main contribution of this paper?"
```

---

## Question Templates

Good starting questions for any new paper:

- What problem does this paper solve?
- What is the proposed method or approach?
- What are the key results and metrics?
- What are the limitations acknowledged by the authors?
- How does this compare to prior work?
- What are the most relevant citations?

---

## Track Naming

One track per research topic, not per paper. Papers are sources; tracks are knowledge.

```
obsidian/tracks/
├── attention-mechanisms.md
├── climate-modeling.md
└── protein-folding.md
```

Use lowercase, hyphenated names. Create a new track when starting a genuinely new topic.

---

## Observation Types

When writing to a track, use typed observations:

| Tag | When to use |
|-----|-------------|
| `[finding]` | Empirical result, metric, or conclusion from a paper |
| `[decision]` | Choice made about how to organize or interpret the research |
| `[constraint]` | Limitation noted in the paper or the research area |
| `[issue]` | Open question or contradiction between sources |
| `[next]` | Follow-up paper to read or question to investigate |

---

## Session Close

At the end of every session:

```bash
python3 -m tools.obsidian.close_session \
  --track <topic> \
  --state active \
  --in-progress "..." \
  --next "..." \
  --observation "[finding] ..." \
  --title "Session title" \
  --summary "What was covered this session."
```
