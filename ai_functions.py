import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from groq import Groq
from config import GROQ_API_KEY

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

def ai_explain(prompt, data):
    """Generate AI explanation for data visualizations"""
    try:
        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": """
"You are a Retail Data Analyst.

Rules:
- NEVER return Python code
- ALWAYS return final numeric answers when asked (like total sales, profit)
- Be direct and business-friendly
- If user asks for totals → calculate from given data summary
- Give short answer + insight

Format:
Answer: <value>
Insight: <short business meaning>"

Explain the visualization in 3 parts:
1. Trend
2. Retail Insight
3. Actionable Takeaway

Keep it short and professional.
"""
                },
                {"role": "user", "content": f"{prompt}\n\nData:\n{data}"}
            ]
        )
        return res.choices[0].message.content
    except Exception as e:
        st.error(f"AI Error: {str(e)}")
        return f"AI temporarily unavailable. Error: {str(e)}"

@st.cache_data(ttl=3600)
def generate_executive_summary(df, _num_cols, _cat_cols):
    """Generate AI-powered executive summary"""
    try:
        num_cols = list(_num_cols)
        cat_cols = list(_cat_cols)
        total_sales = df[num_cols[0]].sum() if len(num_cols) > 0 else 0
        total_profit = df[num_cols[1]].sum() if len(num_cols) > 1 else 0
        
        # Find best region
        best_region = "N/A"
        if "region" in df.columns and len(num_cols) > 0:
            region_sales = df.groupby("region")[num_cols[0]].sum()
            best_region = region_sales.idxmax()
        
        # Find worst category
        worst_category = "N/A"
        if len(cat_cols) > 0 and len(num_cols) > 0:
            cat_sales = df.groupby(cat_cols[0])[num_cols[0]].sum()
            worst_category = cat_sales.idxmin()
        
        context = f"""
Dataset Summary:
- Total Records: {len(df)}
- Total Sales: {total_sales:,.2f}
- Total Profit: {total_profit:,.2f}
- Best Region: {best_region}
- Worst Category: {worst_category}
- Columns: {list(df.columns)}
- Sample Data:
{df.head(3).to_string()}
"""
        
        prompt = """
Generate an executive summary with these sections:
1. Business Overview (2 sentences)
2. Top Revenue Drivers (2-3 bullet points)
3. Biggest Risks (2-3 bullet points)
4. Best Performing Region (1 sentence)
5. Worst Performing Category (1 sentence)
6. Growth Opportunities (2-3 bullet points)
7. Top 5 AI Recommendations (numbered list)

Be concise, professional, and actionable.
"""
        
        result = ai_explain(prompt, context)
        
        # Check if AI returned an error message
        if "AI temporarily unavailable" in result or "AI Error" in result:
            # Provide fallback summary
            return f"""
**Business Overview**
Your dataset contains {len(df)} records with total sales of ${total_sales:,.2f} and profit of ${total_profit:,.2f}.

**Top Revenue Drivers**
- Total Sales: ${total_sales:,.2f}
- Total Profit: ${total_profit:,.2f}
- Average Profit per Transaction: ${total_profit/len(df) if len(df) > 0 else 0:,.2f}

**Biggest Risks**
- Worst Performing Category: {worst_category}
- Review profit margins for underperforming segments

**Best Performing Region**
{best_region} shows the highest sales performance.

**Worst Performing Category**
{worst_category} requires attention to improve profitability.

**Growth Opportunities**
- Focus on expanding in the {best_region} region
- Improve product mix in underperforming categories
- Optimize pricing strategies based on profit margins

**Top 5 AI Recommendations**
1. Increase marketing efforts in {best_region} region
2. Analyze and improve {worst_category} category performance
3. Implement dynamic pricing for better margins
4. Cross-sell high-margin products across segments
5. Monitor and optimize inventory turnover rates
"""
        
        return result
    except Exception as e:
        # Provide fallback summary even on error
        num_cols = list(_num_cols)
        total_sales = df[num_cols[0]].sum() if len(num_cols) > 0 else 0
        total_profit = df[num_cols[1]].sum() if len(num_cols) > 1 else 0
        return f"""
**Business Overview**
Your dataset contains {len(df)} records with total sales of ${total_sales:,.2f} and profit of ${total_profit:,.2f}.

**Note: AI analysis temporarily unavailable. Showing basic summary instead.**

