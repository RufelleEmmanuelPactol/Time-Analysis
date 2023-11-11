import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Define the emotion mapping
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

# Define a custom color sequence or use Plotly's default colors
plotly_colors = px.colors.qualitative.Set1

# Define a color-blind-friendly color palette for Plotly Express
color_blind_palette = px.colors.colorbrewer.Paired

import plotly.graph_objects as go

def create_emotion_activity_chart(crosstab, background_color='white'):
    fig = go.Figure()
    for col in crosstab.columns:
        fig.add_trace(go.Bar(x=crosstab.index, y=crosstab[col], name=col))
    fig.update_layout(title='Relationship between Activity Type and Emotion', xaxis_title='Activity Type', yaxis_title='Emotion Count', plot_bgcolor=background_color)
    st.plotly_chart(fig)


# Define function to create a weighted pie chart based on activity duration
def create_weighted_pie_chart(data, title, background_color='white'):
    weighted_counts = data.groupby('Mapped Activity')['Duration'].sum().reset_index()
    fig = px.pie(weighted_counts, values='Duration', names='Mapped Activity', title=title, 
                 color_discrete_sequence=color_blind_palette, hover_data=['Duration'],
                 height=650, width=700)
    
    # Adjust percentage label size
    fig.update_traces(textinfo='percent+label', insidetextfont=dict(size=14))
    
    return fig

# Define function to create a weighted emotion-activity bar chart
def create_weighted_emotion_activity_chart(data, background_color='white'):
    data['Weight'] = data['Duration'] / data['Duration'].sum()
    weighted_crosstab = pd.crosstab(data['Mapped Activity'], data['Emotion Category'], values=data['Weight'], aggfunc='sum', normalize='index')
    fig = px.bar(weighted_crosstab, barmode='stack', title='Weighted Relationship between Activity Type and Emotion', 
                 labels={'value': 'Proportion of Time', 'index': 'Activity'})
    fig.update_layout(plot_bgcolor=background_color)
    return fig

# Define function to create a weighted activity-value bar chart
def create_weighted_activity_value_chart(data, background_color='white'):
    data['Weight'] = data['Duration'] / data['Duration'].sum()
    weighted_crosstab = pd.crosstab(data['Mapped Activity'], data['Value'], values=data['Weight'], aggfunc='sum', normalize='index')
    fig = px.bar(weighted_crosstab, barmode='stack', title='Weighted Activity Association with Value', 
                 labels={'value': 'Proportion of Time', 'index': 'Activity'})
    fig.update_layout(plot_bgcolor=background_color)
    return fig

# Load the datasets from an Excel file with multiple sheets
data_pactol = pd.read_excel('compiled_data.xlsx', sheet_name='PACTOL')
data_alocardo = pd.read_excel('compiled_data.xlsx', sheet_name='Alocardo')
data_guinita = pd.read_excel('compiled_data.xlsx', sheet_name='Guinita')

# Apply emotion mapping
data_pactol['Emotion Category'] = data_pactol['How I feel'].map(emotion_mapping)
data_alocardo['Emotion Category'] = data_alocardo['How I feel'].map(emotion_mapping)
data_guinita['Emotion Category'] = data_guinita['How I feel'].map(emotion_mapping)

# Assume 'Duration' column is already in minutes as integers for all datasets
# Combine all data for the aggregated analysis
all_data = pd.concat([data_pactol, data_alocardo, data_guinita])

# Streamlit app layout
st.title('Activity and Emotion Distribution Analysis')
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Individual Distributions", "Aggregated Distribution", "Emotion Analysis", "Emotion Through Day", "Activity and Value"])


def create_emotion_activity_chart(crosstab):
    fig, ax = plt.subplots(figsize=(10, 6))
    crosstab.plot(kind='bar', stacked=True, ax=ax)
    plt.title('Relationship between Activity Type and Emotion')
    plt.xlabel('Activity Type')
    plt.ylabel('Emotion Count')
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

import plotly.express as px

def create_emotion_day_chart(data, background_color='white'):
    # Categorize the time of day and then map emotions
    data['Part of Day'] = data['Time'].apply(categorize_time_of_day)
    emotion_day_crosstab = pd.crosstab(data['Part of Day'], data['Emotion Category'])
    fig = px.bar(emotion_day_crosstab, x=emotion_day_crosstab.index, y=emotion_day_crosstab.columns, barmode='stack')
    fig.update_layout(title='Emotions Felt Throughout the Day', xaxis_title='Part of Day', yaxis_title='Count of Emotions', plot_bgcolor=background_color)
    return fig


with tab1:
    st.header('PACTOL Activity Distribution')
    st.plotly_chart(create_weighted_pie_chart(data_pactol, 'PACTOL Activity Distribution'))

    st.header('Alcordo Activity Distribution')
    st.plotly_chart(create_weighted_pie_chart(data_alocardo, 'Alcordo Activity Distribution'))

    st.header('Guinita Activity Distribution')
    st.plotly_chart(create_weighted_pie_chart(data_guinita, 'Guinita Activity Distribution'))

with tab2:
    st.header('Aggregated Activity Distribution')
    st.plotly_chart(create_weighted_pie_chart(all_data, 'Aggregated Activity Distribution'))

with tab3:
    st.header('Aggregated Emotion Analysis')
    st.plotly_chart(create_weighted_emotion_activity_chart(all_data))

with tab4:
    st.header('Emotions Felt Throughout the Day')
    st.plotly_chart(create_emotion_day_chart(all_data))

with tab5:
    st.header('Activity Association with Value')
    st.plotly_chart(create_weighted_activity_value_chart(all_data))

# Make sure to replace 'compiled_data.xlsx' with the correct path to your Excel file.
