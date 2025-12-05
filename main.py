import streamlit as st

# Page config
st.set_page_config(
    page_title="HBR - UBER Case Study Dashboard",
    layout="wide",
)

# ===== HEADER WITH LOGOS & TITLE =====
# Replace "left_logo.png" and "right_logo.png" with your actual image file paths or URLs
left_col, middle_col, right_col = st.columns([1, 3, 1])

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
    st.write("Add high-level information about the case study and dataset here.")
    st.markdown(
        """
        **Example fields you might include:**
        - Case name: HBR – Uber Case Study  
        - Data source: *Describe where the data comes from*  
        - Time period covered: *e.g., 2014–2017*  
        - Unit of analysis: *e.g., trips, drivers, customers*  
        - Last updated: *YYYY-MM-DD*  
        """
    )

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
    # Using a simple structure for bar chart
    surge_levels = {
        "Surge Multiplier": [1.0, 1.2, 1.5, 2.0],
        "Average Fare (USD)": [12, 14, 18, 25],
    }
    st.bar_chart(surge_levels, x="Surge Multiplier", y="Average Fare (USD)")

    st.info(
        "Replace the dummy data above with your actual case study data and "
        "add more visualisations as needed (e.g., driver utilisation, wait times, etc.)."
    )
