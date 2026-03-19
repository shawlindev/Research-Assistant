# research-idea-sindy

An AI-assisted research system. Add academic papers via NotebookLM (URLs, PDFs, or web research), ask questions, and Claude writes structured atomic notes into an Obsidian vault — organized into a navigable knowledge graph.

---

## Architecture

**Workflows** — Markdown SOPs in `workflows/` describing how to handle papers, structure notes, and run sessions.

**Agent** — Claude Code orchestrates sessions: loads papers into NotebookLM, queries them, synthesizes answers, writes structured notes into Obsidian.

**Tools** — `tools/obsidian/` scripts for writing tracks, session notes, and managing state.

### Knowledge structure

```text
obsidian/tracks/<topic>.md              # track (hub per research topic)
obsidian/notes/<topic>/
├── <cluster>.md                        # cluster (groups 3–7 related notes)
└── <concept>.md                        # leaf note (one atomic concept)
```

- **Track** — one per research topic, links to 3–7 clusters
- **Cluster** — groups related leaf notes (e.g., protocols, limitations, disease-models)
- **Leaf note** — one concept per file, linked to its cluster via `up:` frontmatter

Optimized for ExcaliBrain and Obsidian graph view: focused hubs, sparse cross-links, readable labels.

### Source pathways

Papers enter the system through NotebookLM via three pathways:

1. **Open-access URL** — added directly (PubMed Central, bioRxiv, eLife, Frontiers)
2. **Local PDF** — dropped into `papers/`, uploaded to NotebookLM, moved to `papers/processed/`
3. **Web research** — NotebookLM discovers and imports sources for a topic query

---

## Prerequisites

- macOS (these instructions assume Homebrew)
- [Claude Code](https://claude.ai/code) CLI installed
- Python 3.11+
- [Obsidian](https://obsidian.md) app

---

## Setup

### 1. Clone the repo

```bash
git clone git@github.com:shawlindev/research-idea-sindy.git ~/Dev/projects/research-idea-sindy
cd ~/Dev/projects/research-idea-sindy
```

### 2. Install Python 3.11 (if needed)

```bash
brew install python@3.11
```

Ensure it's on your PATH — add to `~/.zshrc` if needed:

```bash
export PATH="/opt/homebrew/bin:$PATH"
```

### 3. Install the NotebookLM CLI

```bash
pip3.11 install "notebooklm-py[browser]"
playwright install chromium
```

Authenticate with your Google account:

```bash
notebooklm login
```

A browser window will open — sign in with the Google account that has access to NotebookLM. Session is saved locally.

Install the Claude Code skill:

```bash
notebooklm skill install
```

### 4. Set up the Obsidian vault

Create the vault folder:

```bash
mkdir -p ~/obsidian-brain/research-idea-sindy
```

Open **Obsidian** → **Open folder as vault** → select `~/obsidian-brain/research-idea-sindy`.

Recommended plugins: **Breadcrumbs** (navigation via `up:` frontmatter) and **ExcaliBrain** (visual mind maps from wiki-links).

### 5. Restart Claude Code

Restart Claude Code to pick up the NotebookLM skill.

### 6. Open a session

```bash
cd ~/Dev/projects/research-idea-sindy
claude
```

---

## How to use

Start by telling Claude what you're working on:

> "I have a new paper on attention mechanisms — here's the PDF"

> "Summarize what the papers in my transformer notebook say about positional encoding"

> "What are the open questions across everything I've read on climate modeling?"

At the end of each session, Claude writes structured notes to your Obsidian vault and updates the track status.

---

## What gets saved where

| Content | Location |
|---|---|
| Per-topic tracks and notes | `~/obsidian-brain/research-idea-sindy/` (Obsidian vault) |
| Session summaries | `~/obsidian-brain/research-idea-sindy/sessions/` |
| NotebookLM notebooks | Google's servers (via your account) |
| Repo code and workflows | `~/Dev/projects/research-idea-sindy/` (this repo) |
| Paper PDFs (temporary) | `papers/` (gitignored, moved to `papers/processed/` after import) |

The Obsidian vault is symlinked into the repo but gitignored. It backs up to a separate private repo (`obsidian-brain`) on session close.
