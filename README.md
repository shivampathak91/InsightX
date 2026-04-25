<h1 align="center">🚀 InSightX – AI-Powered Retail Analytics & Insights Platform</h1>

<p align="center">
  📊 Transform raw retail data into actionable business insights using AI, Machine Learning & Interactive Dashboards  
</p>

<hr>

<h2>🔍 Overview</h2>
<p>
<b>InSightX</b> is an end-to-end AI-powered retail analytics dashboard built with Streamlit.  
It converts raw CSV datasets into <b>interactive visualizations, predictive insights, and AI-generated business recommendations</b>.
</p>

<p>👉 It bridges the gap between <b>raw data → insights → decision-making</b>.</p>

<hr>

<h2>🎯 Problem Statement</h2>
<ul>
<li>Unstructured and inconsistent datasets</li>
<li>Manual KPI calculations and slow reporting</li>
<li>Lack of real-time insights and forecasting</li>
</ul>

<p>👉 <b>InSightX automates analysis, visualization, and insight generation in one platform.</b></p>

<hr>

<h2>💡 Key Features</h2>

<h3>📊 Data Analysis & Visualization</h3>
<ul>
<li>Upload CSV files and instantly analyze data</li>
<li>KPI Metrics (Total Sales, Total Profit)</li>
<li>Category-wise & regional analysis</li>
<li>Correlation heatmaps & segmentation</li>
<li>Monthly trends & treemap visualization</li>
<li>Shipping efficiency & customer insights</li>
<li>Geographical sales mapping</li>
</ul>

<h3>🤖 AI-Powered Insights</h3>
<ul>
<li>Auto-generated explanations for charts</li>
<li>Retail-focused insights using LLM (Groq API)</li>
<li>Trends, insights & recommendations</li>
</ul>

<h3>🔮 Machine Learning Forecasting</h3>
<ul>
<li>Time-series forecasting using Prophet</li>
<li>Predict sales & profit</li>
<li>7 Days | 30 Days | 6 Months | 1 Year</li>
</ul>

<h3>💬 AI Chatbot</h3>
<ul>
<li>Ask natural language questions</li>
<li>Context-aware dataset responses</li>
</ul>

<h3>📄 AI Report Generation</h3>
<ul>
<li>Generate PDF reports with charts & insights</li>
<li>One-click download</li>
</ul>

<h3>🔐 Authentication</h3>
<ul>
<li>Login/signup using Supabase</li>
<li>Secure session handling</li>
</ul>

<hr>

<h2>🛠️ Tech Stack</h2>
<ul>
<li><b>Frontend:</b> Streamlit</li>
<li><b>Data:</b> Pandas</li>
<li><b>Visualization:</b> Plotly</li>
<li><b>ML:</b> Prophet, Scikit-learn</li>
<li><b>AI:</b> Groq (LLaMA 3.1)</li>
<li><b>Backend:</b> Supabase</li>
<li><b>Reporting:</b> ReportLab</li>
</ul>

<hr>

<h2>⚙️ System Workflow</h2>

<pre>
CSV Upload → Data Cleaning → KPI Analysis → Visualization → AI Insights → Forecasting → Report Generation
</pre>

<hr>

<h2>📊 Example Use Case</h2>
<ul>
<li>Analyze retail dataset (10K+ rows)</li>
<li>Identify top-performing categories</li>
<li>Track revenue trends</li>
<li>Generate AI recommendations</li>
<li>Forecast future sales</li>
</ul>

<hr>

<h2 align="center">📸 Application Preview</h2>

---

<h3 align="center">🔐 1. Login / Signup</h3>
<p align="center">
  <img src="https://raw.githubusercontent.com/shivampathak91/InsightX/main/insightx/loginsignup.png" width="800"/>
</p>

---

<h3 align="center">📂 2. Upload Dataset</h3>
<p align="center">
  <img src="https://raw.githubusercontent.com/shivampathak91/InsightX/main/insightx/upload.png" width="800"/>
</p>

---

<h3 align="center">📊 3. Sales Dashboard</h3>
<p align="center">
  <img src="https://raw.githubusercontent.com/shivampathak91/InsightX/main/insightx/sales.png" width="800"/>
</p>

---

<h3 align="center">🔮 4. Forecasting</h3>
<p align="center">
  <img src="https://raw.githubusercontent.com/shivampathak91/InsightX/main/insightx/forecast.png" width="800"/>
</p>

---

<h3 align="center">🤖 5. AI Insights / Explanation</h3>
<p align="center">
  <img src="https://raw.githubusercontent.com/shivampathak91/InsightX/main/insightx/explain.png" width="800"/>
</p>

---

<h3 align="center">💬 6. AI Chatbot</h3>
<p align="center">
  <img src="https://raw.githubusercontent.com/shivampathak91/InsightX/main/insightx/chatbot.png" width="800"/>
</p>


<hr>

<h2>🚀 Installation</h2>

<pre>
git clone https://github.com/shivampathak91/insightx.git
cd insightx
pip install -r requirements.txt
</pre>

<hr>

<h2>🔑 Environment Setup</h2>

<pre>
SUPABASE_URL = "your_supabase_url"
SUPABASE_KEY = "your_supabase_key"
GROQ_API_KEY = "your_groq_api_key"
</pre>

<hr>

<h2>▶️ Run the App</h2>

<pre>
streamlit run app.py
</pre>

<hr>

<h2>📁 Dataset Format</h2>
<ul>
<li>Numerical → Sales, Profit</li>
<li>Categorical → Category, Segment, Region</li>
<li>Date → Order Date</li>
<li>Optional → City, Ship Mode</li>
</ul>

<hr>

<h2>📈 Results & Impact</h2>
<ul>
<li>Automated KPI calculations</li>
<li>Faster insights from raw data</li>
<li>AI-driven decision support</li>
</ul>

<hr>

<h2>⚠️ Limitations</h2>
<ul>
<li>Requires structured CSV</li>
<li>AI depends on data quality</li>
<li>Forecasting needs sufficient data</li>
</ul>

<hr>

<h2>⚠️ Kaleido Issue</h2>

<p><b>Problem:</b> Works locally but may fail on Streamlit Cloud</p>

<p><b>Fix:</b></p>
<pre>
kaleido
</pre>

<p>Or create:</p>
<pre>
libgl1
libglib2.0-0
</pre>

<hr>

<h2>🚀 Future Improvements</h2>
<ul>
<li>Real-time data pipelines</li>
<li>Cloud deployment</li>
<li>Advanced ML models</li>
<li>Role-based dashboards</li>
</ul>

<hr>

<h2>👨‍💻 Author</h2>
<p><b>Shivam Pathak</b><br>
Aspiring Data Analyst | Data Scientist |  Future Data Engineer</p>

<hr>

<p align="center">⭐ If you like this project, consider giving it a star!</p>
