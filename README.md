# The Evolution of Coding for Data Scientists

A 30–45 minute course that tells the story of how data science coding has transformed over the past ~8 years — from Notepad and a terminal to AI-powered agentic workflows.

**The twist:** every era solves the **exact same task** — load a marketing CSV, compute metrics, and create plots — so you can see how the tools changed while the problem stayed the same.

## The 7 Eras

| Era | Years | File | What Changed |
|-----|-------|------|--------------|
| 1. Notepad + Terminal | ~2010–2015 | `era_1_notepad_terminal.py` | Raw Python, `csv` module, manual everything (~160 lines) |
| 2. Jupyter Notebooks | 2014–present | `era_2_jupyter.ipynb` | Interactive cells, inline plots, exploratory workflow (~50 lines) |
| 3. IDE (VS Code / PyCharm) | 2016–present | `era_3_ide.py` | Autocomplete, linting, type hints, structured code |
| 4. Stack Overflow | 2008–2023 | `era_4_stackoverflow.py` | Copy-paste-modify from SO answers (comments show the sources) |
| 5. ChatGPT | Late 2022–present | `era_5_chatgpt.py` | Describe what you want, get working code in 15 seconds |
| 6. Cursor / AI IDE | 2023–present | `era_6_cursor.py` | AI embedded in the editor — Tab to accept, Cmd+K to refine |
| 7. Claude Code | 2025–present | Live demo | Natural language → working code, fully agentic |

## Quick Start

```bash
# Clone
git clone https://github.com/stamtron/vibe-coding.git
cd vibe-coding

# Set up environment
uv venv .venv && uv pip install pandas matplotlib numpy

# Run any era
uv run python3 era_1_notepad_terminal.py
uv run python3 era_3_ide.py
uv run python3 era_5_chatgpt.py
# ... etc

# Open the presentation notebook
uv run jupyter notebook evolution_of_coding.ipynb
```

## What's Inside

```
vibe-coding/
├── data/
│   └── marketing_campaign.csv      # 840 rows of synthetic marketing data
├── plots/                          # All generated charts (17 plots)
├── era_1_notepad_terminal.py       # Era 1: raw csv module + matplotlib
├── era_2_jupyter.ipynb             # Era 2: interactive notebook
├── era_3_ide.py                    # Era 3: structured pandas code
├── era_4_stackoverflow.py          # Era 4: SO-assembled code
├── era_5_chatgpt.py                # Era 5: ChatGPT-generated script
├── era_6_cursor.py                 # Era 6: AI IDE style
├── evolution_of_coding.ipynb       # Main presentation notebook
├── slides.html                     # 6-slide reveal.js deck
└── generate_data.py                # Script that created the CSV
```

## The Dataset

Synthetic marketing campaign data with realistic patterns:

- **840 rows** across 2 years (2023–2024)
- **4 channels:** Email, Social, Search, Display
- **Columns:** date, channel, campaign_name, impressions, clicks, conversions, spend, revenue
- Built-in seasonality, channel-specific behavior, and outliers

## Presenting

Two options for delivery:

1. **Notebook** — Open `evolution_of_coding.ipynb` and walk through each era with runnable code and inline plots
2. **Slides** — Open `slides.html` in a browser (see below) and scroll through, or use arrow keys to navigate

### Opening the slides

```bash
# macOS
open slides.html

# Linux
xdg-open slides.html

# Windows
start slides.html

# Or serve locally (avoids any CORS issues with reveal.js CDN)
python3 -m http.server 8000
# then open http://localhost:8000/slides.html
```

Era 7 (Claude Code) is meant to be done **live** — open Claude Code and ask it to analyze the marketing CSV in real time.

## Historical Context

Eras overlap — each new tool added to the toolkit rather than replacing the last.

| Era | Key Milestone |
|-----|---------------|
| Notepad + Terminal | The pre-tooling era — raw Python, `csv` module, `print()` debugging |
| Jupyter Notebooks | Spun off from IPython in **2014**; 2.5M notebooks on GitHub by 2018; *Nature* called it a cornerstone of scientific computing |
| IDE (VS Code / PyCharm) | VS Code launched 2015, became the **#1 IDE in the 2018** Stack Overflow Developer Survey |
| Stack Overflow | Launched **2008**, peaked at 200K questions/month in 2014; traffic dropped 78% between 2024–2025 after AI tools arrived |
| ChatGPT | Launched **November 30, 2022** — changed coding workflows overnight |
| Cursor / AI IDE | Founded **2022**, hit $100M ARR by January 2025; AI moves inside the editor |
| Claude Code | Preview **February 2025**, GA **May 2025** — fully agentic, reads/writes/runs code end-to-end |

## Key Takeaway

> The skill shift: from **syntax memorization** to **problem decomposition**.
> What hasn't changed: you still need to understand the data and ask the right questions.

## The New Bottleneck

> *"The role of the engineer is fundamentally shifting — from a technical specialist who writes code from scratch to an AI-enabled strategic problem solver."* — **Andrew Ng**

Because AI automates routine coding, engineering velocity has skyrocketed. The bottleneck is no longer *"Can we build this?"* but *"Should we build this?"* — product direction and decision-making are now what separates great engineers from the rest.

## License

MIT
