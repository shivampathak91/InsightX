import streamlit as st
import tempfile
import pandas as pd
from io import BytesIO
import matplotlib
matplotlib.use('Agg')  # Headless backend for matplotlib
import matplotlib.pyplot as plt

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from ai_functions import ai_explain, generate_recommendations, calculate_business_health, detect_anomalies
from ui_components import create_chart_container

def generate_pdf(metric_option, choice, total_sales, total_profit, df, num_cols, cat_cols, charts):
    """Generate PDF report with all details: Visuals, Explanations, KPIs, Correlation, AI Recommendations, Business Health, and Anomalies"""
    try:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()
        
        # Define custom styles
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Title'],
            fontName='Helvetica-Bold',
            fontSize=22,
            leading=26,
            textColor=colors.HexColor("#1A1F35"),
            alignment=0, # Left aligned
            spaceAfter=15
        )
        
        heading_style = ParagraphStyle(
            'SectionHeading',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=14,
            leading=18,
            textColor=colors.HexColor("#4F46E5"),
            spaceBefore=12,
            spaceAfter=8
        )
        
        body_style = ParagraphStyle(
            'ReportBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=13.5,
            textColor=colors.HexColor("#374151"),
            spaceAfter=8
        )
        
        story = []

        # ================= PAGE 1: COVER & KEY PERFORMANCE INDICATORS =================
        story.append(Paragraph("InSightX Retail Intelligence Executive Report", title_style))
        story.append(Spacer(1, 10))
        
        story.append(Paragraph("Key Performance Indicators (KPIs)", heading_style))
        story.append(Spacer(1, 5))
        
        kpi_data = [
            ["Metric", "Value"],
            ["Total Sales", f"${total_sales:,.2f}"],
            ["Total Profit", f"${total_profit:,.2f}"],
            ["Total Records", f"{len(df):,}"]
        ]
        
        if len(num_cols) > 1:
            margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
            kpi_data.append(["Profit Margin", f"{margin:.2f}%"])

        kpi_table = Table(kpi_data, colWidths=[200, 200])
        kpi_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1A1F35")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 6),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#F9FAFB")),
            ('GRID', (0,0), (-1,-1), 1, colors.HexColor("#E5E7EB")),
            ('FONTSIZE', (0,0), (-1,-1), 9.5),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(kpi_table)
        story.append(Spacer(1, 15))
        
        # 1. Regional Sales Distribution
        if "region" in df.columns and len(num_cols) > 0:
            region_data = df.groupby("region")[num_cols[0]].sum().reset_index()
            fig, ax = plt.subplots(figsize=(5, 3))
            ax.pie(region_data[num_cols[0]], labels=region_data["region"], autopct='%1.1f%%', colors=plt.cm.tab20.colors)
            ax.set_title("Regional Sales Distribution", fontsize=10)
            
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            fig.savefig(tmp.name, bbox_inches="tight", dpi=120)
            plt.close(fig)
            
            story.append(Paragraph("Regional Sales Distribution", heading_style))
            story.append(Image(tmp.name, width=300, height=180))
            story.append(Spacer(1, 5))
            
            desc = f"Regional sales distribution data: {region_data.to_string()}"
            explanation = ai_explain("Regional Sales Distribution", desc)
            story.append(Paragraph(explanation.replace("\n", "<br/>"), body_style))

        story.append(PageBreak())

        # ================= PAGE 2: CORRELATION & TREND ANALYSIS =================
        story.append(Paragraph("Data Relationship & Trends", title_style))
        story.append(Spacer(1, 10))

        # 2. Sales vs Profit Correlation Matrix Visual
        if len(num_cols) > 1:
            corr_val = df[num_cols[0]].corr(df[num_cols[1]])
            
            fig, ax = plt.subplots(figsize=(5, 3))
            ax.scatter(df[num_cols[0]], df[num_cols[1]], alpha=0.5, color="#4F46E5", edgecolors='none')
            ax.set_title(f"Sales vs Profit Scatter (Pearson Corr: {corr_val:.2f})", fontsize=10)
            ax.set_xlabel("Sales")
            ax.set_ylabel("Profit")
            
            tmp_corr = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            fig.savefig(tmp_corr.name, bbox_inches="tight", dpi=120)
            plt.close(fig)
            
            story.append(Paragraph("Sales vs Profit Correlation Analysis", heading_style))
            story.append(Image(tmp_corr.name, width=300, height=180))
            story.append(Spacer(1, 5))
            
            corr_desc = f"Scatter correlation data of Sales vs Profit: correlation value is {corr_val:.2f}. Total records: {len(df)}."
            explanation = ai_explain("Sales vs Profit Correlation Matrix", corr_desc)
            story.append(Paragraph(explanation.replace("\n", "<br/>"), body_style))
            story.append(Spacer(1, 10))

        # 3. Customer Segments
        if "segment" in df.columns and len(num_cols) > 0:
            seg_data = df.groupby("segment")[num_cols[0]].sum().reset_index()
            fig, ax = plt.subplots(figsize=(5, 3))
            ax.pie(seg_data[num_cols[0]], labels=seg_data["segment"], autopct='%1.1f%%', colors=plt.cm.Pastel1.colors)
            ax.set_title("Revenue by Customer Segment", fontsize=10)
            
            tmp_seg = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            fig.savefig(tmp_seg.name, bbox_inches="tight", dpi=120)
            plt.close(fig)
            
            story.append(Paragraph("Customer Segment Share", heading_style))
            story.append(Image(tmp_seg.name, width=300, height=180))
            story.append(Spacer(1, 5))
            
            desc = f"Customer segment revenue share data: {seg_data.to_string()}"
            explanation = ai_explain("Revenue by Customer Segment", desc)
            story.append(Paragraph(explanation.replace("\n", "<br/>"), body_style))

        story.append(PageBreak())

        # ================= PAGE 3: BUSINESS HEALTH & ANOMALY DETECTION =================
        story.append(Paragraph("Business Health & Machine Learning Insights", title_style))
        story.append(Spacer(1, 10))

        # 4. Business Health Analysis
        overall_score, individual_scores = calculate_business_health(df, num_cols, cat_cols)
        
        # Generate health score horizontal bar chart
        fig, ax = plt.subplots(figsize=(5.5, 2.5))
        metrics = list(individual_scores.keys())
        scores_list = list(individual_scores.values())
        colors_map = ['#10B981' if s >= 14 else '#F59E0B' if s >= 8 else '#EF4444' for s in scores_list]
        
        ax.barh(metrics, scores_list, color=colors_map)
        ax.set_xlim(0, 20)
        ax.set_title(f"Health Breakdown (Overall: {overall_score:.1f}/100)", fontsize=10)
        
        tmp_health = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        fig.savefig(tmp_health.name, bbox_inches="tight", dpi=120)
        plt.close(fig)

        story.append(Paragraph(f"Business Health Score: {overall_score:.1f}/100", heading_style))
        story.append(Image(tmp_health.name, width=330, height=150))
        story.append(Spacer(1, 5))
        
        health_context = f"Business Health Scores: {individual_scores}, Overall Score: {overall_score:.1f}/100."
        health_explanation = ai_explain("Explain this business health score, highlighting strengths, weaknesses, and ways to improve it.", health_context)
        story.append(Paragraph(health_explanation.replace("\n", "<br/>"), body_style))
        story.append(Spacer(1, 15))

        # 5. Machine Learning Anomaly Detection
        detect_cols = list(num_cols)[:2] if len(num_cols) >= 2 else list(num_cols)
        if detect_cols:
            anomaly_data, used_cols = detect_anomalies(df, detect_cols)
            if anomaly_data is not None and len(used_cols) >= 2:
                total_anomalies = anomaly_data['is_anomaly'].sum()
                anomaly_rate = (total_anomalies / len(anomaly_data)) * 100
                
                # Visual scatter plot for anomalies
                fig, ax = plt.subplots(figsize=(5, 3))
                normal = anomaly_data[~anomaly_data['is_anomaly']]
                anom = anomaly_data[anomaly_data['is_anomaly']]
                
                ax.scatter(normal[used_cols[0]], normal[used_cols[1]], color="#10B981", label="Normal", alpha=0.5, edgecolors='none')
                ax.scatter(anom[used_cols[0]], anom[used_cols[1]], color="#EF4444", label="Anomaly", alpha=0.8, edgecolors='none')
                ax.set_title("ML Anomaly Detection Map", fontsize=10)
                ax.set_xlabel(used_cols[0])
                ax.set_ylabel(used_cols[1])
                ax.legend(fontsize=8)
                
                tmp_anom = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
                fig.savefig(tmp_anom.name, bbox_inches="tight", dpi=120)
                plt.close(fig)
                
                story.append(Paragraph(f"ML Anomaly Analysis (Detected {total_anomalies} anomalies, Rate: {anomaly_rate:.2f}%)", heading_style))
                story.append(Image(tmp_anom.name, width=300, height=180))
                story.append(Spacer(1, 5))
                
                anomaly_context = f"Anomalies found: {total_anomalies} records ({anomaly_rate:.2f}%) using columns {used_cols}."
                anomaly_explanation = ai_explain("Analyze these ML anomaly results, explaining why they are unusual and recommending action steps.", anomaly_context)
                story.append(Paragraph(anomaly_explanation.replace("\n", "<br/>"), body_style))

        story.append(PageBreak())

        # ================= PAGE 4: AI STRATEGIC RECOMMENDATIONS =================
        story.append(Paragraph("AI-Powered Strategic Recommendations", title_style))
        story.append(Spacer(1, 10))

        recs = generate_recommendations(df, num_cols, cat_cols)
        story.append(Paragraph(recs.replace("\n", "<br/>"), body_style))

        doc.build(story)
        buffer.seek(0)
        return buffer
    except Exception as e:
        st.error(f"PDF generation failed: {str(e)}")
        return None

def render_reports(df, num_cols, cat_cols, total_sales, total_profit, charts):
    """Render the Reports page"""
    create_chart_container("Generate AI Report", "Export comprehensive analysis", icon="📄")

    metric_option = st.selectbox("Select Metric for Report", ["Sales", "Profit"])
    choice = st.selectbox("Forecast Range for Report", ["7 Days", "30 Days", "6 Months", "1 Year"])

    if st.button("Generate Report", key="gen_btn_page"):
        try:
            with st.spinner("Generating AI Report..."):
                pdf = generate_pdf(metric_option, choice, total_sales, total_profit, df, num_cols, cat_cols, charts)
                
                if pdf:
                    st.session_state["pdf_ready"] = pdf
                    st.success("✅ Report Ready!")
                    
                    st.download_button(
                        label="📄 Download Full AI Report",
                        data=pdf,
                        file_name="Retail_AI_Report.pdf",
                        mime="application/pdf",
                        key="download_pdf_page"
                    )
        except Exception as e:
            st.error(f"❌ Failed: {e}")
