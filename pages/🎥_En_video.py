import streamlit as st
import os 
import streamlit.components.v1 as components
import difflib



APP_TITLE = 'CGenial concours: en video'
APP_SUB_TITLE = 'Videos des expériences'


def authors():

    st.sidebar.markdown('''

    Contributeurs :male-student: :female-student: :female-teacher:
    - Les élèves du collège Georges Braque
    - Encadrants: M. Devert, F. Mary 
    '''
    )

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

    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)

    st.sidebar.image("https://www.sciencesalecole.org/wp-content/uploads/2022/09/CGenial_Concours_1920x1080.png",
                         use_column_width=True)


    if 'scientific_selected' not in st.session_state:
        st.session_state['scientific_selected'] = 'Tous' #or whatever default


    scientific_selected = st.session_state['scientific_selected'] 
    st.write(scientific_selected)

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
            if type(eleves_scientifiques_table['Expérience'][id_best_guess_scientific]) is str:
                st.write(eleves_scientifiques_table['Expérience'][id_best_guess_scientific])
            else:
                st.write('En cours de rédaction')
                tab1.line_chart(data)

            tab2.subheader("Video de l'expérience")
            tab2.write(data)


    authors()


if __name__ == "__main__":
    main()
