import streamlit as st
import plotly.express as px
from ai_functions import ai_explain, detect_anomalies
from ui_components import create_premium_card, create_chart_container

def render_anomaly_detection(df, num_cols):
    """Render the Anomaly Detection page"""
    create_chart_container("AI Anomaly Detection", "ML-powered pattern detection", icon="🚨")

    with st.expander("Detect Anomalies in Your Data", expanded=True):
        st.info("Uses Isolation Forest ML algorithm to detect unusual patterns in sales, profit, discount, and quantity.")
        
        # Select columns for anomaly detection
        detect_cols = st.multiselect(
            "Select columns to analyze for anomalies",
            options=list(num_cols),
            default=list(num_cols)[:2] if len(num_cols) >= 2 else list(num_cols)
        )
        
        if st.button("Run Anomaly Detection", key="anomaly_btn_page"):
            if detect_cols:
                with st.spinner("Detecting anomalies using ML..."):
                    anomaly_data, used_cols = detect_anomalies(df, detect_cols)
                    
                    if anomaly_data is not None:
                        total_anomalies = anomaly_data['is_anomaly'].sum()
                        anomaly_percentage = (total_anomalies / len(anomaly_data)) * 100
                        
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Total Anomalies", total_anomalies)
                        col2.metric("Percentage", f"{anomaly_percentage:.2f}%")
                        col3.metric("Columns Analyzed", len(used_cols))
                        
                        # Show top anomalous transactions
                        st.subheader("Top Anomalous Transactions")
                        top_anomalies = anomaly_data[anomaly_data['is_anomaly']].nsmallest(10, 'anomaly_score')
                        st.dataframe(top_anomalies.drop(['is_anomaly', 'anomaly_score'], axis=1, errors='ignore'))
                        
                        # Visualize anomalies
                        if len(used_cols) >= 2:
                            fig = px.scatter(
                                anomaly_data,
                                x=used_cols[0],
                                y=used_cols[1],
                                color='is_anomaly',
                                color_discrete_map={True: 'red', False: 'blue'},
                                title=f"Anomaly Detection: {used_cols[0]} vs {used_cols[1]}"
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        
                        # AI Explanation
                        with st.spinner("Generating AI explanation..."):
                            anomaly_context = f"""
Anomaly Detection Results:
- Total Records: {len(anomaly_data)}
- Anomalies Found: {total_anomalies}
- Anomaly Rate: {anomaly_percentage:.2f}%
- Columns Analyzed: {used_cols}
- Top Anomalous Values:
{top_anomalies.head(5).to_string()}
"""
                            explanation = ai_explain(
                                "Explain these anomalies: why are they unusual, possible business reasons, and suggested actions",
                                anomaly_context
                            )
                            create_premium_card("AI Anomaly Analysis", explanation.replace('\n', '<br/>'), icon="🔍", color="red")
            else:
                st.warning("Please select at least one column")
