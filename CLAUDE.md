# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Educational course repository demonstrating the evolution of data science coding across 7 eras. Each era solves the **same task** (load `data/marketing_campaign.csv`, compute metrics, create plots) using the tools and style of that era — from raw `csv` module to agentic AI.

## Commands

```bash
# Setup
uv venv .venv && uv pip install pandas matplotlib numpy jupyter

# Run any era script
uv run python3 era_1_notepad_terminal.py
uv run python3 era_3_ide.py

# Open the presentation notebook
uv run jupyter notebook evolution_of_coding.ipynb

# Regenerate the synthetic dataset (840 rows, seed=42)
uv run python3 generate_data.py

# Serve slides locally
python3 -m http.server 8000   # then open http://localhost:8000/slides.html
```

## Architecture

- **Era scripts** (`era_*.py`, `era_2_jupyter.ipynb`) — standalone, each self-contained. They all read from `data/marketing_campaign.csv` and write plots to `plots/`. The 7 eras are: Notepad+Terminal, Jupyter, IDE, GitHub Copilot, ChatGPT, Cursor/AI IDE, Claude Code.
- **`generate_data.py`** — creates the synthetic marketing CSV with seasonality, channel-specific behavior, and outliers. Deterministic via `random.seed(42)`.
- **`evolution_of_coding.ipynb`** — main presentation notebook tying all eras together.
- **`slides.html`** — reveal.js slide deck (CDN-loaded, no local dependencies). 7 slides in scroll view.
- **`prompts/`** — the AI prompts used to generate era 5, 6, and 7 code.

## Dataset

4 channels (Email, Social, Search, Display), 2 years (2023–2024). Columns: `date, channel, campaign_name, impressions, clicks, conversions, spend, revenue`.

## Environment

Python 3.12, managed with `uv`. Dependencies: pandas, matplotlib, numpy, jupyter.
