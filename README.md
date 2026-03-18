# research-idea-sindy

An AI-assisted research tool. Add academic papers to NotebookLM, ask questions about them, and Claude writes structured notes and summaries into an Obsidian vault — automatically organized by topic and backed up to git.

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

At the end of each session, Claude will automatically write a structured note to your Obsidian vault and back it up to git.

---

## What gets saved where

| Content | Location |
|---|---|
| Per-topic notes (tracks) | `~/obsidian-brain/research-idea-sindy/tracks/` |
| Session summaries | `~/obsidian-brain/research-idea-sindy/sessions/` |
| NotebookLM notebooks | Google's servers (via your account) |
| Repo code and workflows | `~/Dev/projects/research-idea-sindy/` (this repo) |

The Obsidian vault content is local-only and gitignored from the project repo. It backs up to a separate private repo (`obsidian-brain`) automatically on session close.
