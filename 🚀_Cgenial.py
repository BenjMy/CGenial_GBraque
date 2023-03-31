import streamlit as st
import streamlit_folium
from streamlit_folium import st_folium
#https://folium.streamlit.app/dynamic_updates

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
import difflib

from streamlit_extras.switch_page_button import switch_page



APP_TITLE = 'CGenial concours: Les scientifiques de mon quartier'
APP_SUB_TITLE = 'Collège Georges Braque'
scientific_names_list = [
                        # 'Joliot',
#                                     'Adrien Sénéchal',
                                    'Galilée',
                                    'Joliot', 
                                    'Newton',
                                    'Lavoisier', 
                                     'Arago', 
                                     'Kepler', 
                                     'Herschel', 
                                     'Romer',
                                     'Charpak',
                                     'Eddington',
                                     'Edward Jenner',
                                     'Nicolas Copernic',
                                     'François Jacob',
                                    ]

GB_LATLONG = [49.22311782149911, 4.0165995097933]


def authors():

      st.sidebar.markdown('''

      Contributeurs :male-student: :female-student: :female-teacher:
      - Les élèves du collège Georges Braque
      - Encadrants: M. Devert, F. Mary 
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

      st.session_state['scientific_selected'] = scientific_selected 

      return scientific_selected

def fetch_wiki_scientist(scientific_selected_full):

      wikipage = wikipedia.page(scientific_selected_full)
      return wikipage

def convert_to_fullName():

      if scientific_selected =='Newton':
            scientific_selected_full = 'Isaac Newton'
      elif scientific_selected =='Lavoisier':
            scientific_selected_full = 'Antoine Laurent Lavoisier'
      elif scientific_selected =='Galilée':
            scientific_selected_full = 'Galileo'
      else:
            scientific_selected_full = scientific_selected

def display_pic(scientific_selected,eleves_scientifiques_table):


      masque_img = './img/Masques/' + eleves_scientifiques_table[eleves_scientifiques_table['Scientifique'].str.contains(scientific_selected)]['Fichier masque'].iloc[0]
      #st.write(masque_img)
      #st.write(scientific_selected)

      st.image(masque_img,caption=scientific_selected)



def display_shortbio(scientific_selected,eleves_scientifiques_table):

      short_bio = eleves_scientifiques_table[eleves_scientifiques_table['Scientifique'].str.contains(scientific_selected)]['Biographie'].iloc[0]

      if len(short_bio)<1:
        st.write('Courte biographie à écrire')
      else:
        st.write(short_bio)


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
            if len(streets['name_string'].str.contains(scientific_selected))>0:
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


def plot_folium(streets,street_with_scientific,tile_map_selected,eleves_scientifiques_table):
      ### Plot using folium explore (interactive)

      my_map = folium.Map(location=GB_LATLONG, zoom_start=15)

      #my_map = streets.explore()


      for s in street_with_scientific:
            s.explore(m=my_map, color='red',
                    tooltip=False,
                    #popup= "name_string"
                    )

      #st.write(test)
      #folium.TileLayer('Stamen Toner').add_to(my_map)
      #folium.TileLayer('Stamen Water Color').add_to(my_map)
      #folium.TileLayer('cartodbpositron').add_to(my_map)
      #folium.TileLayer('cartodbdark_matter').add_to(my_map)

      if tile_map_selected!='Open Street Map':
            background_tile_type(my_map,tile_map_selected)

      #folium.LayerControl().add_to(my_map)

      POI_pts = add_poi()
      for poi in POI_pts:
            folium.Marker(location=[poi[0],poi[1]],
                                    popup=poi[2],tooltip='Click ici').add_to(my_map)
    

      st_map = st_folium(my_map, width=1200, height=450)



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



def fetch_csv_eleves_scientifiques():
      eleves_scientifiques_table = pd.read_csv('Cgenial_table_eleves_scientifiques.csv')
      return eleves_scientifiques_table


def main():
      st.set_page_config(layout="wide", page_title=APP_TITLE)

      st.sidebar.image("https://www.sciencesalecole.org/wp-content/uploads/2022/09/CGenial_Concours_1920x1080.png",
                                     use_column_width=True)


      col1, col2, col3 = st.columns(3)

      with col1:
         st.write(' ')

      with col2:
         st.image('./img/Bannière mars.png',
      	width=500)
      with col3:
         st.write(' ')
         
      st.title(APP_TITLE)
      st.caption(APP_SUB_TITLE)








      st.info('''

                  
                  Selectionne le nom d'un scientifique dans la colonne de gauche et visualise où se trouve la rue dans ton quartier :world_map:.

                  La rue apparait en rouge! Se trouve t'elle proche de chez toi :question: Se trouve t'elle proche du collège :question:

                  '''
                  ,icon="ℹ️")


      tile_map_selected = display_tile_maps()

      nodes, streets = fetch_data()

      eleves_scientifiques_table = fetch_csv_eleves_scientifiques()
      

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



      if 'scientific_selected' not in st.session_state:
            st.session_state['scientific_selected'] = 'Tous' #or whatever default

      scientific_selected = display_scientific_filter(streets)

      # --------------------------------------------
      street_with_scientific = filter_streets_scientifics(streets,scientific_selected)
      
      # --------------------------------------------


      with st.expander(f'La carte de mon quartier',expanded=True):
            #plot_folium_mpl(streets,street_with_scientific)
            plot_folium(streets,street_with_scientific,tile_map_selected,eleves_scientifiques_table)



      if scientific_selected !='Tous':

            # https://discuss.streamlit.io/t/navigate-multipage-app-with-buttons-instead-of-sidebar/27986/7
            # switch_page("en video")


            st.info(f'''

                        Découvre quels travaux scientifiques a mené {scientific_selected} !
                        
                        Et reproduit son expérience en classe !
                        '''
                        ,icon="ℹ️")


            best_guess_scientific = difflib.get_close_matches(scientific_selected,
                  eleves_scientifiques_table['Scientifique'].to_list(),
                  cutoff=.35)

            id_best_guess_scientific = eleves_scientifiques_table['Scientifique'].to_list().index(best_guess_scientific[0])


            st.title('Groupe: {}'.format(eleves_scientifiques_table['Groupe'][id_best_guess_scientific]))

            #with st.expander('##' + scientific_selected + 'biographie'):
            with st.expander(f'{scientific_selected} biographie'):

                  #Display Biography
                  #st.subheader(f'{scientific_selected} Biographie')
                  col1, col2 = st.columns(2)

                  with col1:
                        display_pic(scientific_selected,eleves_scientifiques_table)
                  with col2:
                        display_shortbio(scientific_selected,eleves_scientifiques_table)

            with st.expander(f'{scientific_selected} Expérience'):

                  #Display Biography
                  tab1, tab2 = st.tabs(["📈 Le protocole expérimental", "🗃 Video"])
                  data = np.random.randn(10, 1)

                  tab1.subheader("Description du protocole expérimental")
                  if type(eleves_scientifiques_table['Expérience'][id_best_guess_scientific]) is str:
                        tab1.markdown(eleves_scientifiques_table['Protocole'][id_best_guess_scientific])
                  else:
                        tab1.write('En cours de rédaction')
                        tab1.line_chart(data)

                  tab2.subheader("Video de l'expérience")
                  #tab2.video("./videos/" + eleves_scientifiques_table['Fichier video'][id_best_guess_scientific], 
                  #    format='video/MOV', 
                  #    start_time=0)


                  DEFAULT_WIDTH = 20

                  width = st.sidebar.slider(
                  label="Width", min_value=0, max_value=100, value=DEFAULT_WIDTH, format="%d%%"
                  )

                  width = max(width, 0.01)
                  side = max((100 - width) / 2, 0.01)

                  _, container, _ = tab2.columns([side, width, side])
                  container.video("./videos/" + eleves_scientifiques_table['Fichier video'][id_best_guess_scientific], 
                  format='video/MOV', 
                  start_time=0)


                  #tab2.write(data)

      authors()

      st.sidebar.image("./img/LOGO-SCIENCES-A-LECOLE-Fond-trans-png.png",
                                     use_column_width=True)
    
      st.sidebar.image("./img/Académie_de_Reims.svg.png",
                        use_column_width=True)

if __name__ == "__main__":
      main()
