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
    """
    Load all sheets from a Google Sheets link (as Excel) into a dict of DataFrames.
    Keys = sheet names, values = DataFrames.
    """
    # Convert the Google Sheets URL into a direct Excel export link
    base = data_url.split("/edit")[0]
    modified_url = base + "/export?format=xlsx"

    # Load ALL sheets from the Excel file
    all_sheets = pd.read_excel(modified_url, sheet_name=None)
    return all_sheets


data = load_file(data_url)

# Example access: sheet named "Switchbacks"
switchbacks_df = data.get("Switchbacks")  # Will be None if sheet not found


def show_metadata(data: dict) -> None:
    """
    Show metadata from a sheet named 'Copyright' inside Streamlit.
    Assumes the sheet contains text in its first column.
    """
    df = data.get("Copyright")

    if df is None:
        st.error("No sheet named 'Copyright' found in the dataset.")
        return

    # Use first column of non-null rows
    lines = [row[0] for row in df.dropna().values.tolist()]
    text = "\n".join(lines)

    st.markdown("### Copyright Information")
    st.markdown(text)


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

    # Show metadata from "Copyright" sheet
    show_metadata(data)

# ===== TAB 2: DATA DICTIONARY =====
with tab_dictionary:
    st.subheader("Data Dictionary")
    st.write("Describe each variable/column used in the analysis.")

    # Example data dictionary using only Streamlit (simple table)
    data_dict = {
        "Variable": [
            "trip_id",
            "driver_id",
            "customer_id",
            "request_datetime",
            "pickup_location",
            "dropoff_location",
            "fare_amount",
            "surge_multiplier",
        ],
        "Type": [
            "string",
            "string",
            "string",
            "datetime",
            "string",
            "string",
            "float",
            "float",
        ],
        "Description": [
            "Unique identifier for each trip",
            "Unique identifier for driver",
            "Unique identifier for customer",
            "Datetime when the ride was requested",
            "Pickup zone or coordinates",
            "Dropoff zone or coordinates",
            "Total fare charged to customer",
            "Multiplier applied during peak demand",
        ],
    }

    # Streamlit can render a simple table directly from dict
    st.table(data_dict)

# ===== TAB 3: VISUALISATIONS =====
with tab_visuals:
    st.subheader("Visualisations")
    st.write("Add charts and key metrics that support the case study analysis.")

    st.markdown("##### Example: Trips per Day (dummy data)")
    trips_per_day = {
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "Trips": [120, 135, 150, 160, 200, 250, 220],
    }
    st.line_chart(trips_per_day, x="Day", y="Trips")

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
