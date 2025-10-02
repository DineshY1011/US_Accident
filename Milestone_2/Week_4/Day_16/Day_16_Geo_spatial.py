import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

# Efficiently load a random sample of 5,000 rows from the large CSV
dataset_path = "C:/Users/dinesh/Documents/Infosys Springboard/Dataset/US_Accidents_March23.csv/US_Accidents_March23.csv"
total_rows = sum(1 for _ in open(dataset_path)) - 1  # minus header
sample_size = 5000

# Randomly select rows to skip (except header)
skip = sorted(np.random.choice(np.arange(1, total_rows + 1), total_rows - sample_size, replace=False))
df = pd.read_csv(dataset_path, skiprows=skip)

def plot_accidents_sampled(df, location_col='State', sample_size=5000):
    counts = df[location_col].value_counts().head(5)
    top5_locations = counts.index.tolist()
    df['is_top5'] = df[location_col].isin(top5_locations)

    fig = px.scatter(
        df,
        x='Start_Lng',
        y='Start_Lat',
        color='is_top5',
        labels={'Start_Lng': 'Longitude', 'Start_Lat': 'Latitude', 'is_top5': 'Top 5 Accident-Prone'},
        title=f'Accident Scatter Plot Highlighting Top 5 {location_col}s',
        opacity=0.6,
        hover_data=[location_col]
    )
    st.plotly_chart(fig)

st.title('Accident Data Visualization')

location_option = st.selectbox('Select Location Type', ['State', 'City'])

plot_accidents_sampled(df, location_col=location_option)

st.header("Hypothesis Testing")

# 1. What time of day has the most accidents?
st.subheader("1. What time of day has the most accidents?")
df['Hour'] = pd.to_datetime(df['Start_Time'], errors='coerce', format='mixed').dt.hour
hour_counts = df['Hour'].value_counts().sort_index()
fig1 = px.bar(x=hour_counts.index, y=hour_counts.values, labels={'x': 'Hour of Day', 'y': 'Number of Accidents'}, title='Accidents by Hour of Day')
st.plotly_chart(fig1)
st.write("Justification: By grouping accidents by hour, we can visually identify peak accident times, such as rush hours.")

# 2. Are accidents more severe during rain or fog?
st.subheader("2. Are accidents more severe during rain or fog?")
weather_severity = df[df['Weather_Condition'].isin(['Rain', 'Fog'])].groupby('Weather_Condition')['Severity'].mean()
fig2 = px.bar(x=weather_severity.index, y=weather_severity.values, labels={'x': 'Weather Condition', 'y': 'Average Severity'}, title='Average Severity: Rain vs Fog')
st.plotly_chart(fig2)
st.write("Justification: Comparing the average severity for 'Rain' and 'Fog' conditions helps determine if one weather type leads to more severe accidents.")

# 3. Is there a correlation between visibility and severity?
st.subheader("3. Is there a correlation between visibility and severity?")
fig3 = px.scatter(df, x='Visibility(mi)', y='Severity', trendline='ols', opacity=0.3, title='Visibility vs Severity')
st.plotly_chart(fig3)
correlation = df[['Visibility(mi)', 'Severity']].corr().iloc[0,1]
st.write(f"Correlation coefficient: {correlation:.2f}")
st.write("Justification: A scatter plot and correlation coefficient show if lower visibility is associated with higher accident severity.")

# 1. What time of day has the most accidents?
peak_hour = hour_counts.idxmax()
st.write(f"Most accidents occur at hour: {peak_hour}:00")

# 2. Are accidents more severe during rain or fog?
if len(weather_severity) == 2:
    if weather_severity['Rain'] > weather_severity['Fog']:
        st.write("Yes, accidents are more severe during Rain.")
    elif weather_severity['Rain'] < weather_severity['Fog']:
        st.write("Yes, accidents are more severe during Fog.")
    else:
        st.write("No, severity is the same for Rain and Fog.")
else:
    st.write("Insufficient data for Rain and Fog comparison.")

# 3. Is there a correlation between visibility and severity?
if abs(correlation) > 0.3:
    st.write(f"Yes, there is a correlation between visibility and severity (correlation coefficient: {correlation:.2f}).")
else:
    st.write(f"No, there is little to no correlation between visibility and severity (correlation coefficient: {correlation:.2f}).")