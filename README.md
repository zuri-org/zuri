# ZuriAI · Data against Rumours

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## What it does
Type any sentence (even offensive) and get an **evidence-based answer** using **Spanish National Statistics Institute (INE) 2023 crime data**.  
Goal: **debunk stereotypes about migrants** with **hard numbers**.

## Demo
https://zurai.org

## Stack
- Backend: FastAPI (Python)
- DB: DuckDB (delitos.db)
- Frontend: vanilla JS (responsive soon)
- AI: GPT-4o-mini (context, percentages)

## Quick start
```bash
git clone https://github.com/zuri-org/zuri.git
cd zuri
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8005

