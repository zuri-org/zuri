# ZuriAI · Data against Rumours

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

**ZuriAI does not debate opinions: it provides facts.**  
Against rumours, data. Against prejudice, context.  
**The data kills the narrative.**

---

## What it does

Type any sentence — even offensive or biased — and get an **evidence-based response**
using official **Spanish National Statistics Institute (INE, 2023)** crime data.

ZuriAI is designed to **detect stereotypes about migrants** and respond with
clear, contextualized statistics instead of opinions.

---

## Why it exists

Rumours spread fast. Data doesn’t.

ZuriAI aims to make public data accessible, understandable and useful
in everyday conversations where misinformation and stereotypes appear.

---

## Demo

https://zurai.org

---

## Stack

- **Backend:** FastAPI (Python)
- **Database:** DuckDB (`delitos.db`)
- **Frontend:** Vanilla JS
- **AI:** GPT-4o-mini (context, explanation, percentages)

---

## Quick start

```bash
git clone https://github.com/zuri-org/zuri.git
cd zuri
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8005

