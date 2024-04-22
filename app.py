import streamlit as st
from streamlit_tags import st_tags, st_tags_sidebar
from datasets import load_dataset 
import pandas as pd
from sklearn.model_selection import train_test_split
from sentence_transformers import SentenceTransformer
from annoy import AnnoyIndex

model = SentenceTransformer.load('st_model')

def tokenize_and_encode(text, model=model):
    embedding = model.encode([text])
    return embedding[0]


if __name__ == '__main__':

    df = pd.read_csv('train_orig.csv')
    dim = 384

    # Load the index
    title_u = AnnoyIndex(dim, 'angular')
    title_u.load('anns/title_test.ann')  # super fast, will just mmap the file

    # Load the index
    ingredients_u = AnnoyIndex(dim, 'angular')
    ingredients_u.load('anns/ingredients_test.ann')  # super fast, will just mmap the file

    # Load the index
    directions_u = AnnoyIndex(dim, 'angular')
    directions_u.load('anns/directions_test.ann')  # super fast, will just mmap the file


    st.markdown("<h1 style='text-align: center'>AutoChef</h1>", unsafe_allow_html=True)

    keywords = st_tags(
        label='',
        text='Press enter ingredients or add more',
        suggestions=['five', 'six', 'seven', 'eight', 'nine', 'three', 'eleven', 'ten', 'four'])

    query = ' '.join(keywords)
    st.write(query)

    query_embedding = tokenize_and_encode(query, model=model)

    n_similar = 5
    similar_items = ingredients_u.get_nns_by_vector(query_embedding, n_similar)

    st.markdown(
        """
        <style>
        .custom-spacing {
            margin-bottom: -10px; /* Adjust the negative value as needed */
        }
        </style>
        <style>
        .head-spacing{
            margin-top: 10px; /* Adjust the negative value as needed */
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    st.markdown("<h2 style='text-align: center' >Results</h2>", unsafe_allow_html=True)
    st.divider()
    # Print the similar items
    for item in similar_items:
        recipe = df.iloc[item]
        st.write(f"#### {recipe['title']}")
        
        st.write(f"##### Ingredients:")
        for i in eval(recipe['ingredients']):
            st.write(f'<div class="custom-spacing"><li>{i}</div>', unsafe_allow_html=True)
            #st.write(f'- {i}')
        
        st.write('<div class="head-spacing"><h5>Directions:</h5></div>', unsafe_allow_html=True)
        for i, step in enumerate(eval(recipe['directions'])):
            st.write(f'<pre><div class="custom-spacing"><b>{i+1}.</b> {step}', unsafe_allow_html=True)

        st.divider()
