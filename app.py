import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Website Traffic & Performance Dashboard", layout="wide")

st.title("🌐 Website Traffic & Performance Analysis Dashboard")

# 1. ACTUAL DATA LOAD (Aapki file ka name yahan dalen)
@st.cache_data
def load_actual_data():
    # Example: Agar aapne CSV save kiya hai toh usika path dein
    # df = pd.read_csv("website_traffic_data.csv")
    
    # Temporarily mapping your exact Jupyter layout columns for clean run
    # Is block ko hata kar aap direct apni file read kar sakte hain
    import numpy as np
    dates = pd.date_range(start='2026-07-01', periods=100, freq='h')
    channels = ['Direct', 'Organic Search', 'Organic Social', 'Referral', 'Paid Ads']
    rows = [[np.random.choice(channels), dt, np.random.randint(50, 250), np.random.randint(60, 300), 
             np.random.uniform(20, 150), np.random.uniform(0.3, 0.7), np.random.randint(100, 1500)] for dt in dates]
    
    return pd.DataFrame(rows, columns=['Channel group', 'Datehours', 'Users', 'Sessions', 'Average engagement time per session', 'Engagement rate', 'Event count'])

df = load_actual_data()
df['Datehours'] = pd.to_datetime(df['Datehours'])
df['Date'] = df['Datehours'].dt.date

# 2. SIDEBAR FILTER
st.sidebar.header("Filter Options")
all_channels = df['Channel group'].unique().tolist()
selected_channels = st.sidebar.multiselect("Select Traffic Channels:", options=all_channels, default=all_channels)
filtered_df = df[df['Channel group'].isin(selected_channels)]

# 3. KPI METRICS
st.subheader("📊 Key Performance Indicators")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Sessions", f"{filtered_df['Sessions'].sum():,}")
with col2:
    st.metric("Unique Users", f"{filtered_df['Users'].sum():,}")
with col3:
    # Converting engagement rate to simulated bounce rate for slide alignment
    avg_bounce = (1 - filtered_df['Engagement rate'].mean()) * 100
    st.metric("Avg. Bounce Rate", f"{avg_bounce:.2f}%")
with col4:
    avg_duration = filtered_df['Average engagement time per session'].mean() / 60
    st.metric("Avg. Duration (Min)", f"{avg_duration:.2f}m")
with col5:
    total_events = filtered_df['Event count'].sum()
    st.metric("Goal Conversions (Events)", f"{total_events:,}")

st.markdown("---")

# 4. CHARTS
chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    st.subheader("🧩 Traffic Share by Channel Group")
    fig_pie = px.pie(filtered_df, names='Channel group', values='Sessions', hole=0.3)
    st.plotly_chart(fig_pie, use_container_width=True)

with chart_col2:
    st.subheader("📈 Website Traffic Peak Trends")
    trend_df = filtered_df.groupby('Date')['Sessions'].sum().reset_index()
    fig_trend = px.line(trend_df, x='Date', y='Sessions', markers=True)
    st.plotly_chart(fig_trend, use_container_width=True)