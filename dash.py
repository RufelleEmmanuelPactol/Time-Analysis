import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

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

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
)

header_html = """
    <div style='
        text-align: center;
        color: #004080;
        background-color: #ADD8E6;
        padding: 5px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        '>
        <h1>
            Team Mang Activity Log Analysis For two weeks
        </h1>
    </div>
"""
# Use st.markdown to display the HTML content
st.markdown(header_html, unsafe_allow_html=True)


# Define a custom color sequence or use Plotly's default colors
plotly_colors = px.colors.qualitative.Set1

# Define a color-blind-friendly color palette for Plotly Express
color_blind_palette = px.colors.colorbrewer.Paired

# Streamlit app layout with HTML-formatted title
st.markdown("<h2 style='text-align: center; color: #ADD8E6;'>Activity and Emotion Distribution Analysis</h2>", unsafe_allow_html=True)

def create_emotion_activity_chart(crosstab, background_color='white'):
    fig = go.Figure()
    for col in crosstab.columns:
        fig.add_trace(go.Bar(x=crosstab.index, y=crosstab[col], name=col))
    fig.update_layout(title='Relationship between Activity Type and Emotion', xaxis_title='Activity Type', yaxis_title='Emotion Count', plot_bgcolor=background_color)
    st.plotly_chart(fig)


# Define function to create a weighted pie chart based on activity duration
def create_weighted_pie_chart(data, title, background_color='white'):
    weighted_counts = data.groupby('Mapped Activity')['Duration'].sum().reset_index()

    total_duration = data.groupby('Mapped Activity')['Duration'].sum().reset_index()

    sorted_data = total_duration.sort_values(by = 'Duration', ascending=True)

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
        return "Dawn"

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
    fig = px.bar(emotion_day_crosstab, x=emotion_day_crosstab.index, y=emotion_day_crosstab.columns, barmode='stack')
    fig.update_layout(title='Emotions Felt Throughout the Day', xaxis_title='Part of Day', yaxis_title='Count of Emotions', plot_bgcolor=background_color)
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


# List of options for the drop-down menu
activity_options = ['Pactol', 'Alcordo', 'Guinita']

# User selects an option from the drop-down menu


# Aggregated Activity Distribution
aggregated_pie_chart = create_weighted_pie_chart(all_data, 'Aggregated Activity Distribution')

# Aggregated Emotion Analysis
emotion_chart = create_weighted_emotion_activity_chart(all_data)

# Emotions Felt Throughout the Day
emotion_day_chart = create_emotion_day_chart(all_data)

# Activity Association with Value
activity_value_chart = create_weighted_activity_value_chart(all_data)


# Create containers to organize charts in rows and columns
col1, col2= st.columns(2)
    
with col1:
    activity_options = ['Pactol', 'Alcordo', 'Guinita']
    selected_activity = st.selectbox('Select Activity', activity_options)
    # Display the selected report based on the user's choice
    if selected_activity == 'Pactol':
        weighted_pie_chart = create_weighted_pie_chart(data_pactol, "Pactol's Activity Distribution")
    elif selected_activity == 'Alcordo':
        weighted_pie_chart = create_weighted_pie_chart(data_alocardo, "Alcordo's Activity Distribution")
    elif selected_activity == 'Guinita':
        weighted_pie_chart = create_weighted_pie_chart(data_guinita, "Guinita's Activity Distribution")
    st.plotly_chart(weighted_pie_chart, use_container_width=True)        

with col2:
    st.plotly_chart(aggregated_pie_chart, use_container_width=True)

    

with st.container():
    col3, col4 = st.columns(2)

    with col3:
        st.plotly_chart(emotion_chart)

    with col4:
        st.plotly_chart(emotion_day_chart)

with st.container():
    col5, col6, col7 = st.columns(3)

    with col5:
        st.write("")
        with col6: 
            st.plotly_chart(activity_value_chart)