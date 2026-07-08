import streamlit as st
import pandas as pd
import plotly.express as px
from prophet import Prophet
from ai_functions import ai_explain
from ui_components import create_chart_container

def render_forecast(df, num_cols):
    """Render the Forecast page"""
    create_chart_container("AI Forecast", "ML-powered sales prediction", icon="🔮")
    forecast_fig = None

    metric_option = st.selectbox("Select Metric", ["Sales", "Profit"])
    choice = st.selectbox("Forecast Range", ["7 Days", "30 Days", "6 Months", "1 Year"])

    days_map = {"7 Days":7,"30 Days":30,"6 Months":180,"1 Year":365}
    periods = days_map[choice]

    value_col = num_cols[0] if metric_option=="Sales" else (num_cols[1] if len(num_cols)>1 else num_cols[0])

    date_cols = [c for c in df.columns if "date" in c]

    if date_cols:
        date_col = date_cols[0]
        ts = df[[date_col, value_col]].copy()
        ts[date_col] = pd.to_datetime(ts[date_col], errors="coerce")
        ts[value_col] = pd.to_numeric(ts[value_col], errors="coerce")
        ts = ts.dropna()
        ts = ts.groupby(date_col, as_index=False)[value_col].sum()
        ts.columns = ["ds", "y"]

        if len(ts) >= 10:
            model = Prophet()
            model.fit(ts)

            future = model.make_future_dataframe(periods=periods)
            forecast = model.predict(future)

            forecast_fig = px.line(forecast, x="ds", y="yhat")
            st.plotly_chart(forecast_fig)

            if st.button("Explain Forecast", key="forecast_btn_page"):
                st.info(ai_explain(f"{metric_option} forecast", forecast.tail(20).to_string()))
