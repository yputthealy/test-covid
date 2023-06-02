import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
import plotly_express as px
import os.path, time

'''
# Coronavirus Live Stats

This app accepts country or metric name and displays current live coronavirus stats from www.worldometers.info.
'''

@st.cache_data
def get_lat_lon():
    '''
    Queries Google's countries_csv page, scapes for country coordinates and returns dataframe
    `coord_df` with columns lat, lon and Country with the former two columns as float.
    '''
    urlpage =  'https://developers.google.com/public-data/docs/canonical/countries_csv'
    # query the website and return the html to the variable 'page'
    page = urllib.request.urlopen(urlpage)
    # parse the html using beautiful soup and store in variable 'soup'
    soup = BeautifulSoup(page, 'html.parser')

    # find results within table
    country_coords = []
    for table in soup.find_all('table'):
        # find all columns per result
        data = table.find_all('tr')
        # check that columns have data 
        if len(data) == 0: 
            continue
        else:
            for i,row in enumerate(data):
                # skip first row for 'th' column header row
                if i == 0:
                    continue
                cells = row.find_all('td')
                country_info = [cell.get_text().strip('\n').replace(",","") for cell in cells]
                country_info.pop(0)
                country_coords.append(country_info)

    coord_df = pd.DataFrame(country_coords,columns=['lat','lon','Country'])
    coord_df.drop(index=226,inplace=True) # remove U.S. Minor Outlying Islands
    coord_df[['lat','lon']] = coord_df[['lat','lon']].astype(float)
    return coord_df

@st.cache_data
def get_virus_data():
    '''
    Queries www.worldometers.info for covid-19 current stats, scrapes table with id 'table3'
    and returns dataframe `merged_df` after merging location data.
    '''
    urlpage =  'https://www.worldometers.info/coronavirus/'
    # query the website and return the html to the variable 'page'
    page = urllib.request.urlopen(urlpage)
    # parse the html using beautiful soup and store in variable 'soup'
    soup = BeautifulSoup(page, 'html.parser')

    # find results within table
    data_content = []
    for table in soup.find_all('table', attrs={'id': 'table3'}):
        # find all columns per result
        data = table.find_all('tr')
        # check that columns have data 
        if len(data) == 0: 
            continue
        else:
            for i,row in enumerate(data):
                if i == 0:
                    continue
                cells = row.find_all('td')
                country_info = [cell.get_text().strip('+\n ').replace(",","") for cell in cells]
                data_content.append(country_info)
    df = pd.DataFrame(data_content,columns=['Country','CaseCount','TodaysCases','TotalDealths','TodaysDeath','RecoveredCount','SevereCount','Region'])
    # update country names on worldometers to match Google's data
    df.loc[df.Country == "S. Korea",'Country'] = "South Korea"
    df.loc[df.Country == "USA",'Country'] = "United States"
    df.loc[df.Country == "U.K.",'Country'] = "United Kingdom"
    df.loc[df.Country == "U.A.E.",'Country'] = "United Arab Emirates"

    # replace all blank cells with 0
    df.replace(r'^\s*$', 0, regex=True, inplace=True)
    # column number columns to numeric`
    for col in df.columns[1:df.shape[1]-1]:
        df[col] = pd.to_numeric(df[col])

    # get lat/lon from google and merge with virus df
    coords_df = get_lat_lon()
    merged_df = df.merge(coords_df, left_on='Country', right_on='Country', how='inner')

    return merged_df

@st.cache_data
def color_stats(val):
    '''
    Takes a string and returns a string with the css property `'color: red'` 
    for column 'TotalDealths'.
    '''
    return 'color: red'

df = get_virus_data()
countrySelected = False

st.sidebar.subheader("Choose Criteria for Display") 
regions = st.sidebar.multiselect('Select a region(s)', df['Region'].unique(),key="1")
new_df = df[df['Region'].isin(regions)]
countries = st.sidebar.multiselect('Select one or more countries', new_df['Country'],key="2")
pick_all_countries = st.sidebar.checkbox(' or all countries')
if not pick_all_countries:
    if countries:
        new_df = new_df[new_df['Country'].isin(countries)]
        countrySelected = True
else:
    countrySelected = True
metric_columns = ['CaseCount','TodaysCases','TotalDealths','TodaysDeath','RecoveredCount','SevereCount']
metric = st.sidebar.multiselect('Select metric', metric_columns,default=['CaseCount'],key="3")

curr_time = time.strftime("%d-%b-%Y %H:%M:%S", time.gmtime())
st.sidebar.markdown('<br/><br/><font size="2">Data last updated :date:: <b>'+curr_time+"</b></font>",unsafe_allow_html=True)

st.subheader('Selected countries')

# display max score filter only when cases are selected
if regions and countrySelected and metric:
    st.dataframe(new_df.style.applymap(color_stats,subset=['TotalDealths']))
    st.subheader(str(metric[0])+' for selected countries')
    fig1 = px.scatter(new_df, x="Country", y=metric[0], color="Country")
    fig1.update_layout(yaxis_type="log")
    st.plotly_chart(fig1)

    # plot map
    country_to_focus = new_df['Country'].unique()[0]
    st.deck_gl_chart(
        viewport={
            'zoom': 3,
            'latitude':new_df[new_df['Country'] == country_to_focus]['lat'].values[0],
            'longitude':new_df[new_df['Country'] == country_to_focus]['lon'].values[0],
            'pitch': 10,
        },
        layers=[{
            'type': 'ScatterplotLayer',
            'data': new_df,
            'radiusScale': 1000,
            'radiusMaxPixels': 100,
            'getRadius': metric[0],
        }])