**Key Metrics**
- Total Records: {len(df)}
- Total Sales: ${total_sales:,.2f}
- Total Profit: ${total_profit:,.2f}
"""

@st.cache_data(ttl=3600)
def detect_anomalies(df, columns, contamination=0.05):
    """Detect anomalies using Isolation Forest"""
    try:
        # Filter only numeric columns that exist
        available_cols = [col for col in columns if col in df.columns]
        if not available_cols:
            return None, []
        
        data = df[available_cols].dropna()
        if len(data) < 10:
            return None, []
        
        # Scale data
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(data)
        
        # Fit Isolation Forest
        iso_forest = IsolationForest(contamination=contamination, random_state=42)
        anomalies = iso_forest.fit_predict(scaled_data)
        
        # Add anomaly flag to original data
        data['is_anomaly'] = anomalies == -1
        data['anomaly_score'] = iso_forest.score_samples(scaled_data)
        
        return data, available_cols
    except Exception as e:
        st.error(f"Anomaly detection error: {str(e)}")
        return None, []

@st.cache_data(ttl=3600)
def generate_recommendations(df, _num_cols, _cat_cols):
    """Generate AI-powered business recommendations"""
    try:
        num_cols = list(_num_cols)
        cat_cols = list(_cat_cols)
        context = f"""
Dataset Analysis:
- Total Sales: {df[num_cols[0]].sum() if len(num_cols) > 0 else 0:,.2f}
- Total Profit: {df[num_cols[1]].sum() if len(num_cols) > 1 else 0:,.2f}
- Average Profit Margin: {(df[num_cols[1]].sum() / df[num_cols[0]].sum() * 100) if len(num_cols) > 1 and df[num_cols[0]].sum() > 0 else 0:.2f}%
- Top Categories: {df.groupby(cat_cols[0])[num_cols[0]].sum().nlargest(3).to_dict() if len(cat_cols) > 0 and len(num_cols) > 0 else 'N/A'}
- Regional Performance: {df.groupby('region')[num_cols[0]].sum().to_dict() if 'region' in df.columns and len(num_cols) > 0 else 'N/A'}
- Data Sample:
{df.head(5).to_string()}
"""
        
        prompt = """
Generate 5-10 actionable business recommendations ranked by impact. Focus on:
- Profit optimization
- Inventory management
- Customer retention
- Regional expansion
- Cost reduction
- Marketing strategies

Format each recommendation as:
✓ [Action] - [Expected Benefit]

Be specific and data-driven.
"""
        
        return ai_explain(prompt, context)
    except Exception as e:
        return f"Error generating recommendations: {str(e)}"

@st.cache_data(ttl=3600)
def calculate_business_health(df, _num_cols, _cat_cols):
    """Calculate overall business health score (0-100)"""
    scores = {}
    num_cols = list(_num_cols)
    cat_cols = list(_cat_cols)
    
    try:
        # Sales Performance (0-20)
        if len(num_cols) > 0:
            sales_score = min(20, (df[num_cols[0]].sum() / 1000000) * 20)  # Scale based on 1M
            scores['Sales Performance'] = sales_score
        else:
            scores['Sales Performance'] = 0
        
        # Profitability (0-20)
        if len(num_cols) > 1:
            profit_margin = (df[num_cols[1]].sum() / df[num_cols[0]].sum() * 100) if df[num_cols[0]].sum() > 0 else 0
            profit_score = min(20, (profit_margin / 20) * 20)  # 20% margin = full score
            scores['Profitability'] = profit_score
        else:
            scores['Profitability'] = 0
        
        # Customer Distribution (0-20)
        if 'segment' in df.columns:
            segment_diversity = df['segment'].nunique()
            diversity_score = min(20, segment_diversity * 5)
            scores['Customer Distribution'] = diversity_score
        else:
            scores['Customer Distribution'] = 10
        
        # Data Quality (0-20)
        null_percentage = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        quality_score = max(0, 20 - null_percentage)
        scores['Data Quality'] = quality_score
        
        # Regional Balance (0-20)
        if 'region' in df.columns:
            region_count = df['region'].nunique()
            balance_score = min(20, region_count * 4)
            scores['Regional Balance'] = balance_score
        else:
            scores['Regional Balance'] = 10
        
        overall_score = sum(scores.values())
        return overall_score, scores
    except Exception as e:
        return 50, {'Error': str(e)}
