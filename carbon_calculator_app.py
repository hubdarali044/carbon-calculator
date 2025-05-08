
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Carbon Calculator", layout="centered")
st.title("🌍 Simple Carbon Consumption Calculator")

EMISSION_FACTORS = {
    'electricity': 0.233,
    'gas': 2.02,
    'diesel': 2.68,
    'gasoline': 2.31,
}

st.sidebar.header("Choose Input Mode")
mode = st.sidebar.radio("Mode", ["Manual Input", "Upload CSV"])

def calculate_emissions(df):
    df['electricity_emission'] = df['electricity'] * EMISSION_FACTORS['electricity']
    df['gas_emission'] = df['gas'] * EMISSION_FACTORS['gas']
    df['transport_emission'] = (df['distance'] / df['fuel_efficiency']) * df['fuel_type'].map(EMISSION_FACTORS)
    df['total_emission'] = df[['electricity_emission', 'gas_emission', 'transport_emission']].sum(axis=1)
    return df

if mode == "Manual Input":
    st.subheader("Enter Your Data")
    electricity = st.number_input("Electricity (kWh)", min_value=0.0)
    gas = st.number_input("Gas (m³)", min_value=0.0)
    distance = st.number_input("Distance (km)", min_value=0.0)
    fuel_type = st.selectbox("Fuel Type", ["gasoline", "diesel"])
    fuel_efficiency = st.number_input("Fuel Efficiency (km/l)", min_value=0.1)

    if st.button("Calculate"):
        df = pd.DataFrame([{
            'electricity': electricity,
            'gas': gas,
            'distance': distance,
            'fuel_type': fuel_type,
            'fuel_efficiency': fuel_efficiency,
        }])
        df = calculate_emissions(df)
        st.success(f"Total Emissions: {df['total_emission'].iloc[0]:.2f} kg CO₂")
        st.dataframe(df)

else:
    st.subheader("Upload Your CSV File")
    st.markdown("Required columns: `electricity`, `gas`, `distance`, `fuel_type`, `fuel_efficiency`")

    uploaded_file = st.file_uploader("Choose a file", type="csv")
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            df = calculate_emissions(df)
            st.success("Calculation Complete!")
            st.dataframe(df)
                    # 📊 Visualizations
    st.subheader("📈 Emissions Visualizations")

        # Line Chart if 'date' exists
        if 'date' in df.columns:
            try:
                df['date'] = pd.to_datetime(df['date'])
                df.set_index('date', inplace=True)
                st.line_chart(df[['electricity_emission', 'gas_emission', 'transport_emission', 'total_emission']])
            except:
                st.warning("⚠️ Could not parse 'date' column for time series chart.")

        # Bar Chart of emissions per row
        st.bar_chart(df[['electricity_emission', 'gas_emission', 'transport_emission']])

        # Pie Chart of total emissions by category
        totals = df[['electricity_emission', 'gas_emission', 'transport_emission']].sum()
        st.subheader("🥧 Emission Share by Category")
        st.pyplot(totals.plot.pie(autopct='%1.1f%%', ylabel='', figsize=(5, 5)).get_figure())

        except Exception as e:
            st.error(f"Error: {e}")
