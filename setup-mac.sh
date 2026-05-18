#!/bin/bash

# ============================================================
#  Research Assistant Setup Script — macOS
#
#  What this installs:
#    Homebrew · Git · VS Code · Claude Code extension
#    Python 3.11 · NotebookLM CLI · Playwright Chromium
#    Obsidian · GitHub CLI
#
#  Usage:
#    bash setup-mac.sh
# ============================================================

set -eo pipefail

# ---- Colors & helpers ----------------------------------------
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

step()    { echo -e "\n${BLUE}${BOLD}[$1]${NC} ${BOLD}$2${NC}"; }
ok()      { echo -e "  ${GREEN}✓${NC}  $1"; }
warn()    { echo -e "  ${YELLOW}!${NC}  $1"; }
info()    { echo -e "  ${BLUE}→${NC}  $1"; }
pause()   { echo ""; read -rp "  Press Enter to continue..."; }
divider() { echo -e "\n${DIM}────────────────────────────────────────────────────${NC}"; }

TOTAL_STEPS=12

# ==============================================================
# WELCOME
# ==============================================================
clear
echo ""
echo -e "${BOLD}${BLUE}"
echo -e "  ╔═══════════════════════════════════════════════════╗"
echo -e "  ║                                                   ║"
echo -e "  ║        Claude Code — Mac Setup                    ║"
echo -e "  ║                  for Thiago                       ║"
echo -e "  ║                     by Tomas                      ║"
echo -e "  ║                                                   ║"
echo -e "  ╚═══════════════════════════════════════════════════╝"
echo -e "${NC}"
echo -e "  This script sets up your Mac with everything needed"
echo -e "  to run the ${BOLD}Research Assistant${NC} — an AI-powered tool"
echo -e "  that researches topics and organises your knowledge."
echo ""
echo -e "  ${BOLD}What will be installed:${NC}"
echo -e "  ${DIM}·${NC} Homebrew, Git, GitHub CLI"
echo -e "  ${DIM}·${NC} Visual Studio Code + Claude Code extension"
echo -e "  ${DIM}·${NC} Python 3.11, NotebookLM CLI, Chromium"
echo -e "  ${DIM}·${NC} Obsidian"
echo ""
echo -e "  ${YELLOW}Heads up:${NC} You may be asked for your Mac password."
echo -e "  ${YELLOW}Heads up:${NC} Two steps will open your browser to sign in."
echo ""
echo -e "  Estimated time: ${BOLD}10–25 minutes${NC}."
echo ""
echo -e "  ${DIM}────────────────────────────────────────────────────${NC}"
echo ""
read -rp "  Ready to start? [y/N] " CONFIRM
echo ""
if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
    echo -e "  Setup cancelled. Run this script again whenever you're ready."
    echo ""
    exit 0
fi

# ==============================================================
# PRE-FLIGHT — XCODE COMMAND LINE TOOLS
# ==============================================================
# Homebrew, git, and most build steps require Apple's Command Line
# Tools. On a fresh Mac this triggers a GUI installer dialog.
if ! xcode-select -p &>/dev/null; then
    echo -e "\n${BLUE}${BOLD}[pre-flight]${NC} ${BOLD}Xcode Command Line Tools${NC}"
    info "macOS needs Command Line Tools (compiler + git) before we continue."
    info "A system dialog will open — click ${BOLD}Install${NC} and accept the license."
    xcode-select --install &>/dev/null || true
    echo ""
    info "Waiting for the install to finish (usually 5–10 minutes)..."
    until xcode-select -p &>/dev/null; do
        sleep 10
    done
    ok "Command Line Tools installed"
fi

# ==============================================================
# STEP 1 — HOMEBREW
# ==============================================================
step "1/$TOTAL_STEPS" "Homebrew (package manager)"

if command -v brew &>/dev/null; then
    ok "Homebrew is already installed — skipping"
else
    info "Installing Homebrew. You may be asked for your Mac password..."
    echo ""
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # Apple Silicon: add brew to PATH for this session and future shells
    if [[ -f "/opt/homebrew/bin/brew" ]]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
        grep -qxF 'eval "$(/opt/homebrew/bin/brew shellenv)"' "$HOME/.zprofile" 2>/dev/null \
            || echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> "$HOME/.zprofile"
    fi

    ok "Homebrew installed"
fi

