import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import hydralit_components as hc
import requests
from PIL import Image
import plotly.express as px
import os
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

with open('data.csv', 'rb') as file:
    content = file.read().decode('utf-8', errors='replace')

from io import StringIO
data = pd.read_csv(StringIO(content))


# Set Page Icon,Title, and Layout
st.set_page_config(layout="wide",  page_title = "Global Terrorism")

# Load css style file from local disk
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)
# Load css style from url
def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">',unsafe_allow_html = True)

# Display lottie animations
def load_lottieurl(url):
    # get the url
    r = requests.get(url)
    # if error 200 raised return Nothing
    if r.status_code !=200:
        return None
    return r.json()

    # Navigation Bar Design
menu_data = [
{'label':"Home", 'icon': "bi bi-house"},
{'label':"EDA", 'icon': "bi bi-clipboard-data"},]

over_theme = {'txc_inactive': 'white','menu_background':'#0178e4', 'option_active':'white'}
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    hide_streamlit_markers=True,
    sticky_nav=True,
    sticky_mode='sticky',
)

# Home Page
if menu_id == "Home":
    st.markdown("<hr style='border-top: 3px solid black;'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: red;'>Global Terrorism <i class='bi bi-heart-fill' style='color: red;'></i> </h2>", unsafe_allow_html=True)
    st.markdown("<hr style='border-top: 3px solid black;'>", unsafe_allow_html=True)
   
# Splitting page into 2 columns
    col1, col2 = st.columns([1,2])
    with col1:
        image = Image.open("pic1.jpg")
    # Display the image in the dashboard
        st.image(image)

    with col2:
        # Space and header
        st.markdown(" ")
        st.markdown("<h2>Course Data Visualization  : Assignment 2</h2>", unsafe_allow_html=True)
        st.markdown(" ")

        # Content with bullet points
        st.markdown("""
            <div style='text-align: justify'>
                <ul>
                    <li><h3>The Global Terrorism Database (GTD) is an open-source database from KAGGLE including information on terrorist attacks around the world from 1970 through 2017.</h3></li>
                    <li><h3>The GTD includes systematic data on domestic as well as international terrorist incidents that have occurred during this time period.</h3></li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

if menu_id == "EDA":
    with open('data.csv', 'rb') as file:
        content = file.read().decode('utf-8', errors='replace')

    from io import StringIO
    df = pd.read_csv(StringIO(content))

    # Sidebar
    st.sidebar.header("Choose your filter:")
        
    # Filtering by year
    selected_year = st.sidebar.slider('Year', min(df['iyear']), max(df['iyear']), min(df['iyear']))
    df = df[df['iyear'] == selected_year]
        
    # Filtering by region
    regions = st.sidebar.multiselect('Select Region(s)', df['region_txt'].unique())
    if regions:
        df = df[df['region_txt'].isin(regions)]

    #Visualization Columns
    col1, col2 = st.columns(2)
    with col1:
            fig = px.histogram(df, x='imonth', nbins=12, title=f'Number of Events in {selected_year}')
            st.plotly_chart(fig)

    with col2:
            fig2 = px.scatter_geo(df, lat='latitude', lon='longitude', hover_name='city', hover_data=['country_txt', 'attacktype1_txt'], title='Events on Map')
            st.plotly_chart(fig2)

    col3, col4 = st.columns(2)
    with col3:
            fig3 = px.histogram(df, x='attacktype1_txt', title='Number of Events by Attack Type')
            st.plotly_chart(fig3)

    with col4:
            region_nationality_counts = df.groupby(['region_txt', 'natlty1_txt']).size().reset_index(name='Count')
            fig_sunburst = px.sunburst(
                region_nationality_counts,
                path=['region_txt', 'natlty1_txt'],
                values='Count',
                title='Distribution of Nationalities of Attackers by Region',
            )
            st.plotly_chart(fig_sunburst)

    col5, col6 = st.columns(2)
    with col6:
        propextent_categories = df['propextent_txt'].unique()
        weapon_propextent_counts = df.groupby(['weaptype1_txt', 'propextent_txt']).size().reset_index(name='Count')
        pivot_df = pd.pivot_table(weapon_propextent_counts, values='Count', columns='weaptype1_txt', index='propextent_txt', fill_value=0)
        pivot_df = pivot_df.reindex(propextent_categories, fill_value=0)
        label_mapping = {
            'Minor (likely < $1 million)': 'minor',
            'Major (likely >= $1 million but < $1 billion)': 'major',
            'Unknown': 'unknown'
            }
        pivot_df.index = pivot_df.index.map(label_mapping)
        fig = px.bar(
            pivot_df,
            x=pivot_df.index,
            y=pivot_df.columns,
            title='Weapons Used in Relation to Property Damage Extent',
            labels={'value': 'Number of Attacks'},
            )
        fig.update_layout(barmode='stack')
        fig.update_xaxes(title_text='Property Damage Extent')
        st.plotly_chart(fig)

        # Define a list of attack types to visualize
        attack_types = ['Assassination', 'Armed Assault', 'Facility/Infrastructure Attack', 'Bombing/Explosion']

        # Create an empty DataFrame to store the results
        results = pd.DataFrame()
     
    with col5:
        # Group data by weapon type and count the occurrences
        weapon_counts = df['weaptype1_txt'].value_counts().reset_index()
        weapon_counts.columns = ['Weapon Type', 'Count']

        # Creating a pie chart using Plotly Express
        fig = px.pie(
            weapon_counts,
            names='Weapon Type',  # defining the categories (different weapon types)
            values='Count',       # defining the size of each pie slice
            title='Distribution of Attacks by Weapon Type'
        )

        # Optionally customize the chart look
        fig.update_traces(textinfo='percent+label')

        # Displaying the pie chart in Streamlit
        st.plotly_chart(fig)