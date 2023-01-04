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


APP_TITLE = 'CGenial concours: Les scientifiques de mon quartier'
APP_SUB_TITLE = 'College Georges Braque'
scientific_names_list = [
                        # 'Joliot',
# 						'Adrien Sénéchal',
						'Galilée', 
						'Lavoisier', 
						'Newton',
# 						'Arago', 
# 						'Kepler', 
# 						'Herschel', 
# 						'Romer',
# 						'Charpak',
# 						'Eddington',
						]

GB_LATLONG = [49.22311782149911, 4.0165995097933]


def authors():

	st.sidebar.markdown('''

	Contributeurs :male-student: :female-student: :female-teacher:
	- Les élèves du college George Braque
	- Encadrants: Marie Devert, Florian Mary 
	'''
	)


def display_scientific_filter(streets):
	scientific_names_list.sort()
	scientific_names_list.insert(0,'Tous')
	st.sidebar.header('Selectionne un scientifique')
	scientific_selected = 'Tous'
	scientific_selected = st.sidebar.selectbox('Nom du scientifique :female-scientist: :male-scientist:', scientific_names_list,
												)
	#st.write(scientific_selected)

	return scientific_selected

def display_pic(scientific_selected):

	if scientific_selected =='Newton':
		scientific_selected_full = 'Isaac Newton'
	elif scientific_selected =='Lavoisier':
		scientific_selected_full = 'Antoine Laurent Lavoisier'
	elif scientific_selected =='Galilée':
		scientific_selected_full = 'Galileo'

	wikipage = wikipedia.page(scientific_selected_full)

	try:
		st.image(wikipage.images[0], 
			caption=scientific_selected + 'Source: wikipedia')
	except:
		pass

def display_shortbio(scientific_selected):
	st.write('short bio here')


def fetch_data():
	### Fetch data


	# Fetch all Reims streets
	# ---------------------
	#df_reims = ox.geocode_to_gdf('reims')
	#reims = 'Reims, France'
	#graph = ox.graph_from_place(reims, network_type='drive')
	#nodes, streets = ox.graph_to_gdfs(graph)

	# Fetch only the neighbour
	# ---------------------
	G2 = ox.graph_from_point(GB_LATLONG, dist=1250, dist_type='bbox', network_type='drive')
	nodesGB2_quartier, GB2_quartier = ox.graph_to_gdfs(G2)


	return nodesGB2_quartier, GB2_quartier

#@st.cache(suppress_st_warning=True)
def filter_streets_scientifics(streets,scientific_selected):
	### Search for streets with scientific names

	scientifics = []
	if scientific_selected=='Tous':
		scientific_selected = scientific_names_list
		for s in scientific_names_list:
			if sum(streets['name_string'].str.contains(s))>1:
				scientifics.append(streets[streets['name_string'].str.contains(s)])
	else:
		if sum(streets['name_string'].str.contains(scientific_selected))>1:
			scientifics.append(streets[streets['name_string'].str.contains(scientific_selected)])


	#ox.plot_graph(G)
	return scientifics

def add_poi():

	### Add points of interest
	#G = ox.graph_from_address('3 rue Adrien Sénéchal, 51100, REIMS')
	#nodesGB_quartier, GB_quartier = ox.graph_to_gdfs(G)

	GB_latlong = [49.22311782149911, 4.0165995097933, 'College']

	POI_pts = [GB_latlong]
	return POI_pts


def display_tile_maps():
	tile_map_selected = []
	tile_map_list = ['Open Street Map','Esri','Stamen Toner']
	tile_map_selected = st.sidebar.selectbox('Change type de carte', tile_map_list,
											index=0)
	return tile_map_selected


def background_tile_type(my_map,tile_map_selected):

	if tile_map_selected == 'Esri':
		folium.TileLayer(tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
			attr='Esri',
			name='Esri Satellite',
			overlay=True,
			control=False,
			).add_to(my_map)
	elif tile_map_selected == 'Stamen Toner':
		folium.TileLayer('Stamen Toner').add_to(my_map)
	else:
		pass