# ==============================================================
# STEP 2 — GIT
# ==============================================================
step "2/$TOTAL_STEPS" "Git (version control)"

if command -v git &>/dev/null; then
    ok "Git is already installed — $(git --version)"
else
    info "Installing Git..."
    brew install git
    ok "Git installed"
fi

echo ""
echo -e "  Git needs your name and email to label your work."
echo -e "  ${DIM}(Use the same email as your GitHub account.)${NC}"
echo ""
read -rp "  Your full name: " GIT_NAME
read -rp "  Your email:     " GIT_EMAIL
git config --global user.name  "$GIT_NAME"
git config --global user.email "$GIT_EMAIL"
ok "Git identity saved"

# ==============================================================
# STEP 3 — VISUAL STUDIO CODE
# ==============================================================
step "3/$TOTAL_STEPS" "Visual Studio Code"

CODE_BIN=""

if command -v code &>/dev/null; then
    CODE_BIN="code"
    ok "VS Code is already installed — skipping"
elif [[ -d "/Applications/Visual Studio Code.app" ]]; then
    CODE_BIN="/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"
    ok "VS Code is already installed (not in PATH) — skipping"
else
    info "Installing VS Code..."
    brew install --cask visual-studio-code
    CODE_BIN="code"
    ok "VS Code installed"
fi

# Ensure 'code' CLI is reachable for the rest of this script
if [[ "$CODE_BIN" != "code" ]]; then
    export PATH="$PATH:/Applications/Visual Studio Code.app/Contents/Resources/app/bin"
    CODE_BIN="code"
fi

# ==============================================================
# STEP 4 — CLAUDE CODE EXTENSION
# ==============================================================
step "4/$TOTAL_STEPS" "Claude Code (VS Code extension)"

if "$CODE_BIN" --list-extensions 2>/dev/null | grep -qi "anthropic.claude-code"; then
    ok "Claude Code extension is already installed — skipping"
else
    info "Installing Claude Code extension..."
    "$CODE_BIN" --install-extension anthropic.claude-code
    ok "Claude Code extension installed"
fi

# ==============================================================
# STEP 5 — PYTHON 3.11 + pipx
# ==============================================================
step "5/$TOTAL_STEPS" "Python 3.11 + pipx"

if command -v python3.11 &>/dev/null; then
    ok "Python 3.11 is already installed — $(python3.11 --version)"
else
    info "Installing Python 3.11..."
    brew install python@3.11
    ok "Python 3.11 installed"
fi

if command -v pipx &>/dev/null; then
    ok "pipx is already installed"
else
    info "Installing pipx (isolated installer for Python CLI tools)..."
    brew install pipx
    ok "pipx installed"
fi

# Make pipx's user bin available now and in future shells
pipx ensurepath >/dev/null 2>&1 || true
export PATH="$HOME/.local/bin:$PATH"

# ==============================================================
# STEP 6 — NOTEBOOKLM CLI
# ==============================================================
step "6/$TOTAL_STEPS" "NotebookLM CLI"

if command -v notebooklm &>/dev/null; then
    ok "NotebookLM CLI is already installed — skipping"
else
    info "Installing NotebookLM CLI (isolated via pipx)..."
    pipx install "notebooklm-py[browser]" --python python3.11
    ok "NotebookLM CLI installed"
fi

# ==============================================================
# STEP 7 — PLAYWRIGHT CHROMIUM
# ==============================================================
step "7/$TOTAL_STEPS" "Chromium (browser automation)"

info "Installing Chromium for NotebookLM..."
NOTEBOOKLM_VENV_PY="$HOME/.local/pipx/venvs/notebooklm-py/bin/python"
if [[ -x "$NOTEBOOKLM_VENV_PY" ]]; then
    "$NOTEBOOKLM_VENV_PY" -m playwright install chromium
    ok "Chromium installed"
else
    warn "Could not find NotebookLM's Python environment."
    warn "Re-run this script, or run manually:"
    warn "  ~/.local/pipx/venvs/notebooklm-py/bin/python -m playwright install chromium"
fi

# ==============================================================
# STEP 8 — OBSIDIAN
# ==============================================================
step "8/$TOTAL_STEPS" "Obsidian (knowledge base app)"

if [[ -d "/Applications/Obsidian.app" ]] || brew list --cask obsidian &>/dev/null 2>&1; then
    ok "Obsidian is already installed — skipping"
