import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="HBR - UBER Case Study Dashboard",
    layout="wide",
)

# ======= LOAD DATA =======
data_url = "https://docs.google.com/spreadsheets/d/1fTpJACr1Ay6DEIgFxjFZF8LgEPiwwAFY/edit?usp=sharing&ouid=103457517634340619188&rtpof=true&sd=true"


@st.cache_data
def load_file(data_url: str) -> dict:
    """Load all sheets from a Google Sheets link (as Excel)."""
    base = data_url.split("/edit")[0]
    modified_url = base + "/export?format=xlsx"
    all_sheets = pd.read_excel(modified_url, sheet_name=None)
    return all_sheets


data = load_file(data_url)

# Example: Switchbacks sheet
switchbacks_df = data.get("Switchbacks")


# ======= METADATA FUNCTION =======
def show_metadata(data: dict):
    df = data.get("Copyright")

    if df is None:
        st.error("No sheet named 'Copyright' found in the dataset.")
        return

    lines = [row[0] for row in df.dropna().values.tolist()]
    text = "\n".join(lines)

    st.markdown("### Copyright Information")
    st.markdown(text)


# ======= DATA DICTIONARY FUNCTION =======
def show_dictionary(data: dict):
    if "Data Dictionary" not in data:
        st.error("No sheet named 'Data Dictionary' found.")
        return

    df_raw = data["Data Dictionary"]

    # Extract headers from row 1 (second row)
    headers = df_raw.iloc[1, :].values.tolist()
