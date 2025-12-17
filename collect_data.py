# collect_data.py
# Trenton Sedlacek ECON 8320
# grabs data from BLS API

import requests
import json
import pandas as pd
from datetime import datetime
import os

API_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
OUTPUT_FILE = "data/bls_data.csv"

# series IDs from BLS
# employment ones end in 01, wages end in 03
# these are the 11 supersectors which add up to total nonfarm without double counting
SERIES = {
    # main stuff
    "CES0000000001": "total_nonfarm",
    "CES0500000001": "total_private",
    "LNS14000000": "unemployment_rate",
    "LNS11300000": "lfpr",
    
    # employment for each sector
    "CES1000000001": "mining_emp",
    "CES2000000001": "construction_emp",
    "CES3000000001": "manufacturing_emp",
    "CES4000000001": "ttu_emp",
    "CES5000000001": "information_emp",
    "CES5500000001": "financial_emp",
    "CES6000000001": "profbusiness_emp",
    "CES6500000001": "eduhealth_emp",
    "CES7000000001": "leisure_emp",
    "CES8000000001": "otherservices_emp",
    "CES9000000001": "government_emp",
    
    # wages for each sector (govt doesnt have this)
    "CES0500000003": "total_private_wage",
    "CES1000000003": "mining_wage",
    "CES2000000003": "construction_wage",
    "CES3000000003": "manufacturing_wage",
    "CES4000000003": "ttu_wage",
    "CES5000000003": "information_wage",
    "CES5500000003": "financial_wage",
    "CES6000000003": "profbusiness_wage",
    "CES6500000003": "eduhealth_wage",
    "CES7000000003": "leisure_wage",
    "CES8000000003": "otherservices_wage",
}


def fetch_from_bls(series_list, start_year, end_year, api_key=None):
    payload = {
        "seriesid": series_list,
        "startyear": str(start_year),
        "endyear": str(end_year),
    }
    
    if api_key:
        payload["registrationkey"] = api_key
    
    headers = {"Content-type": "application/json"}
    resp = requests.post(API_URL, data=json.dumps(payload), headers=headers)
    
    if resp.status_code != 200:
        raise Exception(f"API returned {resp.status_code}")
    
    data = resp.json()
    if data.get("status") != "REQUEST_SUCCEEDED":
        raise Exception(f"BLS error: {data.get('message')}")
    
    return data


def parse_response(response):
    rows = []
    
    for series in response.get("Results", {}).get("series", []):
        series_id = series.get("seriesID")
        col_name = SERIES.get(series_id, series_id)
        
        for item in series.get("data", []):
            period = item.get("period", "")
            
            # M01 thru M12 are monthly, M13 is annual avg so skip it
            if not period.startswith("M") or period == "M13":
                continue
            
            year = item.get("year")
            month = int(period.replace("M", ""))
            
            try:
                value = float(item.get("value"))
                rows.append({
                    "date": f"{year}-{month:02d}-01",
                    "column": col_name,
                    "value": value
                })
            except (ValueError, TypeError):
                pass
    
    if not rows:
        return pd.DataFrame()
    
    # pivot to wide format
    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    df = df.pivot_table(index="date", columns="column", values="value", aggfunc="last")
    df = df.reset_index().sort_values("date")
    
    return df


def main():
    api_key = os.environ.get("BLS_API_KEY")
    if api_key:
        print("Found API key")
    else:
        print("No API key, using public API")
    
    os.makedirs("data", exist_ok=True)
    
    current_year = datetime.now().year
    start_year = current_year - 9
    
    print(f"Pulling data from {start_year} to {current_year}...")
    
    # public API caps at 20 series per request
    all_series = list(SERIES.keys())
    chunks = [all_series[i:i+20] for i in range(0, len(all_series), 20)]
    
    dataframes = []
    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i+1}/{len(chunks)}...")
        response = fetch_from_bls(chunk, start_year, current_year, api_key)
        df = parse_response(response)
        if not df.empty:
            dataframes.append(df)
    
    if not dataframes:
        print("No data collected!")
        return
    
    # merge chunks together
    result = dataframes[0]
    for df in dataframes[1:]:
        result = result.merge(df, on="date", how="outer")
    
    result = result.sort_values("date").reset_index(drop=True)
    result.to_csv(OUTPUT_FILE, index=False)
    
    print(f"\nSaved {len(result)} rows to {OUTPUT_FILE}")
    print(f"Columns: {len(result.columns)}")


if __name__ == "__main__":
    main()
