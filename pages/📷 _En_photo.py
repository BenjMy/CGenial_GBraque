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

	imageUrls = [
		"./img/recherche_map.jpeg",
		"./img/CGenial_Concours_1920x1080.png",
	]

	#st.image(imageUrls, use_column_width=True, caption=["Le travail des élèves du collège"] * len(imageUrls))
	
	image_iterator = paginator("Select a page", imageUrls)
	indices_on_page, images_on_page = map(list, zip(*image_iterator))
	st.image(images_on_page, width=400, caption=indices_on_page)


	authors()


if __name__ == "__main__":
	main()
