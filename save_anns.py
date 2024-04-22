import streamlit as st
from streamlit_tags import st_tags, st_tags_sidebar
from datasets import load_dataset 
import pandas as pd
from sklearn.model_selection import train_test_split
from sentence_transformers import SentenceTransformer
from annoy import AnnoyIndex


demo1 = load_dataset("csv", data_files="train_orig.csv", split='train')
df = demo1.to_pandas()
df_copy = df.copy()

model = SentenceTransformer('all-MiniLM-L6-v2')

# Define the tokenize_and_encode function
def tokenize_and_encode(text, model=model):
    embedding = model.encode([text])
    return embedding[0]

# Tokenize and encode the columns

df_copy['title'] = df_copy['title'].apply(tokenize_and_encode)
df_copy['ingredients'] = df_copy['ingredients'].apply(tokenize_and_encode)
df_copy['directions'] = df_copy['directions'].apply(tokenize_and_encode)

title_embeddings = df_copy['title']
ingredients_embeddings = df_copy['ingredients']
directions_embeddings = df_copy['directions']

# Assuming that 'embeddings' is a list of your document vectors
title_dim = len(title_embeddings[0])  # Length of item vector that will be indexed
title_t = AnnoyIndex(title_dim, 'angular')  # Length of item vector that will be indexed and 'angular' for cosine similarity

ingredients_dim = len(ingredients_embeddings[0])
ingredients_t = AnnoyIndex(ingredients_dim, 'angular')

directions_dim = len(directions_embeddings[0])
directions_t = AnnoyIndex(directions_dim, 'angular')


for i, vector in enumerate(title_embeddings):
    title_t.add_item(i, vector)

title_t.build(10)  # 10 trees
title_t.save('anns/title_test.ann')

for i, vector in enumerate(ingredients_embeddings):
    ingredients_t.add_item(i, vector)

ingredients_t.build(10)  # 10 trees
ingredients_t.save('anns/ingredients_test.ann')

for i, vector in enumerate(directions_embeddings):
    directions_t.add_item(i, vector)

directions_t.build(10)  # 10 trees
directions_t.save('anns/directions_test.ann') 

model.save('/Users/nithin/Desktop/Spring2/Recipe/st_model')