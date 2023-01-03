import streamlit as st
import streamlit_folium
from streamlit_folium import st_folium

import os 
import folium
from folium import plugins
import osmnx as ox

import pandas as pd
import geopandas
import matplotlib.pyplot as plt

import wikipedia
import time
import numpy as np

from streamlit_extras.no_default_selectbox import selectbox


APP_TITLE = 'CGenial concours: Les scientifiques de mon quartier'
APP_SUB_TITLE = 'College Georges Braque'
scientific_names_list = ['Taittinger','Name2','Name3']

def authors():

	st.sidebar.markdown('''
	Credit: 
	- Les élèves du college George Braque
	- Encadrants: Marie Devert, Benjamin Mary 
	'''
	)


def display_scientific_filter():
    scientific_names_list.sort()

    st.sidebar.header('Select a scientific')
    scientific_selected = st.sidebar.selectbox('Scientific names', scientific_names_list)

    st.write(scientific_selected)

    return scientific_selected

def display_pic(scientific_selected):
    wikipage = wikipedia.page(scientific_selected)
    st.image(wikipage.images[0], 
    	caption=scientific_selected + 'Source: wikipedia')


def display_shortbio(scientific_selected):
	st.write('short bio here')


def fetch_data():
	### Fetch data

	df_reims = ox.geocode_to_gdf('reims')
	reims = 'Reims, France'
	graph = ox.graph_from_place(reims, network_type='drive')
	nodes, streets = ox.graph_to_gdfs(graph)

	return nodes, streets

@st.cache(suppress_st_warning=True)
def filter_streets_scientifics(streets):
	### Search for streets with scientific names

	#scientifics = streets[streets['name']=='Voie Jean Taittinger']
	for s in scientific_names_list:
		#scientifics_id = streets[streets['name'].isin(scientific_names_list)]
		scientifics.append(streets[s.isin(streets['name'])])
	st.write(scientifics)
	#ox.plot_graph(G)
	return scientifics

def add_poi():

	### Add points of interest
	G = ox.graph_from_address('3 rue Adrien Sénéchal, 51100, REIMS')
	nodesGB_quartier, GB_quartier = ox.graph_to_gdfs(G)

def plot_folium(streets,scientifics):
	### Plot using folium explore (interactive)

	map = streets.plot()
	scientifics.explore(m=map, color='red',
	             tooltip="name", # show "name" column in the tooltip)
	            )

	st_map = st_folium(map, width=700, height=450)


def plot_folium_mpl(streets,scientifics,scientific_selected):

	fig, ax = plt.subplots(figsize=(24, 18))
	streets.plot(ax=ax, legend=True)

	if scientific_selected is None:
		scientifics.plot(ax=ax, color='red')
	else:
		scientific_selected.plot(ax=ax, color='red')

	plt.title("Reims")

	st.pyplot(fig)




def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)

    st.info('''
            Selectionne le nom d'un scientifique dans la collonne de gauche et visualise ou se trouve la rue dans ton quartier. 
            La rue apparait en rouge
            '''
            ,icon="ℹ️")


    scientific_selected = display_scientific_filter()

    nodes, streets = fetch_data()
    scientifics = filter_streets_scientifics(streets)
    plot_folium_mpl(streets,scientifics,scientific_selected)


    with st.expander(f'{scientific_selected} Biographie'):

        #Display Biography
        st.subheader(f'{scientific_selected} Biographie')
        col1, col2 = st.columns(2)

        with col1:
            display_pic(scientific_selected)
        with col2:
            display_shortbio(scientific_selected)

    with st.expander(f'{scientific_selected} Experience'):

        #Display Biography
        tab1, tab2 = st.tabs(["📈 Protocole", "🗃 Video"])
        data = np.random.randn(10, 1)

        tab1.subheader("A tab with a chart")
        tab1.line_chart(data)

        tab2.subheader("A tab with the data")
        tab2.write(data)

    authors()


if __name__ == "__main__":
    main()
