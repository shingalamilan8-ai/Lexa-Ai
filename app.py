import streamlit as st
import pandas as pd
from utils import generate_plotly_code
import json

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="AI Data Analyst", layout="wide")

st.title("🤖 AI Data Analyst Dashboard")

# -------------------------------
# FILE UPLOAD
# -------------------------------
uploaded_file = st.file_uploader("📂 Upload CSV or Excel file", type=["csv", "xlsx"])

df = None

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("✅ File uploaded successfully")

        st.subheader("📊 Data Preview")
        st.dataframe(df.head())

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")

# -------------------------------
# GENERATE BUTTON
# -------------------------------
if st.button("🚀 Generate Charts"):

    if df is None:
        st.error("❌ Please upload a dataset first")

    else:
        with st.spinner("🤖 Analyzing data and generating charts..."):

            try:
                code = generate_plotly_code(df)

                st.subheader("⚡ Generated Code")
                st.code(code, language="python")

                st.subheader("📊 Visualizations")

                # Safe execution
                local_vars = {"df": df}

                # ❌ Remove fig.show() (prevents new tabs)
                clean_code = code.replace(".show()", "")
                
                # Execute cleaned code
                exec(clean_code, {}, local_vars)

                # Display figures
                found = False
                for var in local_vars:
                    if "fig" in var.lower():
                        st.plotly_chart(local_vars[var], use_container_width=True)
                        found = True

                if not found:
                    st.warning("⚠️ No charts were generated")

            except Exception as e:
                st.error(f"❌ Error: {e}")
                
            
            
if st.button("💾 Save Dashboard"):

    charts_data = []

    for var in local_vars:
        if "fig" in var.lower():
            charts_data.append(local_vars[var].to_dict())

    with open("saved_dashboard.json", "w") as f:
        json.dump(charts_data, f)

    st.success("✅ Dashboard saved!")
    
    
    
if st.button("📂 Load Dashboard"):
    import json

    with open("saved_dashboard.json", "r") as f:
        charts = json.load(f)

    for chart in charts:
        st.plotly_chart(chart, use_container_width=True)
        
        
        
        
        
        
