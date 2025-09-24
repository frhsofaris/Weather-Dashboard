# Real-Time Weather & Air-Quality Dashboard
Fetches live hourly temperature data and PM2.5 air-quality readings for Kuala Lumpur,
calculates a Comfort Index, and outputs:
* A CSV of hourly data
* A line chart (PNG) of Temperature vs Comfort Index

## Requirements
- Python 3.10+
- `requests`, `pandas`, `matplotlib`

Install packages:
```bash
pip install requests pandas matplotlib