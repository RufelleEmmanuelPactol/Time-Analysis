import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Define emotion mapping
emotion_mapping = {
    'Tired': 'Negative',
    'Refreshed': 'Positive',
    'Relaxed': 'Positive',
    'Stressed': 'Negative',
    'Sleepy': 'Negative',
    'Normal': 'Neutral',
    'Happy': 'Strongly Positive',
    'Bored': 'Negative',
    'Fine': 'Neutral'
    # Add more mappings if necessary
}

# Define function to create the emotion-activity bar chart
def create_emotion_activity_chart(crosstab, background_color='white'):
    fig, ax = plt.subplots(figsize=(10, 6))
    crosstab.plot(kind='bar', stacked=True, ax=ax)
    plt.title('Relationship between Activity Type and Emotion')
    plt.xlabel('Activity Type')
    plt.ylabel('Emotion Count')
    fig.patch.set_facecolor(background_color)
    return fig

# Define function to create a pie chart for the mapped activity distribution
def create_pie_chart(data, title, background_color='white'):
    activity_counts = data['Mapped Activity'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(activity_counts, labels=activity_counts.index, autopct='%1.1f%%', startangle=90)
    plt.title(title)
    fig.patch.set_facecolor(background_color)
    return fig

def categorize_time_of_day(time_str):
    try:
        time_obj = pd.to_datetime(time_str, format='%H:%M').time()
    except ValueError:
        # Return 'Unknown' if time_str is not a valid time
        return "Unknown"

        # Return the part of the day based on the time
    if time_obj.hour < 6:
        return "Night"
    elif 6 <= time_obj.hour < 12:
        return "Morning"
    elif 12 <= time_obj.hour < 17:
        return "Afternoon"
    elif 17 <= time_obj.hour < 21:
        return "Evening"
    else:  # From 9 PM to 6 AM
        return "Night"

def create_emotion_day_chart(data, background_color='white'):
    # Categorize the time of day and then map emotions
    data['Part of Day'] = data['Time'].apply(categorize_time_of_day)
    emotion_day_crosstab = pd.crosstab(data['Part of Day'], data['Emotion Category'])
    fig, ax = plt.subplots()
    emotion_day_crosstab.plot(kind='bar', stacked=True, ax=ax)
    plt.title('Emotions Felt Throughout the Day')
    plt.xlabel('Part of Day')
    plt.ylabel('Count of Emotions')
    fig.patch.set_facecolor(background_color)
    return fig

# Define function to create a chart for activity-value association
def create_activity_value_chart(data, background_color='white'):
    activity_value_crosstab = pd.crosstab(data['Mapped Activity'], data['Value'])
    fig, ax = plt.subplots()
    activity_value_crosstab.plot(kind='bar', stacked=True, ax=ax)
    plt.title('Activity Association with Value')
    plt.xlabel('Activity')
    plt.ylabel('Value Count')
    fig.patch.set_facecolor(background_color)
    return fig

# Load the datasets from an Excel file with multiple sheets
data_pactol = pd.read_excel('compiled_data.xlsx', sheet_name='PACTOL')
data_alocardo = pd.read_excel('compiled_data.xlsx', sheet_name='Alocardo')
data_guinita = pd.read_excel('compiled_data.xlsx', sheet_name='Guinita')

# Apply emotion mapping
data_pactol['Emotion Category'] = data_pactol['How I feel'].map(emotion_mapping)
data_alocardo['Emotion Category'] = data_alocardo['How I feel'].map(emotion_mapping)
data_guinita['Emotion Category'] = data_guinita['How I feel'].map(emotion_mapping)

# Combine all data for the aggregated analysis
all_data = pd.concat([data_pactol, data_alocardo, data_guinita])

# Create the crosstab for emotion analysis
emotion_activity_crosstab = pd.crosstab(all_data['Mapped Activity'], all_data['Emotion Category'])

# Streamlit app layout

st.title('Activity and Emotion Distribution Analysis')
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Individual Distributions", "Aggregated Distribution", "Emotion Analysis", "Emotion Through Day", "Activity and Value"])


with tab1:
    st.header('PACTOL Activity Distribution')
    st.pyplot(create_pie_chart(data_pactol, 'PACTOL Activity Distribution'))

    st.header('Alocardo Activity Distribution')
    st.pyplot(create_pie_chart(data_alocardo, 'Alocardo Activity Distribution'))

    st.header('Guinita Activity Distribution')
    st.pyplot(create_pie_chart(data_guinita, 'Guinita Activity Distribution'))

with tab2:
    st.header('Aggregated Activity Distribution')
    st.pyplot(create_pie_chart(all_data, 'Aggregated Activity Distribution'))

with tab3:
    st.header('Aggregated Emotion Analysis')
    st.pyplot(create_emotion_activity_chart(emotion_activity_crosstab))

with tab4:
    st.header('Emotions Felt Throughout the Day')
    st.pyplot(create_emotion_day_chart(all_data))

with tab5:
    st.header('Activity Association with Value')
    st.pyplot(create_activity_value_chart(all_data))
