import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('health_dataset_final.csv')

# Print the columns to debug (optional)
st.write("Columns in the dataset:", df.columns.tolist())

# BMI Calculation if not already present
if 'BMI' not in df.columns:
    df['BMI'] = df['Weight_kg'] / (df['Height_m'] ** 2)

# Categorize BMI
def categorize_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"

df['BMI_Category'] = df['BMI'].apply(categorize_bmi)

# Find the correct Blood Sugar column
possible_columns = ['Blood Sugar', 'Blood_Sugar', 'Blood_Sugar_mg/dL', 'Blood_Sugar_level', 'Blood Sugar (mg/dL)']
blood_sugar_column = None
for col in possible_columns:
    if col in df.columns:
        blood_sugar_column = col
        break

# Streamlit App
st.title("Health Data Analysis Dashboard")
st.subheader("Exploratory Data Analysis")

# Show raw data
if st.checkbox("Show Raw Data"):
    st.dataframe(df)

# Plot BMI Distribution
st.subheader("BMI Distribution")
plt.figure(figsize=(10,6))
sns.histplot(df['BMI'], bins=30, kde=True)
plt.title("BMI Distribution")
st.pyplot(plt)

# Show BMI Categories Count
st.subheader("BMI Categories")
bmi_count = df['BMI_Category'].value_counts()
st.bar_chart(bmi_count)

# Blood Sugar Alert Section
if blood_sugar_column:
    st.subheader("High Blood Sugar Alerts (Above 140 mg/dL)")
    high_blood_sugar = df[df[blood_sugar_column] > 140]

    st.write(f"Total patients with high blood sugar: {high_blood_sugar.shape[0]}")
    st.dataframe(high_blood_sugar)
else:
    st.warning("Blood Sugar column not found in the dataset!")

# Summary Statistics
st.subheader("Summary Statistics")
st.write(df.describe())

st.success("Analysis Completed Successfully!")