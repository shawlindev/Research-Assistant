# Research Workflow — Academic Overlay

**Read [research.md](research.md) first.** This file is a delta — it overrides or extends specific sections of the general workflow for academic-paper research. Everything not mentioned here (core loop, track naming, three-level hierarchy, session close) is unchanged.

When to apply this overlay: the research centers on peer-reviewed papers, pre-prints, or scientific literature. Signals include explicit mention of "paper", "DOI", "arxiv", "pubmed", "bioRxiv/medRxiv", "eLife", "Frontiers", the user dropping a PDF into `papers/`, or an existing track whose `## Status` declares `mode: academic`.

---

## Source Access (overrides general)

Three pathways specific to papers. Try in this order:

### Pathway A — Open-access URL

Add directly. These sources work reliably with NotebookLM:

- PubMed Central (`pmc.ncbi.nlm.nih.gov`)
- eLife (`elifesciences.org`)
- bioRxiv / medRxiv (`biorxiv.org`, `medrxiv.org`)
- Frontiers (`frontiersin.org`)
- arXiv (`arxiv.org`)

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

NotebookLM handles all extraction. The agent's only job is to upload the file.

### Fallback — Web research

Still available when source discovery is needed (e.g., "find key papers on X"):

```bash
notebooklm source add-research "topic query"
```

Use `--mode deep` for broader literature sweeps.

---

## Question Templates (overrides general)

Paper-shaped starter questions:

- What problem does this paper solve?
- What is the proposed method or approach?
- What are the key results and metrics?
- What are the limitations acknowledged by the authors?
- How does this compare to prior work?
- What are the most relevant citations?

Use the general-workflow templates as well if the session is broader than a single paper (e.g., synthesizing across multiple papers in a field).

---

## Cluster & Leaf Types (extends general)

Academic-flavored types to use alongside the general ones:

**Cluster examples:** `protocols`, `mechanisms`, `disease-models`, `limitations`, `findings`, `prior-work`.

**Leaf `type:` values:** add these to the general set — `protocol`, `mechanism`, `model`, `limitation`.

```yaml
---
up: "[[<cluster>]]"
type: protocol  # or: mechanism, model, limitation, finding, comparison
tags: [tag1, tag2]
---
```

The three-level hierarchy (Track → Cluster → Note) and the 3–7 children rule are unchanged.

---

## Observation Flavor (extends general)

Observation tags are identical; only the phrasing shifts toward papers:

| Tag            | Academic framing                                                  |
| -------------- | ----------------------------------------------------------------- |
| `[finding]`    | Empirical result, metric, or conclusion from a paper              |
| `[constraint]` | Limitation noted in the paper or the research area                |
| `[issue]`      | Contradiction between papers, or unresolved debate in the field   |
| `[next]`       | Follow-up paper to read or experiment/question to investigate     |

---

## Track Status (optional)

When opening or updating an academic-mode track, you can record the mode in the track's Status section so future sessions skip the routing gate:

```
## Status
state: active
mode: academic
...
```

This is optional — the routing rule in `CLAUDE.md` already picks up on explicit paper signals in the user's message.