else
    info "Installing Obsidian..."
    brew install --cask obsidian
    ok "Obsidian installed"
fi

# ==============================================================
# STEP 9 — GITHUB CLI
# ==============================================================
step "9/$TOTAL_STEPS" "GitHub CLI"

if command -v gh &>/dev/null; then
    ok "GitHub CLI is already installed — $(gh --version | head -1)"
else
    info "Installing GitHub CLI..."
    brew install gh
    ok "GitHub CLI installed"
fi

# ==============================================================
# STEP 10 — GITHUB SIGN-IN
# ==============================================================
step "10/$TOTAL_STEPS" "GitHub — sign in"

if gh auth status &>/dev/null 2>&1; then
    ok "Already signed in to GitHub — skipping"
else
    echo ""
    echo -e "  Your browser will open so you can sign in to GitHub."
    echo -e "  Just log in and click ${BOLD}Authorize${NC} — then come back here."
    echo ""
    pause
    if gh auth login --web --hostname github.com --git-protocol https; then
        gh auth setup-git 2>/dev/null || true
        ok "GitHub sign-in complete"
    else
        warn "GitHub sign-in was skipped or failed."
        warn "Run 'gh auth login' in your terminal later to finish this step."
    fi
fi

# ==============================================================
# STEP 11 — NOTEBOOKLM GOOGLE SIGN-IN
# ==============================================================
step "11/$TOTAL_STEPS" "NotebookLM — sign in with Google"

echo ""
echo -e "  Your browser will open for a Google sign-in."
echo -e "  Log in with the Google account you want to use for research."
echo ""
pause
if notebooklm login; then
    ok "NotebookLM sign-in complete"
else
    warn "NotebookLM sign-in was skipped or failed."
    warn "Run 'notebooklm login' in your terminal later to finish this step."
fi

# ==============================================================
# STEP 12 — NOTEBOOKLM SKILL
# ==============================================================
step "12/$TOTAL_STEPS" "NotebookLM skill (Claude Code integration)"

info "Installing NotebookLM skill..."
if notebooklm skill install; then
    ok "NotebookLM skill installed"
else
    warn "Skill install failed — run 'notebooklm skill install' in your terminal later."
fi

# ==============================================================
# DONE
# ==============================================================
divider
echo ""
echo -e "  ${GREEN}${BOLD}Installation complete!${NC}"
echo ""
echo -e "  ${BOLD}Two quick manual steps remaining:${NC}"
echo ""
echo -e "  ${BOLD}1.  Sign in to Claude Code${NC}"
echo -e "      a. Open VS Code  ${DIM}(Applications folder)${NC}"
echo -e "      b. Click the ${BOLD}Claude icon${NC} in the left sidebar"
echo -e "      c. Click Sign In and log in with your Claude account"
echo ""
echo -e "  ${BOLD}2.  Open Obsidian${NC}"
echo -e "      a. Open Obsidian  ${DIM}(Applications folder)${NC}"
echo -e "      b. Create a new vault when prompted"
echo -e "      c. Name it anything you like — e.g. ${DIM}'Brain'${NC} or ${DIM}'Notes'${NC}"
echo ""
divider
echo ""
echo -e "  ${BOLD}What was installed:${NC}"
echo ""
echo -e "  ${GREEN}✓${NC}  Homebrew"
echo -e "  ${GREEN}✓${NC}  Git  ${DIM}($(git --version 2>/dev/null))${NC}"
echo -e "  ${GREEN}✓${NC}  Visual Studio Code"
echo -e "  ${GREEN}✓${NC}  Claude Code extension"
echo -e "  ${GREEN}✓${NC}  Python 3.11  ${DIM}($(python3.11 --version 2>/dev/null))${NC}"
echo -e "  ${GREEN}✓${NC}  NotebookLM CLI"
echo -e "  ${GREEN}✓${NC}  Chromium"
echo -e "  ${GREEN}✓${NC}  Obsidian"
echo -e "  ${GREEN}✓${NC}  GitHub CLI"
echo ""
echo -e "${BOLD}${GREEN}"
echo -e "  ╔═══════════════════════════════════════════════════╗"
echo -e "  ║                                                   ║"
echo -e "  ║                 ALL SET, THIAGO!                  ║"
echo -e "  ║                See you next class                 ║"
echo -e "  ║                                                   ║"
echo -e "  ╚═══════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""
