import os
import google.generativeai as genai
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_plotly_code(df):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("API Key not found. Check .env file")

    # Configure Gemini
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("models/gemini-flash-latest")

    prompt = f"""
You are an expert data analyst.

Columns:
{list(df.columns)}

Data Types:
{df.dtypes}

Sample Data:
{df.sample(min(5, len(df))).to_string()}

TASK:
1. Identify best possible graphs
2. Generate ONLY Python code using plotly.express
3. Use 'df' as dataframe
4. Generate multiple graphs
5. Handle missing values

STRICT RULES:
- Output ONLY Python code
- No explanation
- No markdown
"""

    response = model.generate_content(prompt)
    code = response.text

    # Clean markdown if present
    code = re.sub(r"```python|```", "", code)

    return code