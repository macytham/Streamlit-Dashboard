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

    # Actual dictionary rows start at row 2 (third row)
    df = df_raw.iloc[2:, :].copy()
    df.columns = headers
    df.reset_index(drop=True, inplace=True)

    st.markdown("### Data Dictionary")
    st.dataframe(df, use_container_width=True)


# ======= TAB 3 DATA LOADER (WITH SLIDER) =======
def load_data(data: dict):
    """
    Show the 'Switchbacks' sheet with a row-range slider filter.
    """
    df = data.get("Switchbacks")

    if df is None:
        st.error("No sheet named 'Switchbacks' found in the dataset.")
        return

    n_rows = len(df)
    if n_rows == 0:
        st.warning("The 'Switchbacks' sheet is empty.")
        return

    st.markdown("### Switchbacks Data")

    # Double int slider for row range
    start_row, end_row = st.slider(
        "Select row range (by index)",
        min_value=0,
        max_value=n_rows - 1,
        value=(0, min(50, n_rows - 1)),
    )

    # Filter dataframe by selected range (inclusive)
    filtered_df = df.iloc[start_row:end_row + 1]

    st.caption(f"Showing rows {start_row} to {end_row} (total {len(filtered_df)} rows)")
    st.dataframe(filtered_df, use_container_width=True)


# ===== HEADER WITH LOGOS & TITLE =====
left_col, middle_col, right_col = st.columns([1, 4, 1])

with left_col:
    st.image("Data files/Uber-logo.png", use_container_width=True)

with middle_col:
    st.markdown(
        "<h1 style='text-align: center; margin-bottom: 0;'>HBR - UBER Case Study Dashboard</h1>",
        unsafe_allow_html=True,
    )

with right_col:
    st.image("Data files/rice-logo.jpg", use_container_width=True)

st.markdown("---")

# ===== TABS =====
tab_metadata, tab_dictionary, tab_visuals = st.tabs(
    ["Metadata", "Data Dictionary", "Visualisations"]
)

# ===== TAB 1: METADATA =====
with tab_metadata:
    st.subheader("Metadata")

    st.write("Dataset loaded from Google Sheets:")
    st.write(f"**Sheets found:** {list(data.keys())}")

    # Show preview of Switchbacks sheet
    if switchbacks_df is not None:
        st.markdown("### Preview of `Switchbacks` Sheet")
        st.dataframe(switchbacks_df.head())
    else:
        st.warning("Sheet named 'Switchbacks' not found in the Excel file.")

    st.markdown("---")

    # Show metadata text
    show_metadata(data)


# ===== TAB 2: DATA DICTIONARY =====
with tab_dictionary:
    st.subheader("Data Dictionary Overview")
    st.write("Below is the automatically extracted data dictionary from your Google Sheet:")

    show_dictionary(data)


# ===== TAB 3: VISUALISATIONS =====
with tab_visuals:
    st.subheader("Visualisations")

    # Three columns layout
    col1, col2, col3 = st.columns(3)

    # ---- LEFT COLUMN: TABLE + SLIDER ----
    with col1:
        load_data(data)

    # ---- MIDDLE COLUMN: Example chart 1 ----
    with col2:
        st.markdown("##### Example: Trips per Day (dummy data)")
        trips_per_day = {
            "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "Trips": [120, 135, 150, 160, 200, 250, 220],
        }
        st.line_chart(trips_per_day, x="Day", y="Trips")

    # ---- RIGHT COLUMN: Example chart 2 ----
    with col3:
        st.markdown("##### Example: Average Fare vs Surge Multiplier (dummy data)")
        surge_levels = {
            "Surge Multiplier": [1.0, 1.2, 1.5, 2.0],
            "Average Fare (USD)": [12, 14, 18, 25],
        }
        st.bar_chart(surge_levels, x="Surge Multiplier", y="Average Fare (USD)")

        st.info(
            "Replace the dummy data above with your actual case study data and "
            "add more visualisations as needed (e.g., driver utilisation, wait times, etc.)."
        )
