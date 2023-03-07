import streamlit as st
import os 
import streamlit.components.v1 as components



APP_TITLE = 'CGenial concours: Notre travail'
APP_SUB_TITLE = 'Les élèves du Collège Georges Braque'
scientific_names_list = [
                        # 'Joliot',
# 						'Adrien Sénéchal',
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


def authors():

	st.sidebar.markdown('''

	Contributeurs :male-student: :female-student: :female-teacher:
	- Les élèves du collège Georges Braque
	- Encadrants: M. Devert, F. Mary 
	'''
	)



def main():
	st.set_page_config(layout="wide", page_title=APP_TITLE)

	st.title(APP_TITLE)
	st.caption(APP_SUB_TITLE)

	st.sidebar.image("https://www.sciencesalecole.org/wp-content/uploads/2022/09/CGenial_Concours_1920x1080.png",
						 use_column_width=True)


	imageCarouselComponent = components.declare_component("image-carousel-component", 
															path="frontend/public")

	from PIL import Image

	imageUrls = [
		"./img/recherche_map.jpeg",
		"./img/CGenial_Concours_1920x1080.png",
	]
	selectedImageUrl = imageCarouselComponent(imageUrls=imageUrls, height=200)
	

	if selectedImageUrl is not None:
		st.image(selectedImageUrl)


	
	authors()


if __name__ == "__main__":
	main()
