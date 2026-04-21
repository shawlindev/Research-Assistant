# Research Workflow

How to use this system to research any topic and build a structured knowledge base.

> **Academic papers?** If the research is centered on peer-reviewed papers, pre-prints, or scientific literature, also read [research-academic.md](research-academic.md) — it overlays paper-specific source pathways, question templates, and cluster/observation types on top of this workflow.

---

## Core Loop

For each research session:

1. **Identify the topic** — which track does this belong to? Check `obsidian/tracks/` for existing ones.
2. **Load sources into NotebookLM** — use the appropriate source pathway below.
3. **Ask targeted questions** — see question templates below.
4. **Create atomic notes** — one concept per file in `obsidian/notes/<topic>/`. Update the track's `## Notes` section to link them. Only high-level session observations go into the track itself.
5. **Close the session** — `close_session` writes a session note and updates the track status.

---

## Source Access

Three pathways for loading material into NotebookLM. Use whichever fits.

### Pathway A — URL

Add any publicly accessible URL directly:

```bash
notebooklm source add "https://..."
```

Works with articles, documentation, blog posts, reports, or any page with readable content.

### Pathway B — Web research

When you need to discover sources on a topic (most common pathway):

```bash
notebooklm source add-research "topic query"
```

Use `--mode deep` for broader coverage (slower). Default (fast) mode works for focused queries.

### Pathway C — Local file

For files already on disk (PDFs, text files, etc.):

```bash
notebooklm source add ./path/to/file.pdf
```

NotebookLM handles all extraction. The agent's only job is to upload the file.

---

## NotebookLM Notebooks

- **One notebook per topic** (e.g., `[RESEARCH] Instagram Boosting`, `[RESEARCH] RAG`)
- Add multiple sources to the same notebook when they share a topic — NotebookLM synthesizes across them
- Sources can be URLs, web research results, or local files

```bash
# Create notebook
notebooklm create "[RESEARCH] <topic>"

# Add sources
notebooklm source add "https://..."          # open-access URL
notebooklm source add ./path/to/file.pdf     # local file

# Web research (source discovery)
notebooklm source add-research "query"

# Query
notebooklm ask "What are the key insights from these sources?"
```

---

## Question Templates

Good starting questions for any new topic:

- What is the core concept or approach here?
- What are the key takeaways or actionable insights?
- What are the trade-offs or limitations?
- How does this compare to alternatives?
- What would I need to implement or apply this?
- What are the open questions or unresolved debates?

---

## Track Naming

One track per research topic. Sources are inputs; tracks are knowledge.

```text
obsidian/tracks/
├── instagram-boosting.md
├── rag.md
└── ffn-contributor-pipeline.md
```

Use lowercase, hyphenated names. Create a new track when starting a genuinely new topic.

---

## Atomic Notes (Required)

**Do not pack all findings into a single note.** Each distinct concept gets its own file.

### Three-level hierarchy: Track → Cluster → Note

```text
obsidian/tracks/<topic>.md          # track (hub)
obsidian/notes/<topic>/
├── <cluster-a>.md                  # cluster (groups 3–7 related notes)
├── <cluster-b>.md
├── <concept-1>.md                  # leaf note (atomic concept)
├── <concept-2>.md
└── <concept-3>.md
```

- **Track** links to 3–7 clusters in `## Notes`. Never links directly to leaf notes.
- **Cluster** groups related leaf notes (e.g., strategies, trade-offs, implementation-steps). `up:` points to the track.
- **Leaf note** is one atomic concept. `up:` points to its cluster, not the track.

When a cluster grows past 7 notes, split it — that signals a natural sub-topic boundary.

**Rules:**

- One concept per file — strategies, trade-offs, limitations, tools, findings each get their own note
- Use `[[wiki-links]]` in note bodies to connect related notes — these become lateral edges in the graph
- Keep cross-links sparse and meaningful; only link when there is a real relationship
- Add `aliases:` when the filename is awkward as a graph label (acronyms, apostrophes)

**Why:** ExcaliBrain and graph view are only useful when each hub has a limited set of direct children. A track with 17 direct links is noise; a track with 5 clusters, each containing 3–5 notes, is navigable.

**Cluster frontmatter:**

```yaml
---
up: "[[<topic>]]"
aliases: [Readable Label]
type: cluster
tags: [tag1, tag2]
---
```

**Leaf note frontmatter:**

```yaml
---
up: "[[<cluster>]]"
type: finding  # or: strategy, trade-off, limitation, tool, comparison
tags: [tag1, tag2]
---
```

---

## Observation Types

When writing typed observations to the track's `## Observations` section:

| Tag            | When to use                                                 |
| -------------- | ----------------------------------------------------------- |
| `[finding]`    | Key result, metric, or conclusion from sources              |
| `[decision]`   | Choice made about how to organize or interpret the research |
| `[constraint]` | Limitation or hard constraint relevant to the topic         |
| `[issue]`      | Open question or contradiction between sources              |
| `[next]`       | Follow-up to research or question to investigate            |

---

## Session Close

At the end of every session:

```bash
# Optionally update track status mid-session
python3 -m tools.obsidian.write_track <topic> --state active --next "..."

# Close session — updates track status and writes session note
python3 -m tools.obsidian.close_session \
  --track <topic> \
  --state active \
  --in-progress "..." \
  --next "..." \
  --observation "[finding] ..." \
  --title "Session title" \
  --summary "What was covered this session."
```
