import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
import xarray as xr
import yaml
import plotly.graph_objects as go
from matplotlib.colors import to_rgba
import plotly.express as px
import math
import plotly.offline as pltly

import sys
sys.path.insert(0, "..")
from utils import plot

import matplotlib.pyplot as plt

import pypsa

ng_model_location = "./results/NG/networks/elec_s_10_ec_lcopt_Co2L-4H.nc"
big_model_location = "./results/BIG/networks/elec_s_10_ec_lcopt_Co2L-4H.nc"

n = pypsa.Network(ng_model_location)

with st.sidebar:
    st.title("PyPSA-Earth Sample Network Analysis")

    genre = st.radio(
    "Select a graph:",
    ('no_oil', 'with_oil'))





option = st.selectbox(
    'How would you like to be contacted?',
    ('Capital Expenditure', 'Installed Capacity', 'Operational Expenditure','Revenue','Optimal Capacity'))

st.write('You selected:', option)


ylabel=""
if(option == 'Capital Expenditure'or option == 'Operational Expenditure' or option == 'Revenue'):
    ylabel = "Euro"
else:
    ylabel = "MW"

# if(genre == 'no_oil'):
#     fig=px.bar(n.statistics()[[x != 1 and not math.isnan(x) for x in n.statistics()[option]]][option].loc
#     ['Generator'].drop('load', errors='ignore'),color='value',
#            labels={
#                      "carrier": "type of generator",
#                      "value": ylabel,
#                      })
#     st.plotly_chart(fig, use_container_width=True)
#     # 
#     fig=px.bar(n.carriers[n.carriers["co2_emissions"]!=0]["co2_emissions"])
#     st.plotly_chart(fig, use_container_width=True)
# else:
#     fig=px.bar(n1.statistics()[[x != 0 and not math.isnan(x) for x in n1.statistics()[option]]][option].loc
#     ['Generator'].drop('load', errors='ignore'),color='value',
#               labels={
#                         "carrier": "type of generator",
#                          "value": ylabel,
#                      })
#     st.plotly_chart(fig, use_container_width=True)       
#     # 
#     fig=px.bar(n1.carriers[n1.carriers["co2_emissions"]!=0]["co2_emissions"],color='value')
#     st.plotly_chart(fig , use_container_width=True)
df = pd.DataFrame()
df["x"] = n.buses["x"]
df["y"] = n.buses["y"]
df["name"] = n.buses.index
import json
nigeria_boundries = json.load(open("nigeria_geojson.geojson"))
fig = px.scatter_geo(df, lat="y", lon="x", geojson=nigeria_boundries, featureidkey="properties.state", hover_name="name")
fig.update_geos(fitbounds="geojson", scope="africa", projection_type="conic equidistant")
st.plotly_chart(fig, use_container_width=True)

# fig = plot.plot(n, geomap=True, color_geomap=True)

