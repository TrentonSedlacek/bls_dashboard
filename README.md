# BLS Dashboard

Trenton Sedlacek
Live: https://blsdashboard-trenton.streamlit.app/

## About

Interactive dashboard showing US labor market data from the Bureau of Labor Statistics. Automatically updates monthly.

## Features

Shows national totals for employment, unemployment, participation, and wages. Also breaks down employment and wages by the 11 BLS supersectors. You can filter by date range and select which sectors to compare.

## Data

Pulls from the BLS API:
- Total Nonfarm Employment
- Unemployment Rate  
- Labor Force Participation
- Average Hourly Earnings
- Employment and wages for all 11 supersectors

## Files

- `.github/workflows/update_data.yml` runs the monthly update
- `collect_data.py` pulls from BLS
- `data/bls_data.csv` is the most recentdata
- `app.py` builds the dashboard


## Run locally

```
pip install -r requirements.txt
python collect_data.py
streamlit run app.py
```

## Source

https://www.bls.gov/