def plot_folium(streets,street_with_scientific,tile_map_selected):
	### Plot using folium explore (interactive)

	my_map = folium.Map(location=GB_LATLONG, zoom_start=18)

	my_map = streets.explore()

	for s in street_with_scientific:
		s.explore(m=my_map, color='red')

	#folium.TileLayer('Stamen Toner').add_to(my_map)
	#folium.TileLayer('Stamen Water Color').add_to(my_map)
	#folium.TileLayer('cartodbpositron').add_to(my_map)
	#folium.TileLayer('cartodbdark_matter').add_to(my_map)

	if tile_map_selected!='Open Street Map':
		background_tile_type(my_map,tile_map_selected)

	#folium.LayerControl().add_to(my_map)

	#st_folium(my_map)
	POI_pts = add_poi()
	for poi in POI_pts:
		folium.Marker(location=[poi[0],poi[1]],
						popup=poi[2],tooltip='Click ici').add_to(my_map)
    
	st_map = st_folium(my_map, width=700, height=450)


def plot_POI(ax):

	POI_pts = add_poi()
	for poi in POI_pts:
		ax.scatter(poi[1],poi[0],label=poi[2])



def plot_folium_mpl(streets,street_with_scientific):

	fig, ax = plt.subplots(figsize=(24, 18))
	streets.plot(ax=ax, legend=True)

	for s in street_with_scientific:
			s.plot(ax=ax, color='red')


	plot_POI(ax)

	plt.title("Reims")
	plt.legend()

	st.pyplot(fig)






def main():
	st.set_page_config(APP_TITLE)
	st.title(APP_TITLE)
	st.caption(APP_SUB_TITLE)

	st.sidebar.image("https://www.sciencesalecole.org/wp-content/uploads/2022/09/CGenial_Concours_1920x1080.png",
						 use_column_width=True)

	st.info('''

			
			Selectionne le nom d'un scientifique dans la colonne de gauche et visualise où se trouve la rue dans ton quartier :world_map:. 
			
			La rue apparait en rouge! 

			- Se trouve t'elle proche de chez toi :question:
			- Se trouve t'elle proche du collège :question:

			'''
			,icon="ℹ️")


	tile_map_selected = display_tile_maps()

	nodes, streets = fetch_data()
	

	# reshape name of the streets typ
	# --------------------------------------------
	streets = streets[streets['name'].notna()]
	newstreetname = []
	for l in streets['name']:
		if  type(l)==list:
			newstreetname.append(','.join(map(str, l)))
		else:
			newstreetname.append(l)
	streets['name_string'] = newstreetname


	scientific_selected = display_scientific_filter(streets)

	# --------------------------------------------
	street_with_scientific = filter_streets_scientifics(streets,scientific_selected)
	
	# --------------------------------------------


	with st.expander(f'La carte de mon quartier',expanded=True):
		#plot_folium_mpl(streets,street_with_scientific)
		plot_folium(streets,street_with_scientific,tile_map_selected)



	if scientific_selected !='Tous':

		st.info(f'''

				Découvre quels travaux scientifiques à mener {scientific_selected} !
				
				Et reproduit son expérience en classe !
				'''
				,icon="ℹ️")


		#with st.expander('##' + scientific_selected + 'biographie'):
		with st.expander(f'{scientific_selected} biographie'):

			#Display Biography
			#st.subheader(f'{scientific_selected} Biographie')
			col1, col2 = st.columns(2)

			with col1:
				display_pic(scientific_selected)
			with col2:
				display_shortbio(scientific_selected)

		with st.expander(f'{scientific_selected} Expérience'):

			#Display Biography
			tab1, tab2 = st.tabs(["📈 Le protocole expérimental", "🗃 Video"])
			data = np.random.randn(10, 1)

			tab1.subheader("Description du protocole expérimental")
			tab1.line_chart(data)

			tab2.subheader("Video de l'expérience")
			tab2.write(data)

	authors()


if __name__ == "__main__":
	main()
