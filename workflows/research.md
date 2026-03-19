# Research Workflow

How to use this system to process academic papers and build a structured knowledge base.

---

## Core Loop

For each paper or research session:

1. **Identify the topic** — which track does this belong to? Check `obsidian/tracks/` for existing ones.
2. **Load sources into NotebookLM** — use the appropriate source pathway below.
3. **Ask targeted questions** — see question templates below.
4. **Create atomic notes** — one concept per file in `obsidian/notes/<topic>/`. Update the track's `## Notes` section to link them. Only high-level session observations go into the track itself.
5. **Close the session** — `close_session` writes a session note and updates the track status.

---

## Source Access

Three pathways depending on how the paper is available. Try in this order:

### Pathway A — Open-access URL

Add directly. These sources work reliably:

- PubMed Central (`pmc.ncbi.nlm.nih.gov`)
- eLife (`elifesciences.org`)
- bioRxiv / medRxiv (`biorxiv.org`, `medrxiv.org`)
- Frontiers (`frontiersin.org`)

```bash
notebooklm source add "https://pmc.ncbi.nlm.nih.gov/articles/..."
```

### Pathway B — Paywalled URL

Do not attempt to access the content. Ask the user:

> "This source is behind a paywall. Please provide either your institution credentials or download the PDF directly and drop it in the `papers/` folder."

Once the user provides a file, proceed to Pathway C.

### Pathway C — Local PDF (`papers/` folder)

User drops the PDF into `papers/` at the project root. Then:

1. List `papers/` to discover new files
2. Add each file to NotebookLM — do **not** read the file contents yourself

```bash
notebooklm source add ./papers/paper.pdf
```

Move to `papers/processed/` after successful import to avoid re-adding:

```bash
mv papers/paper.pdf papers/processed/paper.pdf
```

NotebookLM handles all extraction and synthesis. The agent's only job is to upload the file.

### Fallback — Web research

When no specific paper is provided and source discovery is needed:

```bash
notebooklm source add-research "topic query"
```

Use `--mode deep` for broader coverage (slower). Use fast mode (default) for a specific topic.

---

## NotebookLM Notebooks

- **One notebook per topic** (e.g., `[RESEARCH] Transformer Architectures`, `[RESEARCH] Climate Models`)
- Add multiple papers to the same notebook when they share a topic — NotebookLM synthesizes across them
- Sources can be PDFs, URLs, or web research results

```bash
# Create notebook
notebooklm create "[RESEARCH] <topic>"

# Add sources
notebooklm source add "https://..."          # open-access URL
notebooklm source add ./papers/paper.pdf     # local PDF

# Web research (source discovery)
notebooklm source add-research "query"

# Query
notebooklm ask "What is the main contribution of this paper?"
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

```text
obsidian/tracks/
├── attention-mechanisms.md
├── climate-modeling.md
└── protein-folding.md
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
- **Cluster** groups related leaf notes (e.g., protocols, limitations, disease-models). `up:` points to the track.
- **Leaf note** is one atomic concept. `up:` points to its cluster, not the track.

When a cluster grows past 7 notes, split it — that signals a natural sub-topic boundary.

**Rules:**

- One concept per file — protocols, mechanisms, limitations, models, findings each get their own note
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
type: finding  # or: protocol, limitation, model, mechanism
tags: [tag1, tag2]
---
```

---

## Observation Types

When writing typed observations to the track's `## Observations` section:

| Tag            | When to use                                                 |
| -------------- | ----------------------------------------------------------- |
| `[finding]`    | Empirical result, metric, or conclusion from a paper        |
| `[decision]`   | Choice made about how to organize or interpret the research |
| `[constraint]` | Limitation noted in the paper or the research area          |
| `[issue]`      | Open question or contradiction between sources              |
| `[next]`       | Follow-up paper to read or question to investigate          |

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
