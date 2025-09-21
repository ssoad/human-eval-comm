# HumanEvalComm Leaderboard Web App

This Flask app provides an interactive leaderboard for HumanEvalComm benchmark results.

## Features
- Reads leaderboard CSV from `Benchmark/HumanEvalComm_v2.csv`
- Displays sortable/filterable table of results
- Filter by model name
- Modern Bootstrap UI

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   python app.py
   ```
3. Open your browser at [http://localhost:5000](http://localhost:5000)

## Customization
- Update the CSV path in `app.py` if your leaderboard file is elsewhere.
- Extend the UI in `templates/index.html` for more filters or charts.
