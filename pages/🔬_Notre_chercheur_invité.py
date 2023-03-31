import streamlit as st
import os 
import streamlit.components.v1 as components
import difflib



APP_TITLE = 'CGenial concours'
APP_SUB_TITLE = 'Notre chercheur invité'


def authors():

    st.sidebar.markdown('''

    Contributeurs :male-student: :female-student: :female-teacher:
    - Les élèves du collège Georges Braque
    - Encadrants: M. Devert, F. Mary 
    '''
    )


def main():
    st.set_page_config(layout="wide", page_title=APP_TITLE)

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

    st.sidebar.image("https://www.sciencesalecole.org/wp-content/uploads/2022/09/CGenial_Concours_1920x1080.png",
                         use_column_width=True)


    imageUrls = [
        "./img/BMary_presentation2.jpeg",
        "./img/BMary_presentation1.jpeg",
    ]
    st.image(imageUrls, use_column_width=False, 
                            width=500,
        caption=["La présentation de B. Mary notre chercheur invité"] * len(imageUrls))



    authors()


if __name__ == "__main__":
    main()
