
Copy

# BLS Dashboard
# Trenton Sedlacek ECON 8320

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="BLS Dashboard", layout="wide")

# LinkedIn badge function  <-- ADD THIS FUNCTION
def linkedin_badge():
    return """
    <div style="
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        background: white;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    ">
        <div style="
            width: 72px;
            height: 72px;
            border-radius: 50%;
            background: linear-gradient(135deg, #0077b5 0%, #00a0dc 100%);
            margin: 0 auto 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            color: white;
            font-weight: bold;
        ">TS</div>
        <h3 style="margin: 0 0 4px 0; font-size: 16px; color: #000;">Trenton Sedlacek</h3>
        <p style="margin: 0 0 8px 0; font-size: 12px; color: #666; line-height: 1.4;">
            M.S. Biostatistics Candidate<br>
            University of Nebraska Medical Center
        </p>
        <p style="margin: 0 0 12px 0; font-size: 11px; color: #888;">
            Nebraska DHHS | Statistics • R • Python
        </p>
        <a href="https://www.linkedin.com/in/trentonsedlacek" target="_blank" style="
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: #0077b5;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            text-decoration: none;
            font-weight: 600;
            font-size: 13px;
        ">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="white">
                <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
            </svg>
            View Profile
        </a>
    </div>
    """

# the 11 supersectors (they dont overlap so they add up to total nonfarm)
SECTORS = {
    "mining": {"emp": "mining_emp", "wage": "mining_wage", "label": "Mining and Logging"},
    "construction": {"emp": "construction_emp", "wage": "construction_wage", "label": "Construction"},
    "manufacturing": {"emp": "manufacturing_emp", "wage": "manufacturing_wage", "label": "Manufacturing"},
    "ttu": {"emp": "ttu_emp", "wage": "ttu_wage", "label": "Trade, Trans, Utilities"},
    "information": {"emp": "information_emp", "wage": "information_wage", "label": "Information"},
    "financial": {"emp": "financial_emp", "wage": "financial_wage", "label": "Financial Activities"},
    "profbusiness": {"emp": "profbusiness_emp", "wage": "profbusiness_wage", "label": "Professional/Business"},
    "eduhealth": {"emp": "eduhealth_emp", "wage": "eduhealth_wage", "label": "Education and Health"},
    "leisure": {"emp": "leisure_emp", "wage": "leisure_wage", "label": "Leisure and Hospitality"},
    "otherservices": {"emp": "otherservices_emp", "wage": "otherservices_wage", "label": "Other Services"},
    "government": {"emp": "government_emp", "wage": None, "label": "Government"},
}

# prettier names for the raw data table
COLUMN_LABELS = {
    "date": "Date",
    "total_nonfarm": "Total Nonfarm",
    "total_private": "Total Private",
    "unemployment_rate": "Unemployment Rate (%)",
    "lfpr": "Labor Force Participation (%)",
    "total_private_wage": "Avg Hourly Wage ($)",
    "mining_emp": "Mining Employment",
    "construction_emp": "Construction Employment",
    "manufacturing_emp": "Manufacturing Employment",
    "ttu_emp": "Trade/Trans/Util Employment",
    "information_emp": "Information Employment",
    "financial_emp": "Financial Employment",
    "profbusiness_emp": "Prof/Business Employment",
    "eduhealth_emp": "Education/Health Employment",
    "leisure_emp": "Leisure/Hospitality Employment",
    "otherservices_emp": "Other Services Employment",
    "government_emp": "Government Employment",
    "mining_wage": "Mining Wage ($)",
    "construction_wage": "Construction Wage ($)",
    "manufacturing_wage": "Manufacturing Wage ($)",
    "ttu_wage": "Trade/Trans/Util Wage ($)",
    "information_wage": "Information Wage ($)",
    "financial_wage": "Financial Wage ($)",
    "profbusiness_wage": "Prof/Business Wage ($)",
    "eduhealth_wage": "Education/Health Wage ($)",
    "leisure_wage": "Leisure/Hospitality Wage ($)",
    "otherservices_wage": "Other Services Wage ($)",
}

@st.cache_data
def load_data():
    path = "data/bls_data.csv"
    if not os.path.exists(path):
        return None
    df = pd.read_csv(path, parse_dates=["date"])
    return df.sort_values("date")

df = load_data()

if df is None or df.empty:
    st.error("No data found. Run collect_data.py first.")
    st.stop()

min_date = df["date"].min().date()
max_date = df["date"].max().date()

