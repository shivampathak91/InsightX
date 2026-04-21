
 🚀 InSightX – Smart Retail Analytics & AI Insights Platform

InSightX is an end-to-end **AI-powered retail analytics dashboard** built with Streamlit. It transforms raw CSV data into actionable business insights using **data visualization, machine learning, and LLM-powered explanations**.

---
📌 Features

📊 Data Analysis & Visualization

* Upload CSV files and instantly analyze data
* KPI Metrics (Total Sales, Total Profit)
* Category-wise sales analysis
* Regional distribution (Pie Chart)
* Correlation heatmap
* Sales vs Profit segmentation
* Monthly sales trends
* Treemap (Category & Sub-category profitability)
* Shipping efficiency analysis
* Customer segment insights
* Geographical sales mapping

---

 🤖 AI-Powered Insights

* Auto-generated business explanations for every chart
* Retail-focused insights using LLM (Groq API)
* Smart summaries:

  * Trends
  * Business insights
  * Actionable recommendations

---

🔮 Machine Learning Forecasting

* Time-series forecasting using Prophet
* Predict:

  * Sales
  * Profit
* Custom forecast ranges:

  * 7 Days
  * 30 Days
  * 6 Months
  * 1 Year

---

 💬 AI Chatbot (Ask Your Data)

* Ask natural language questions about your dataset
* Context-aware responses based on:

  * Dataset structure
  * Sample data
  * Statistical summary

---

📄 AI Report Generation

* Generate full PDF reports including:

  * Charts
  * AI explanations
  * Business insights
* One-click download

---

🔐 Authentication

* User login/signup via Supabase
* Secure session handling

---

🛠️ Tech Stack

* **Frontend/UI:** Streamlit
* **Data Processing:** Pandas
* **Visualization:** Plotly
* **Machine Learning:** Prophet, Scikit-learn
* **AI/LLM:** Groq (LLaMA 3.1)
* **Backend/Auth:** Supabase
* **Reporting:** ReportLab

---

⚙️ Installation

```bash
git clone https://github.com/your-username/insightx.git
cd insightx
pip install -r requirements.txt
```

---

🔑 Environment Setup

Add your API keys in the script:

```python
SUPABASE_URL = "your_supabase_url"
SUPABASE_KEY = "your_supabase_key"
GROQ_API_KEY = "your_groq_api_key"
```

---

 ▶️ Run the App

```bash
streamlit run app.py
```

---

📁 Expected Dataset Format

The app automatically detects columns, but works best with:

* Numerical columns → Sales, Profit
* Categorical columns → Category, Segment, Region
* Date column → Order Date / Ship Date
* Optional → City, Ship Mode

---

📊 Example Use Cases

* Retail performance dashboards
* Business intelligence reporting
* Sales forecasting
* Customer segmentation
* Operational efficiency analysis

---

 ⚠️ Limitations

* Requires structured CSV data
* AI responses depend on data quality
* Forecasting requires sufficient time-series data (≥10 rows)

---

 🚀 Future Improvements

* Real-time database integration
* Advanced forecasting models
* Role-based dashboards
* Export to PowerPoint
* Multi-language AI insights

---

🤝 Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you'd like to change.

---

📜 License

This project is licensed under the MIT License.

---

If you want, I can also:

* create a **GitHub-ready version with badges**
* add **screenshots section**
* or write a **killer project description for resumes / LinkedIn**
