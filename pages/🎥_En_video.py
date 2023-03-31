import streamlit as st
import os 
import streamlit.components.v1 as components
import difflib
import pandas as pd


APP_TITLE = 'CGenial concours: en video'
APP_SUB_TITLE = 'Videos des expériences'


scientific_names_list = [
                        # 'Joliot',
#                                     'Adrien Sénéchal',
                                    'Galilée',
                                    'Newton',
                                    'Lavoisier', 
                                    'Arago', 
                                    'François Jacob',
                                    ]


def authors():

    st.sidebar.markdown('''

    Contributeurs :male-student: :female-student: :female-teacher:
    - Les élèves du collège Georges Braque
    - Encadrants: M. Devert, F. Mary 
    '''
    )


def fetch_csv_eleves_scientifiques():
      eleves_scientifiques_table = pd.read_csv('Cgenial_table_eleves_scientifiques.csv')
      return eleves_scientifiques_table

def display_scientific_filter():
      scientific_names_list.sort()
      scientific_names_list.insert(0,'Tous')
      st.sidebar.header('Selectionne un scientifique')
      scientific_selected = 'Tous'
      scientific_selected = st.selectbox('Nom du scientifique :female-scientist: :male-scientist:', scientific_names_list,
                                                                        )
      #st.write(scientific_selected)

      st.session_state['scientific_selected'] = scientific_selected 

      return scientific_selected


def paginator(label, items, items_per_page=10, on_sidebar=True):
    """Lets the user paginate a set of items.
    Parameters
    ----------
    label : str
        The label to display over the pagination widget.
    items : Iterator[Any]
        The items to display in the paginator.
    items_per_page: int
        The number of items to display per page.
    on_sidebar: bool
        Whether to display the paginator widget on the sidebar.
        
    Returns
    -------
    Iterator[Tuple[int, Any]]
        An iterator over *only the items on that page*, including
        the item's index.
    Example
    -------
    This shows how to display a few pages of fruit.
    >>> fruit_list = [
    ...     'Kiwifruit', 'Honeydew', 'Cherry', 'Honeyberry', 'Pear',
    ...     'Apple', 'Nectarine', 'Soursop', 'Pineapple', 'Satsuma',
    ...     'Fig', 'Huckleberry', 'Coconut', 'Plantain', 'Jujube',
    ...     'Guava', 'Clementine', 'Grape', 'Tayberry', 'Salak',
    ...     'Raspberry', 'Loquat', 'Nance', 'Peach', 'Akee'
    ... ]
    ...
    ... for i, fruit in paginator("Select a fruit page", fruit_list):
    ...     st.write('%s. **%s**' % (i, fruit))
    """

    # Figure out where to display the paginator
    if on_sidebar:
        location = st.sidebar.empty()
    else:
        location = st.empty()

    # Display a pagination selectbox in the specified location.
    items = list(items)
    n_pages = len(items)
    n_pages = (len(items) - 1) // items_per_page + 1
    page_format_func = lambda i: "Page %s" % i
    page_number = location.selectbox(label, range(n_pages), format_func=page_format_func)

    # Iterate over the items in the page to let the user display them.
    min_index = page_number * items_per_page
    max_index = min_index + items_per_page
    import itertools
    return itertools.islice(enumerate(items), min_index, max_index)


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

    display_scientific_filter()

    eleves_scientifiques_table = fetch_csv_eleves_scientifiques()


    st.sidebar.image("https://www.sciencesalecole.org/wp-content/uploads/2022/09/CGenial_Concours_1920x1080.png",
                         use_column_width=True)


    if 'scientific_selected' not in st.session_state:
        st.session_state['scientific_selected'] = 'Tous' #or whatever default


    scientific_selected = st.session_state['scientific_selected'] 

    if scientific_selected !='Tous':

        # https://discuss.streamlit.io/t/navigate-multipage-app-with-buttons-instead-of-sidebar/27986/7

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

        #with st.expander(f'{scientific_selected} biographie'):
        #    st.write('test')
        #    st.write(eleves_scientifiques_table.iloc[id_best_guess_scientific])


        DEFAULT_WIDTH = 40

        width = st.sidebar.slider(
         label="Dimension video", min_value=0, max_value=100, value=DEFAULT_WIDTH, format="%d%%"
          )

        width = max(width, 0.01)
        side = max((100 - width) / 2, 0.01)

        _, container, _ = st.columns([side, width, side])

        video = eleves_scientifiques_table['Fichier video'][id_best_guess_scientific]

        if video != None:
            videos = video.split('/')

        if len(videos)==1:
            container.video("./videos/" + eleves_scientifiques_table['Fichier video'][id_best_guess_scientific], 
            format='video/MOV', 
            start_time=0)
        else:
            for i in range(len(videos)):
                container.video("./videos/" + videos[i], 
                format='video/MOV', 
                start_time=0)




    authors()



if __name__ == "__main__":
    main()
