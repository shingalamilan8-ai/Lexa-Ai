import streamlit as st
import pandas as pd
import json
from utils import generate_plotly_code, generate_all_insights, chat_with_data
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="AI Data Analyst", layout="wide")

st.title("🤖 AI Data Analyst Dashboard")

# -------------------------------
# FILE UPLOAD
# -------------------------------
uploaded_file = st.file_uploader("Upload CSV/Excel", type=["csv", "xlsx"])

df = None

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("✅ File Uploaded")
    st.dataframe(df.head())


# -------------------------------
# GENERATE CHARTS
# -------------------------------
if st.button("🚀 Generate Charts"):

    if df is None:
        st.error("Upload dataset first")

    else:
        with st.spinner("Generating charts..."):

            code = generate_plotly_code(df)

            st.subheader("⚡ Generated Code")
            st.code(code)

            # Remove .show()
            clean_code = code.replace(".show()", "")

            local_vars = {"df": df}
            exec(clean_code, {}, local_vars)

            st.subheader("📊 Visualizations")

            figs = []

            for var in local_vars:
                if "fig" in var.lower():
                    fig = local_vars[var]
                    st.plotly_chart(fig, use_container_width=True)
                    figs.append(fig)

            # Save charts in session
            st.session_state["figs"] = figs
            st.session_state["code"] = code

            # 🔥 ONE CALL INSIGHTS
            st.subheader("📊 Insights")
            insights = generate_all_insights(df, code)
            st.success(insights)

            st.session_state["insights"] = insights


# -------------------------------
# SAVE DASHBOARD
# -------------------------------
if st.button("💾 Save Dashboard"):

    if "figs" in st.session_state:
        data = [fig.to_dict() for fig in st.session_state["figs"]]

        with open("dashboard.json", "w") as f:
            json.dump(data, f)

        st.success("✅ Dashboard Saved!")


# -------------------------------
# LOAD DASHBOARD (WORKING)
# -------------------------------
if st.button("📂 Load Dashboard"):

    try:
        with open("dashboard.json", "r") as f:
            charts = json.load(f)

        st.subheader("📊 Loaded Dashboard")

        for chart in charts:
            st.plotly_chart(chart, use_container_width=True)

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

query = st.text_input("Ask anything about your data")

if st.button("Ask"):

    if df is None:
        st.error("Upload dataset first")

    elif query:
        answer = chat_with_data(df, query)
        st.success(answer)