import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
@st.cache_data
def load_data():
    url = "cities_air_quality_water_pollution.csv"
    df = pd.read_csv(url)
    df.columns = df.columns.str.replace('"', '').str.strip()
    return df

df = load_data()

# =============================
# Title and Executive Summary
# =============================
st.title("🌎 Global Air Quality & Water Pollution Analysis")

st.markdown("""
**Executive Summary:**  
This dashboard analyzes air quality and water pollution across different global cities.  
We explore pollution hotspots, regional disparities, and uncover correlations to help inform data-driven environmental strategies.
""")

# Dataset Overview
st.subheader("📈 Dataset Overview")
st.write(f"Total number of cities: {df['City'].nunique()}")
st.write(f"Total number of countries: {df['Country'].nunique()}")

# =============================
# Sidebar Filters
# =============================
st.sidebar.header("🔍 Filters")
selected_country = st.sidebar.selectbox("Select a Country", ["All"] + sorted(df["Country"].unique().tolist()))
if selected_country != "All":
    df = df[df["Country"] == selected_country]

selected_region = st.sidebar.selectbox("Select a Region", ["All"] + sorted(df["Region"].unique().tolist()))
if selected_region != "All":
    df = df[df["Region"] == selected_region]

air_quality_range = st.sidebar.slider("Select Air Quality Range",
                                      int(df["AirQuality"].min()),
                                      int(df["AirQuality"].max()),
                                      (int(df["AirQuality"].min()), int(df["AirQuality"].max())))

water_pollution_range = st.sidebar.slider("Select Water Pollution Range",
                                          int(df["WaterPollution"].min()),
                                          int(df["WaterPollution"].max()),
                                          (int(df["WaterPollution"].min()), int(df["WaterPollution"].max())))

# Filter by selected ranges
df = df[(df["AirQuality"] >= air_quality_range[0]) & (df["AirQuality"] <= air_quality_range[1])]
df = df[(df["WaterPollution"] >= water_pollution_range[0]) & (df["WaterPollution"] <= water_pollution_range[1])]

# =============================
# Tabs
# =============================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Scatter Plot",
                                              "Bar Chart",
                                              "Correlation Heatmap",
                                              "Top 10 Cities (Air Quality)",
                                              "Worst 10 Cities (Water Pollution)",
                                              "Country Statistics"])

# =============================
# Tab 1: Scatter Plot
# =============================
with tab1:
    st.subheader("Air Quality vs Water Pollution")
    scatter = alt.Chart(df).mark_circle(size=100).encode(
        x=alt.X("AirQuality", scale=alt.Scale(zero=False)),
        y=alt.Y("WaterPollution", scale=alt.Scale(zero=False)),
        color="Country",
        tooltip=["City", "Country", "Region", "AirQuality", "WaterPollution"]
    ).interactive()
    st.altair_chart(scatter, use_container_width=True)

    st.markdown("""
    - Generally, cities with higher air quality tend to have lower water pollution levels.
    - Environmental policies may affect both air and water simultaneously.
    """)

# =============================
# Tab 2: Bar Chart
# =============================
with tab2:
    st.subheader("City Water Pollution Levels")
    bar = alt.Chart(df).mark_bar().encode(
        x=alt.X("City", sort="-y"),
        y="WaterPollution",
        color="Region",
        tooltip=["City", "WaterPollution"]
    ).interactive()
    st.altair_chart(bar, use_container_width=True)

# =============================
# Tab 3: Correlation Heatmap
# =============================
with tab3:
    st.subheader("Correlation between Features")
    if len(df) > 1:
        corr = df[['AirQuality', 'WaterPollution']].corr()
        fig, ax = plt.subplots()
        sns.heatmap(corr, annot=True, cmap="coolwarm", center=0, ax=ax)
        st.pyplot(fig)
    else:
        st.write("Not enough data to plot correlation heatmap.")

# =============================
# Tab 4: Top 10 Cities (Air Quality)
# =============================
with tab4:
    st.subheader("Top 10 Cities with Best Air Quality")
    top_cities = df.sort_values("AirQuality", ascending=False).head(10)
    st.dataframe(top_cities[["City", "Country", "Region", "AirQuality"]])

# =============================
# Tab 5: Worst 10 Cities (Water Pollution)
# =============================
with tab5:
    st.subheader("Top 10 Cities with Worst Water Pollution")
    worst_cities = df.sort_values("WaterPollution", ascending=False).head(10)
    st.dataframe(worst_cities[["City", "Country", "Region", "WaterPollution"]])

# =============================
# Tab 6: Country Level Stats
# =============================
with tab6:
    st.subheader("Aggregated Pollution Statistics by Country")
    country_stats = df.groupby("Country").agg({
        "AirQuality": "mean",
        "WaterPollution": "mean"
    }).reset_index().sort_values(by="AirQuality", ascending=False)
    st.dataframe(country_stats)

# =============================
# Download Button
# =============================
st.sidebar.subheader("📥 Download Filtered Data")
st.sidebar.download_button(
    label="Download CSV",
    data=df.to_csv(index=False).encode('utf-8'),
    file_name="filtered_pollution_data.csv",
    mime='text/csv'
)

# =============================
# Footer
# =============================
st.markdown("""---""")
st.markdown("""
✅ Developed for ITCS 5122 Visual Analytics  
✅ Built with Streamlit and Altair  
✅ Dataset: Global City Pollution Statistics
""")
