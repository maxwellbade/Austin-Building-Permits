#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pandas_profiling import ProfileReport
from sodapy import Socrata

csv1 = 'https://data.austintexas.gov/resource/3syk-w9eu.csv'
all_data_exports = 'https://data.austintexas.gov/Building-and-Development/Issued-Construction-Permits/3syk-w9eu'
austin_data = 'https://data.austintexas.gov'

px.set_mapbox_access_token('pk.eyJ1IjoibWF4YmFkZSIsImEiOiJja2poa3Ixc2w5OHJ0MnNwZGVhNXlhdmprIn0.7Vxpd_-JanBsc8o2R3nzKg')

pd.set_option('display.max_columns', None)

# !ls -ltr | tail -20


# In[3]:


df = pd.read_csv('Issued_Construction_Permits-2.csv')
df.head()


# In[4]:


import requests
response = requests.get('https://data.austintexas.gov/resource/3syk-w9eu.csv')
print(response.status_code)


# In[18]:


#!/usr/bin/env python
#api version

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("data.austintexas.gov"
                 ,'your_app_token'
                 ,username="your_email"
                 ,password="your_password"
                )

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("3syk-w9eu"
                     , order='calendar_year_issued desc'
                     , where="calendar_year_issued in ('2013','2014','2015','2016','2017','2018','2019','2020','2021')"
                     , limit=20000 #something weird here - can't read data based on query parameters bc limit function seems to precede other functions
                    )

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)

del(results)

min_year = '2013-01-01'
zip_code = 78747

results_df['original_zip'] = results_df['original_zip'].fillna(0)
results_df['calendar_year_issued'] = results_df['calendar_year_issued'].astype(int)
results_df['original_zip'] = results_df['original_zip'].astype(int)
results_df['issue_date'] = results_df['issue_date'].astype('datetime64[ns]')

# results_df = results_df[results_df['issue_date'] >= min_year]
results_df = results_df[results_df['original_zip'] == zip_code]

results_df = results_df.reset_index()
results_df['count_permits'] = results_df.groupby('project_id')["index"].transform("count")

#Show df
print(results_df.shape)
results_df.head()


# In[19]:


#enter in the zipcode you want to search 
#and the earliest year for which you want to see data
min_year = 2013
zip_code = 78747
zip_codes = ['78747','78744','78617','78612','78616','78719']

df = df[df['Calendar Year Issued'] >= min_year]

# df = df[df['Permit Class Mapped'] == 'Commercial']

df1 = df[df['Original Zip'] == zip_code]
print(df1.shape)

df1 = df1.reset_index()

df1['count_permits'] = df1.groupby('Project Name')["index"].transform("count")

#display map
fig = px.scatter_mapbox(df1
                        , lat="Latitude"
                        , lon="Longitude"
                        , color="Calendar Year Issued"
                        , text='Description'
                        , size="count_permits"
                        , color_continuous_scale=px.colors.diverging.PRGn
                        , zoom=12
                        , height=900
                        , opacity=.15
                        , title='<b>Number of Permits by Zipcode</b>'
                        , template='seaborn'
                       )

fig1 = px.scatter_mapbox(df1
                        , lat="Latitude"
                        , lon="Longitude"
                        , color="Calendar Year Issued"
                        , text='Description'
                        , size="count_permits"
                        , color_continuous_scale=px.colors.diverging.PRGn
                        , zoom=12
                        , height=900
                        , opacity=.15
                        , title='<b>Number of Permits by Zipcode</b>'
                        , template='seaborn'
                       )

fig.update_layout(
    mapbox_style="open-street-map"
)

fig1.update_layout(
    mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "sourceattribution": "United States Geological Survey",
            "source": [
                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            ]
        },
        {
            "sourcetype": "raster",
            "sourceattribution": "Government of Canada",
            "source": ["https://geo.weather.gc.ca/geomet/?"
                       "SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&BBOX={bbox-epsg-3857}&CRS=EPSG:3857"
                       "&WIDTH=1000&HEIGHT=1000&LAYERS=RADAR_1KM_RDBR&TILED=true&FORMAT=image/png"],
        }
      ]
)

