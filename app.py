import streamlit as st
from src.feature_engineering import create_features
from src.optimization import run_optimization

st.set_page_config(page_title="WattWise Dashboard", layout="wide")
st.title("⚡ Energy Flexibility Optimization Dashboard")


@st.cache_data
def get_base_data():
    return create_features()


@st.cache_data
def get_optimized_data(solar_factor, demand_factor):
    df = get_base_data().copy()
    df["solar"] = df["solar"] * solar_factor
    df["load"] = df["load"] * demand_factor
    df["renewable"] = df["solar"] + df["wind"]
    df["renewable_balance"] = df["renewable"] - df["load"]
    df["ratio"] = df["load"] / (df["renewable"] + 1)
    df["deficit"] = df["renewable_balance"] < 0
    df["surplus"] = df["renewable_balance"] > 0
    return run_optimization(df)


# ------------------------------------
# Sidebar Controls
# ------------------------------------
st.sidebar.header("Scenario Controls")

solar_factor = st.sidebar.slider("Solar Level", 0.0, 1.5, 1.0, 0.1)
demand_factor = st.sidebar.slider("Demand Level", 0.0, 1.5, 1.0, 0.1)

# ------------------------------------
# # Run optimization
# ------------------------------------

df = get_optimized_data(solar_factor, demand_factor)

# ------------------------------------
# Show Data
# ------------------------------------
st.subheader("📊 Energy Data Overview")
plot_df = df.resample("D").mean(numeric_only=True)
recent_df = df.tail(1000)
st.subheader("Energy Data Overview")
st.dataframe(df.tail(20))

# ------------------------------------
# Plot1: Load vs Supply
# ------------------------------------
st.subheader("⚡ Load vs Total Supply")
st.line_chart(plot_df[["load", "total_supply"]])
# ------------------------------------
# Plot2: Battery level
# ------------------------------------
st.subheader("🔋 Battery Level")
st.line_chart(plot_df["battery_level"])

# ------------------------------------
# Plot3: Balance(risk)
# ------------------------------------
st.subheader("⚠️ Energy Balance (Risk)")
st.line_chart(plot_df["balance"])

# ------------------------------------
# Plot4: Metrics
# ------------------------------------
st.subheader("📈 Key Metrics")

col1, col2, col3 = st.columns(3)
col1.metric("Avg Load", int(plot_df["load"].mean()))
col2.metric("Avg Renewable", int(plot_df["renewable"].mean()))
col3.metric("Avg Balance", int(plot_df["balance"].mean()))
