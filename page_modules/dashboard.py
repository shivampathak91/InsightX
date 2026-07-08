import streamlit as st
import pandas as pd
import plotly.express as px
from ai_functions import ai_explain, generate_executive_summary
from ui_components import create_premium_card, create_chart_container

def render_dashboard(df, num_cols, cat_cols):
    """Render the Dashboard page"""
    # KPI Cards
    st.markdown("---")
    st.subheader("📈 Key Performance Indicators")

    total_sales = df[num_cols[0]].sum()
    total_profit = df[num_cols[1]].sum() if len(num_cols) > 1 else 0
    total_records = len(df)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(79, 70, 229, 0.15) 0%, rgba(124, 58, 237, 0.1) 100%);
            border: 1px solid rgba(79, 70, 229, 0.3);
            border-radius: 16px;
            padding: 24px;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        ">
            <div style="font-size: 32px; margin-bottom: 8px;">💰</div>
            <div style="color: #9CA3AF; font-size: 14px; margin-bottom: 8px;">Total Sales</div>
            <div style="color: #F9FAFB; font-size: 28px; font-weight: 700;">""" + f"{total_sales:,.2f}" + """</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(5, 150, 105, 0.1) 100%);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 16px;
            padding: 24px;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        ">
            <div style="font-size: 32px; margin-bottom: 8px;">📊</div>
            <div style="color: #9CA3AF; font-size: 14px; margin-bottom: 8px;">Total Profit</div>
            <div style="color: #F9FAFB; font-size: 28px; font-weight: 700;">""" + f"{total_profit:,.2f}" + """</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(217, 119, 6, 0.1) 100%);
            border: 1px solid rgba(245, 158, 11, 0.3);
            border-radius: 16px;
            padding: 24px;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        ">
            <div style="font-size: 32px; margin-bottom: 8px;">📋</div>
            <div style="color: #9CA3AF; font-size: 14px; margin-bottom: 8px;">Total Records</div>
            <div style="color: #F9FAFB; font-size: 28px; font-weight: 700;">""" + f"{total_records:,}" + """</div>
        </div>
        """, unsafe_allow_html=True)

    # AI Executive Summary
    st.markdown("---")
    with st.expander("🎯 AI Executive Summary", expanded=True):
        with st.spinner("Generating AI-powered executive summary..."):
            summary = generate_executive_summary(df, num_cols, cat_cols)
            create_premium_card("Business Intelligence Summary", summary.replace('\n', '<br/>'), icon="🧠", color="purple")

    # Charts Grid Layout
    col1, col2 = st.columns(2)
    
    with col1:
        # Regional Sales Pie Chart
        create_chart_container("Regional Sales", "Sales distribution by region", icon="🌍")
        region_fig = None

        if "region" in df.columns and len(num_cols) > 0:
            region_data = df.groupby("region")[num_cols[0]].sum().reset_index()

            region_fig = px.pie(
                region_data,
                names="region",
                values=num_cols[0],
                height=400
            )

            st.plotly_chart(region_fig, use_container_width=True)

            if st.button("Explain Regional Sales", key="region_btn"):
                st.info(
                    ai_explain(
                        "Pie chart showing regional sales distribution",
                        region_data.to_string()
                    )
                )
    
    with col2:
        # Customer Segments Pie Chart
        create_chart_container("Customer Segments", "Revenue by customer segment", icon="👥")
        segment_fig = None

        if "segment" in df.columns:
            seg_data = df.groupby("segment")[num_cols[0]].sum().reset_index()

            segment_fig = px.pie(seg_data, names="segment", values=num_cols[0], height=400)
            st.plotly_chart(segment_fig, use_container_width=True)

            if st.button("Explain Segment Distribution", key="segpie_btn"):
                st.info(ai_explain("Customer segment revenue share", seg_data.to_string()))
    
    # Second Row
    col3, col4 = st.columns(2)
    
    with col3:
        # Monthly Sales Chart
        create_chart_container("Monthly Sales", "Sales trend over time", icon="📅")
        monthly_fig = None

        date_cols = [col for col in df.columns if "date" in col.lower()]

        if len(date_cols) == 0:
            st.warning("No date column found for monthly analysis")
        else:
            date_col = date_cols[0]

            df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

            monthly = df.groupby(df[date_col].dt.to_period("M"))[num_cols[0]].sum().reset_index()
            monthly[date_col] = monthly[date_col].astype(str)

            monthly_fig = px.bar(monthly, x=date_col, y=num_cols[0], title="Monthly Sales")

            st.plotly_chart(monthly_fig, use_container_width=True)

            if st.button("Explain Monthly", key="monthly_btn"):
                st.info(ai_explain("Monthly sales trend", monthly.to_string()))
    
    with col4:
        # Shipping Efficiency Chart
        create_chart_container("Shipping Efficiency", "Average shipping time by mode", icon="🚚")
        ship_fig = None

        date_cols = [col for col in df.columns if "date" in col]

        if len(date_cols) >= 2 and "ship mode" in df.columns:
            order_col = date_cols[0]
            ship_col = date_cols[1]

            temp = df[[order_col, ship_col]].copy()
            temp[order_col] = pd.to_datetime(temp[order_col], errors="coerce")
            temp[ship_col] = pd.to_datetime(temp[ship_col], errors="coerce")

            temp["lead_time"] = (temp[ship_col] - temp[order_col]).dt.days

            ship_data = df.copy()
            ship_data["lead_time"] = temp["lead_time"]

            ship_avg = ship_data.groupby("ship mode")["lead_time"].mean().reset_index()

            ship_fig = px.bar(ship_avg, x="ship mode", y="lead_time", title="Avg Shipping Time")
            st.plotly_chart(ship_fig, use_container_width=True)

            if st.button("Explain Shipping Efficiency", key="ship_btn"):
                st.info(ai_explain("Shipping lead time analysis", ship_avg.to_string()))
    
    # Third Row - Full Width
    # Treemap Chart
    create_chart_container("Category Profitability", "Sales size vs profit color", icon="📊")
    treemap_fig = None
    if len(cat_cols) >= 2 and len(num_cols) >= 2:
        treemap_fig = px.treemap(
            df,
            path=[cat_cols[0], cat_cols[1]],
            values=num_cols[0],  # Sales
            color=num_cols[1],   # Profit
            title="Sales Size vs Profit Color"
        )
        st.plotly_chart(treemap_fig, use_container_width=True)

        if st.button("Explain Treemap", key="tree_btn"):
            st.info(ai_explain(
                "Treemap showing category and sub-category sales vs profit",
                df[[cat_cols[0], cat_cols[1], num_cols[0], num_cols[1]]].head().to_string()
            ))
