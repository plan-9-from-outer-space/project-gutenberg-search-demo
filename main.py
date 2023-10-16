import streamlit as st
import pandas as pd
import requests

@st.cache_data(show_spinner="Searching...")
def search_gutenberg(author, title):
    BASE_URL = "https://gutendex.com/books?search="
    author = author.replace(" ", "%20")
    title = title.replace(" ", "%20")
    params_url = f"{author}%20{title}"
    # params_url = params_url.replace(" ", "%20")
    search_url = f"{BASE_URL}{params_url}"
    try:
        res = requests.get(search_url)
        json_res = res.json()
        if json_res["count"] == 0:
            return False
        else:
            return json_res
    except:
        return False


@st.cache_data
def format_json_res(json_res):
    cols = ['Id', 'Author', 'Title', 'Language', 'Link']
    rows = []
    try:
        for i, result in enumerate(json_res["results"]):
            id = result["id"]
            # temp1 = result["authors"]
            author = [] if result["authors"] == [] else result["authors"][0]["name"]
            title = result["title"]
            # temp2 = result["languages"]
            language = [] if result["languages"] == [] else result["languages"][0]
            # link = f"https://www.gutenberg.org/ebooks/{id}"
            url = f"https://www.gutenberg.org/ebooks/{id}"
            link = f"[{url}]({url})"
            # print('link = ', link)
            rows.append([id, author, title, language, link])
        df = pd.DataFrame(rows, columns=cols)
        return df
    except Exception as e:
        print('\n', e, '\n')
        st.error("Error while parsing data")


if __name__ == "__main__":
    st.title("📚 Search Project Gutenberg")

    with st.form("search-form"):
        col1, col2 = st.columns(2)
        with col1:
            author = st.text_input("Author")
        with col2:
            title = st.text_input("Title")
        search = st.form_submit_button("Search", type='primary')

    if search:
        if author == '' and title == '':
            st.warning('Please enter an author and/or title')
            exit()
        json_res = search_gutenberg(author, title)
        if json_res:
            df = format_json_res(json_res)
            st.subheader(":robot_face: Search Results")
            st.table(df)
            # st.table(df.to_html(escape=False, unsafe_allow_html=True))
        else:
            st.error("No results found")
