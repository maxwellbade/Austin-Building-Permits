#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pandas_profiling import ProfileReport

px.set_mapbox_access_token('pk.eyJ1IjoibWF4YmFkZSIsImEiOiJja2poa3Ixc2w5OHJ0MnNwZGVhNXlhdmprIn0.7Vxpd_-JanBsc8o2R3nzKg')

pd.set_option('display.max_columns', None)

# !ls -ltr | tail -20


# In[2]:


df = pd.read_csv('Issued_Construction_Permits-2.csv')
df.head()


# In[4]:


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




