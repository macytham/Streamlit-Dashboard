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


# ======= TAB 3 LEFT COLUMN: DATA TABLE WITH SLIDER =======
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


# ======= TAB 3 MIDDLE COLUMN: TIME SERIES PLOT =======
def show_time_series(data: dict):
    df = data.get("Switchbacks")

    if df is None:
        st.error("No sheet named 'Switchbacks' found in the dataset.")
        return

    df = df.copy()

    # Ensure period_start is datetime
    if not pd.api.types.is_datetime64_any_dtype(df["period_start"]):
        df["period_start"] = pd.to_datetime(df["period_start"], errors="coerce")

    df = df.dropna(subset=["period_start"])

    # Candidate metrics
    candidate_metrics = ["trips_pool", "trips_express", "rider_cancellations"]
    available_metrics = [m for m in candidate_metrics if m in df.columns]

    if not available_metrics:
        st.error("None of the expected metrics columns were found in 'Switchbacks'.")
        return

    st.markdown("### Time Series of Uber Trips in Boston")

    # Multi-selection filter of metrics to plot
    selected_metrics = st.multiselect(
        "Select metrics to plot",
        options=available_metrics,
        default=available_metrics,
    )

    if not selected_metrics:
        st.warning("Please select at least one metric to plot.")
        return

    fig = go.Figure()

    for y_column in selected_metrics:
        fig.add_trace(
            go.Scatter(
                x=df["period_start"],
                y=df[y_column],
                mode="lines+markers",
                name=y_column,
            )
        )

    fig.update_layout(
        title="Time Series of Uber Trips in Boston",
        xaxis_title="Time",
        yaxis_title="Value",
        height=500,
        legend_title="Metric",
    )

    st.plotly_chart(fig, use_container_width=True)


# ======= TAB 3 RIGHT COLUMN: PIE CHART =======
def pie_chart(data: dict):
    df = data.get("Switchbacks")

    if df is None:
        st.error("No sheet named 'Switchbacks' found in the dataset.")
        return

    df = df.copy()

    # Ensure period_start is datetime
    if not pd.api.types.is_datetime64_any_dtype(df["period_start"]):
        df["period_start"] = pd.to_datetime(df["period_start"], errors="coerce")

    df = df.dropna(subset=["period_start"])

    if "total_driver_payout" not in df.columns:
        st.error("Column 'total_driver_payout' not found in 'Switchbacks'.")
        return

    st.markdown("### Driver Payout Distribution")

    # Dropdown to select period aggregation
    period = st.selectbox(
        "Select period aggregation",
        options=["week", "month"],
        index=0,
    )

    if period == "week":
        df["label"] = df["period_start"].dt.day_name()
        title = "Total Driver Payout by Day of Week"
    else:  # month
        df["label"] = df["period_start"].dt.month_name()
        title = "Total Driver Payout by Month"

    # Aggregate payouts by label
    grouped = (
        df.groupby("label", as_index=False)["total_driver_payout"]
        .sum()
        .sort_values("total_driver_payout", ascending=False)
    )

    fig = px.pie(
        grouped,
        names="label",
        values="total_driver_payout",
        title=title,
    )

    st.plotly_chart(fig, use_container_width=True)


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

    # ---- MIDDLE COLUMN: TIME SERIES ----
    with col2:
        show_time_series(data)

    # ---- RIGHT COLUMN: PIE CHART ----
    with col3:
        pie_chart(data)
