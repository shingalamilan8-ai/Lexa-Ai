import streamlit as st
import pandas as pd
import json
import plotly.io as pio
from utils import generate_plotly_code, generate_all_insights, chat_with_data
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="AI Data Analyst", layout="wide")

st.title("🤖 AI Data Analyst Dashboard")

# -------------------------------
# FILE UPLOAD
# -------------------------------
uploaded_file = st.file_uploader("Upload CSV/Excel", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.session_state["df"] = df

    st.success("✅ File Uploaded")
    st.dataframe(df.head())

# -------------------------------
# GENERATE CHARTS
# -------------------------------
if st.button("🚀 Generate Charts"):

    if "df" not in st.session_state:
        st.error("Upload dataset first")

    else:
        df = st.session_state["df"]

        with st.spinner("Generating charts..."):

            code = generate_plotly_code(df)

            st.subheader("⚡ Generated Code")
            st.code(code)

            clean_code = code.replace(".show()", "")

            local_vars = {"df": df}
            exec(clean_code, {}, local_vars)

            figs = []

            for var in local_vars:
                if "fig" in var.lower():
                    figs.append(local_vars[var])

            st.session_state["figs"] = figs
            st.session_state["code"] = code

            # 🔥 ONE CALL INSIGHTS
            insights = generate_all_insights(df, code)
            st.session_state["insights"] = insights


# -------------------------------
# DISPLAY (PERSISTENT)
# -------------------------------
if "figs" in st.session_state:

    st.subheader("📊 Visualizations")

    for fig in st.session_state["figs"]:
        st.plotly_chart(fig, use_container_width=True)

if "insights" in st.session_state:

    st.subheader("📊 Insights")
    st.success(st.session_state["insights"])


# -------------------------------
# SAVE DASHBOARD (FIXED)
# -------------------------------
if st.button("💾 Save Dashboard"):

    if "figs" in st.session_state:

        charts_json = [pio.to_json(fig) for fig in st.session_state["figs"]]

        with open("dashboard.json", "w") as f:
            json.dump(charts_json, f)

        st.success("✅ Dashboard Saved!")


# -------------------------------
# LOAD DASHBOARD (FIXED)
# -------------------------------
if st.button("📂 Load Dashboard"):

    try:
        with open("dashboard.json", "r") as f:
            charts_json = json.load(f)

        figs = [pio.from_json(c) for c in charts_json]

        st.session_state["figs"] = figs

        st.success("✅ Dashboard Loaded!")

    except:
        st.error("❌ No saved dashboard found")


# -------------------------------
# EXPORT PDF
# -------------------------------
if st.button("📄 Export Insights as PDF"):

    if "insights" in st.session_state:

        doc = SimpleDocTemplate("report.pdf")
        styles = getSampleStyleSheet()

        content = [Paragraph(st.session_state["insights"], styles["Normal"])]

        doc.build(content)

        st.success("✅ PDF saved as report.pdf")


# -------------------------------
# CHAT WITH DATASET
# -------------------------------
st.subheader("💬 Chat with Dataset")

query = st.text_input("Ask something about your data")

if st.button("Ask"):

    if "df" not in st.session_state:
        st.error("Upload dataset first")

    elif query:
        answer = chat_with_data(st.session_state["df"], query)
        st.success(answer)