fig.show()
fig1.show()


# In[21]:


#enter in the zipcode you want to search 
#and the earliest year for which you want to see data
min_year = 2013
zip_code = 78610
zip_codes = ['78747','78744','78617','78612','78616','78719']

df = df[df['Calendar Year Issued'] >= min_year]

# df = df[df['Permit Class Mapped'] == 'Commercial']

df1 = df[df['Original Zip'] == zip_code]
print(df1.shape)

df1 = df1.reset_index()

df1['count_permits'] = df1.groupby('Project Name')["index"].transform("count")

#display map
fig = px.scatter_mapbox(df1
                        , lat="Latitude"
                        , lon="Longitude"
                        , color="Calendar Year Issued"
                        , text='Description'
                        , size="count_permits"
                        , color_continuous_scale=px.colors.diverging.PRGn
                        , zoom=12
                        , height=900
                        , opacity=.15
                        , title='<b>Number of Permits by Zipcode</b>'
                        , template='seaborn'
                       )

fig1 = px.scatter_mapbox(df1
                        , lat="Latitude"
                        , lon="Longitude"
                        , color="Calendar Year Issued"
                        , text='Description'
                        , size="count_permits"
                        , color_continuous_scale=px.colors.diverging.PRGn
                        , zoom=12
                        , height=900
                        , opacity=.6
                        , title='<b>Number of Permits by Zipcode</b>'
                        , template='seaborn'
                       )

fig.update_layout(
    mapbox_style="open-street-map"
)

fig1.update_layout(
    mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "sourceattribution": "United States Geological Survey",
            "source": [
                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            ]
        },
        {
            "sourcetype": "raster",
            "sourceattribution": "Government of Canada",
            "source": ["https://geo.weather.gc.ca/geomet/?"
                       "SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&BBOX={bbox-epsg-3857}&CRS=EPSG:3857"
                       "&WIDTH=1000&HEIGHT=1000&LAYERS=RADAR_1KM_RDBR&TILED=true&FORMAT=image/png"],
        }
      ]
)

fig.show()
fig1.show()


# # Profiling the data
# ### finds duplicates, nulls etc.

# In[14]:


profile = ProfileReport(df1
                        , title='Pandas Profiling Report'
                        , explorative=True
                       )
profile


# # Testing stuff out

# In[33]:


df.info()


# In[45]:


df['Fiscal Year Issued'].unique()
df['Fiscal Year Issued'].value_counts().sort_values().tail(10)


# In[46]:


df['Calendar Year Issued'].unique()
df['Calendar Year Issued'].value_counts().sort_values().tail(10)


# In[59]:


df['Permit Class Mapped'].unique()
df = df[df['Permit Class Mapped'] == 'Commercial']
df.describe


# In[61]:


zipcodes = ['78747','78744','78617','78612','78616','78719']


# In[9]:


df1 = df[df['Original Zip'] == 78747]
print(df1.shape)
df1.head()


# In[87]:


df1['Calendar Year Issued'] = df1['Calendar Year Issued'].astype(int)
# print(df1.info())


# In[47]:


df1['#_of_permits'] = df1.groupby('Project Name')['index'].count()
df1


# In[30]:


import plotly.graph_objects as go
import plotly.express as px

px.set_mapbox_access_token('pk.eyJ1IjoibWF4YmFkZSIsImEiOiJja2poa3Ixc2w5OHJ0MnNwZGVhNXlhdmprIn0.7Vxpd_-JanBsc8o2R3nzKg')

fig = go.Figure(data=go.Scattergeo(
        lon = df1['Longitude'],
        lat = df1['Latitude'],
        text = df1['Description'],
        mode = 'markers',
        marker_color = df1['Calendar Year Issued'],
        ))

fig.update_layout(
        title = 'Austin 78747 Building Permits',
        geo_scope='usa',
    )

fig.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




