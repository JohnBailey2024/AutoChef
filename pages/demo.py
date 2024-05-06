import os
import json
import textwrap
from IPython.display import Markdown

import pandas as pd
import h5py
import google.generativeai as genai
import streamlit as st
from datasets import load_from_disk
from sentence_transformers import SentenceTransformer, util

# ---------------------------------
# from dotenv import load_dotenv

# load_dotenv()
# ---------------------------------

API_KEY = os.getenv("GOOGLE_API_KEY")


genai.configure(api_key=API_KEY)

gen_model = genai.GenerativeModel('gemini-pro')
embed_model = SentenceTransformer.load('embed_model/')

train = load_from_disk('full/')['train']

with open('config.json') as f:
    config = json.load(f)

with h5py.File('embeddings_100k.h5', 'r') as f:
    # Access the dataset in the HDF5 file
    embed_dataset = f['embeddings']
    embeds = embed_dataset[:]  
    
def get_similar_ids(target_query, vector_db = embeds, top_k = 10, model=embed_model):
    model.eval()
    target_vector =  model.encode(target_query)
    top_n_indices = util.semantic_search(target_vector, vector_db, top_k=top_k)[0]
    return {i['corpus_id']: i['score']  for i in top_n_indices}


def retrieve_docs_from_id(ids, doc_db=train):
    return {i: doc_db[i] for i in ids}

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def format_doc(doc):
    # Extracting title, ingredients, and directions from the recipe dictionary
    title = doc['title'].strip()
    ingredients = doc['ingredients']
    directions = doc['directions']

    # Capitalizing the first letter of each word in the title
    formatted_title = ' '.join(word.capitalize() for word in title.split())

    # Formatting ingredients
    formatted_ingredients = "\n".join(f"* {ingredient.strip()}" for ingredient in ingredients)

    # Formatting directions
    formatted_directions = "\n".join([f"Step {i+1}: \n {step.strip()}\n" for i, step in enumerate(directions)])

    # Combining all formatted components into the final recipe string
    formatted_recipe = f"""Recipe Title: {formatted_title}

INGREDIENTS

{formatted_ingredients}

COOKING INSTRUCTIONS:

{formatted_directions}"""

    return formatted_recipe


def main():
    st.sidebar.success('Test our demo here')
    st.markdown("<h1 style='text-align: center'>AutoChef</h1>", unsafe_allow_html=True)
    

    keywords = st.multiselect(
        '',
        config['first_500'] + config['next_500'],
        key='ing_input')
    
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

    if keywords:
        query = ','.join(keywords)

        prompt = f'''

        Take the {query} from the user and create cooking directions for a recipe where no ingredient apart from the ingredients in {query} and pantry staples are allowed.
        Output only the step by step directions. Do not include nay ingredient quantities or numbers in your instructions.
        '''

        response = gen_model.generate_content(prompt)

        llm_direction = response.parts[0].text

        rerank_query = query + llm_direction

        rag_ids = get_similar_ids(rerank_query)
        rag_docs = retrieve_docs_from_id(rag_ids)
        formatted_docs = [format_doc(doc) for doc in rag_docs.values()]
        doc_string = '\n ---------------- \n'.join(formatted_docs)


        fin_prompt = f'''
        recipe_documents: {doc_string}

        recipe_format: {config['recipe_format']}

        available_ingredients: {query}

        Imagine you are a creative and trustworthy recipe generator acting as an assistant. You offer help with generating new and delicious recipes.
        Your recipe should contain no ingredients apart from those provided in available_ingredients and any pantry staples.
        Base your generated recipe on the content of recipes provided as recipe_documents above. Make sure it follows the recipe_format provided above.

        Important Instruction Notice: If you cannot create a grounded recipe when limiting yourself to the available_ingredients, pantry staples and spices,
        then get more creative and allow some deviation from recpies from the documents
        '''

        response = gen_model.generate_content(fin_prompt)
        
        st.markdown(to_markdown(response.parts[0].text).data)
    else:
        st.write('Add an Ingredient')
    # Print the similar items

    



if __name__ == "__main__":
    main()