# sidebar stuff
with st.sidebar:
    # LinkedIn Badge at the top  <-- ADD THIS
    components.html(linkedin_badge(), height=250)
    st.markdown("---")
    
    st.header("Controls")
    
    date_range = st.slider(
        "Date Range",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="MMM YYYY"
    )

# date filter
mask = (df["date"].dt.date >= date_range[0]) & (df["date"].dt.date <= date_range[1])
filtered = df[mask].copy()
filtered_max = filtered["date"].max().date()

with st.sidebar:
    st.markdown("---")
    
    available = [k for k, v in SECTORS.items() if v["emp"] in filtered.columns]
    
    if available:
        select_all = st.checkbox("Select All Sectors", value=False)
        
        if select_all:
            default_sectors = available
        else:
            default_sectors = [s for s in ["construction", "manufacturing", "ttu", "leisure"] if s in available]
        
        selected = st.multiselect(
            "Select Sectors",
            options=available,
            default=default_sectors,
            format_func=lambda x: SECTORS[x]["label"]
        )
    else:
        selected = []
        st.warning("No sector data available")
    
    st.markdown("---")
    st.info(f"Latest: {filtered_max.strftime('%B %Y')}")
    st.info(f"Records: {len(filtered)}")


st.title("US Labor Statistics Dashboard")
st.caption("Data from Bureau of Labor Statistics. Updates monthly via GitHub Actions.")


def get_metric(col):
    if col not in filtered.columns:
        return None, None
    vals = filtered[col].dropna()
    if len(vals) < 2:
        return None, None
    return vals.iloc[-1], vals.iloc[-1] - vals.iloc[0]


# national totals
st.markdown("---")
st.subheader("National Totals")
c1, c2, c3, c4 = st.columns(4)

with c1:
    v, d = get_metric("total_nonfarm")
    st.metric("Total Nonfarm", f"{v:,.0f}K" if v else "N/A", f"{d:+,.0f}K" if d else None)

with c2:
    v, d = get_metric("unemployment_rate")
    st.metric("Unemployment", f"{v:.1f}%" if v else "N/A", f"{d:+.1f}%" if d else None, delta_color="inverse")

with c3:
    v, d = get_metric("lfpr")
    st.metric("Participation", f"{v:.1f}%" if v else "N/A", f"{d:+.1f}%" if d else None)

with c4:
    v, d = get_metric("total_private_wage")
    st.metric("Avg Hourly Wage", f"${v:.2f}" if v else "N/A", f"${d:+.2f}" if d else None)

# selected sectors
if selected:
    st.markdown("---")
    st.subheader(f"Selected Sectors ({len(selected)})")
    
    s1, s2 = st.columns(2)
    
    with s1:
        emp_cols = [SECTORS[s]["emp"] for s in selected if SECTORS[s]["emp"] in filtered.columns]
        if emp_cols and len(filtered) >= 2:
            total_emp = filtered[emp_cols].sum(axis=1)
            latest = total_emp.iloc[-1]
            change = latest - total_emp.iloc[0]
            st.metric("Combined Employment", f"{latest:,.0f}K", f"{change:+,.0f}K")
        else:
            st.metric("Combined Employment", "N/A")
    
    with s2:
        sectors_with_wages = [s for s in selected if SECTORS[s]["wage"] and SECTORS[s]["wage"] in filtered.columns]
        
        if sectors_with_wages and len(filtered) >= 2:
            wage_cols = [SECTORS[s]["wage"] for s in sectors_with_wages]
            emp_cols = [SECTORS[s]["emp"] for s in sectors_with_wages]
            
            # weighted avg so bigger sectors count more
            weighted_sum = sum(filtered[w] * filtered[e] for w, e in zip(wage_cols, emp_cols))
            total_emp = filtered[emp_cols].sum(axis=1)
            weighted_avg = weighted_sum / total_emp
            
            latest = weighted_avg.iloc[-1]
            change = latest - weighted_avg.iloc[0]
            st.metric("Avg Hourly Wage", f"${latest:.2f}", f"${change:+.2f}")
        else:
            st.metric("Avg Hourly Wage", "N/A")
    
    st.caption("Wage is weighted average by employment.")

# tabs
st.markdown("---")
tab1, tab2, tab3 = st.tabs(["Overview", "Sector Employment", "Sector Wages"])

