import streamlit as st
from ai_functions import ai_explain, calculate_business_health
from ui_components import create_premium_card, create_chart_container, create_gauge_chart

def render_business_health(df, num_cols, cat_cols):
    """Render the Business Health page"""
    create_chart_container("Business Health Dashboard", "Comprehensive health analysis", icon="🏥")

    with st.expander("View Business Health Score", expanded=True):
        st.info("Comprehensive health score based on sales, profitability, customer distribution, data quality, and regional balance.")
        
        with st.spinner("Calculating business health score..."):
            overall_score, individual_scores = calculate_business_health(df, num_cols, cat_cols)
            
            # Display gauge chart
            col1, col2 = st.columns([1, 2])
            with col1:
                gauge_fig = create_gauge_chart(overall_score)
                st.plotly_chart(gauge_fig, use_container_width=True)
            
            with col2:
                st.metric("Overall Health Score", f"{overall_score:.1f}/100")
            
            # Color-coded individual scores
            for metric, score in individual_scores.items():
                if metric != "Error":
                    color = "🟢" if score >= 70 else "🟡" if score >= 40 else "🔴"
                    st.markdown(f"{color} **{metric}**: {score:.1f}/20")
        
        # AI explanation
        with st.spinner("Generating AI health analysis..."):
            health_context = f"""
Business Health Analysis:
- Overall Score: {overall_score:.1f}/100
- Individual Scores: {individual_scores}
- Total Sales: {df[num_cols[0]].sum() if len(num_cols) > 0 else 0:,.2f}
- Total Profit: {df[num_cols[1]].sum() if len(num_cols) > 1 else 0:,.2f}
"""
            health_explanation = ai_explain(
                "Explain this business health score: why was this score assigned, what are the strengths and weaknesses, and how to improve it",
                health_context
            )
            create_premium_card("AI Health Analysis", health_explanation.replace('\n', '<br/>'), icon="📊", color="blue")
