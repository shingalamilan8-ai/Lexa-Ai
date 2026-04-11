import os
import google.generativeai as genai
import re
from dotenv import load_dotenv

load_dotenv()

def get_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("API key missing in .env")

    genai.configure(api_key=api_key)
    return genai.GenerativeModel("models/gemini-flash-latest")


# 🔥 Generate Plotly Code (1 API CALL)
def generate_plotly_code(df):
    model = get_model()

    prompt = f"""
You are an expert data analyst.

Dataset Columns:
{list(df.columns)}

Data Types:
{df.dtypes}

Sample Data:
{df.sample(min(5, len(df))).to_string()}

TASK:
1. Select BEST meaningful visualizations
2. Use plotly.express ONLY
3. Add proper titles, labels, colors
4. Create multiple graphs
5. Store in variables: fig1, fig2, fig3...

IMPORTANT:
- DO NOT use fig.show()
- RETURN ONLY PYTHON CODE
"""

    response = model.generate_content(prompt)
    code = response.text
    code = re.sub(r"```python|```", "", code)

    return code


# 🔥 Generate ALL insights (1 API CALL)
def generate_all_insights(df, code):
    model = get_model()

    prompt = f"""
You are a senior business analyst.

Dataset:
{df.sample(min(5, len(df))).to_string()}

Charts Code:
{code}

TASK:
Explain ALL charts.

For each chart:
- What it shows
- Key insights
- Business meaning

Make it structured.
"""

    response = model.generate_content(prompt)
    return response.text


# 🔥 Chat with Dataset (1 API CALL per question)
def chat_with_data(df, query):
    model = get_model()

    prompt = f"""
Dataset:
{df.sample(min(5, len(df))).to_string()}

User Question:
{query}

Answer clearly.
"""

    response = model.generate_content(prompt)
    return response.text