with tab1:
    st.header("National Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if "total_nonfarm" in filtered.columns and filtered["total_nonfarm"].notna().any():
            fig = px.line(filtered, x="date", y="total_nonfarm", title="Total Nonfarm Employment")
            fig.update_layout(yaxis_title="Thousands", xaxis_title="")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data")
    
    with col2:
        if "unemployment_rate" in filtered.columns and filtered["unemployment_rate"].notna().any():
            fig = px.line(filtered, x="date", y="unemployment_rate", title="Unemployment Rate")
            fig.update_traces(line_color="red")
            fig.update_layout(yaxis_title="Percent", xaxis_title="")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data")
    
    col3, col4 = st.columns(2)
    
    with col3:
        if "lfpr" in filtered.columns and filtered["lfpr"].notna().any():
            fig = px.line(filtered, x="date", y="lfpr", title="Labor Force Participation")
            fig.update_traces(line_color="green")
            fig.update_layout(yaxis_title="Percent", xaxis_title="")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data")
    
    with col4:
        if "total_private_wage" in filtered.columns and filtered["total_private_wage"].notna().any():
            fig = px.line(filtered, x="date", y="total_private_wage", title="Avg Hourly Earnings")
            fig.update_traces(line_color="orange")
            fig.update_layout(yaxis_title="Dollars", xaxis_title="")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data")

with tab2:
    st.header("Sector Employment Comparison")
    
    if not selected:
        st.info("Pick some sectors from the sidebar")
    else:
        fig = go.Figure()
        for sec in selected:
            col = SECTORS[sec]["emp"]
            if col in filtered.columns:
                fig.add_trace(go.Scatter(
                    x=filtered["date"], y=filtered[col],
                    name=SECTORS[sec]["label"], mode="lines"
                ))
        
        fig.update_layout(
            title="Employment by Sector (Thousands)", height=500,
            yaxis=dict(rangemode="tozero", title="Thousands"),
            xaxis_title="", hovermode="x unified",
            legend=dict(orientation="h", y=-0.15)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # yoy growth
        if len(filtered) >= 12:
            st.subheader("Year over Year Growth")
            fig = go.Figure()
            
            for sec in selected:
                col = SECTORS[sec]["emp"]
                if col in filtered.columns:
                    growth = filtered[col].pct_change(12) * 100
                    fig.add_trace(go.Scatter(
                        x=filtered["date"], y=growth,
                        name=SECTORS[sec]["label"], mode="lines"
                    ))
            
            fig.update_layout(
                height=400, yaxis_title="Percent", xaxis_title="",
                hovermode="x unified", legend=dict(orientation="h", y=-0.15)
            )
            fig.add_hline(y=0, line_dash="dash", line_color="gray")
            st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Sector Wages Comparison")
    
    if not selected:
        st.info("Pick some sectors from the sidebar")
    else:
        with_wages = [s for s in selected if SECTORS[s]["wage"] and SECTORS[s]["wage"] in filtered.columns]
        without_wages = [s for s in selected if s not in with_wages]
        
        if without_wages:
            missing = ", ".join([SECTORS[s]["label"] for s in without_wages])
            st.warning(f"No wage data for: {missing}")
        
        if with_wages:
            fig = go.Figure()
            for sec in with_wages:
                col = SECTORS[sec]["wage"]
                fig.add_trace(go.Scatter(
                    x=filtered["date"], y=filtered[col],
                    name=SECTORS[sec]["label"], mode="lines"
                ))
            
            fig.update_layout(
                title="Avg Hourly Earnings by Sector", height=500,
                yaxis=dict(rangemode="tozero", title="Dollars"),
                xaxis_title="", hovermode="x unified",
                legend=dict(orientation="h", y=-0.15)
            )
            st.plotly_chart(fig, use_container_width=True)
            
            if len(filtered) >= 12:
                st.subheader("Year over Year Wage Growth")
                fig = go.Figure()
                
                for sec in with_wages:
                    col = SECTORS[sec]["wage"]
                    growth = filtered[col].pct_change(12) * 100
                    fig.add_trace(go.Scatter(
                        x=filtered["date"], y=growth,
                        name=SECTORS[sec]["label"], mode="lines"
                    ))
                
                fig.update_layout(
                    height=400, yaxis_title="Percent", xaxis_title="",
                    hovermode="x unified", legend=dict(orientation="h", y=-0.15)
                )
                fig.add_hline(y=0, line_dash="dash", line_color="gray")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("None of the selected sectors have wage data")

# raw data
st.markdown("---")
with st.expander("Raw Data"):
    display_df = filtered.rename(columns={c: COLUMN_LABELS.get(c, c) for c in filtered.columns})
    st.dataframe(display_df.sort_values("Date", ascending=False), use_container_width=True)
    st.download_button("Download CSV", filtered.to_csv(index=False), "bls_data.csv")

st.markdown("---")
st.caption("Data: U.S. Bureau of Labor Statistics | Trenton Sedlacek | ECON 8320")
