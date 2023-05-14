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
from utils import tools

import matplotlib.pyplot as plt
import json

import pypsa

ng_model_location = "./results/NG/networks/elec_s_10_ec_lcopt_Co2L-4H.nc"
big_model_location = "./results/BIG/networks/elec_s_10_ec_lcopt_Co2L-4H.nc"



with st.sidebar:
    st.title("PyPSA-Earth Sample Network Analysis")

    genre = st.radio(
    "Select a graph:",
    ('no_oil', 'with_oil'))

if(genre == 'no_oil'):
    n = pypsa.Network(big_model_location)
else:
    n = pypsa.Network(ng_model_location)

options = st.multiselect(
    'select features',
    ['lines', 'generators'])




nigeria_boundries = json.load(open("nigeria_geojson.geojson"))

df=tools.get_sctter_points(n)

if(options.__contains__("generators")):
    fig = px.scatter_mapbox(df, lat="y", lon="x", hover_name="name",size="size" ,color="size",opacity=1)

else:
    fig = px.scatter_mapbox(df, lat="y", lon="x", hover_name="name",size="size" ,color="size",opacity=0)

# create line traces to figure
line_df = tools.get_lines(n)

if(options.__contains__("lines")):
    for i in range(len(line_df)):
        s_nom = line_df["width"][i]
        fig.add_trace(
            go.Scattermapbox(
                lon=[line_df["source_x"][i], line_df["destination_x"][i]],
                lat=[line_df["source_y"][i], line_df["destination_y"][i]],
                mode="lines",
                line=dict(width=line_df["width"][i]/800),
                hovertemplate=f"s_nom: {s_nom:.2f},   name: {line_df['index'][i]}",
                hovertext=line_df["width"][i],
                name=line_df["index"][i],
                hoverinfo ="all",
                showlegend=False,
            )
        )

fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=4.5, mapbox_center={"lat": sum(df["y"])/len(df), "lon": sum(df["x"])/len(df)})

st.plotly_chart(fig, use_container_width=False, theme="streamlit")



