# -*- coding: utf-8 -*
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer, util
import torch
import pandas as pd
import random

defn_df = pd.read_csv("Data/Unsupervised Topic Modeling - Topic definitions.csv")

extracts_df = pd.read_csv("Data/Unsupervised Topic Modeling - Extracts.csv")
extracts_list = extracts_df['Extracts']

defn_list = []
for i in range(len(defn_df)):
    defn_list.append(defn_df['Definition'][i])
topic_list = defn_df['Topics']


#Load AutoModel from model repository
#THIS DOWNLOADS IMPORTANT!!!!!!!!!!
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/stsb-roberta-large")

model = AutoModel.from_pretrained("sentence-transformers/stsb-roberta-large")

#Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    return sum_embeddings/sum_mask

#Defintions Embeddings
def defn_encode():
    #Tokenize sentences
    encoded_defn = tokenizer(defn_list, padding=True, truncation=True, max_length=128, return_tensors='pt')
    #Compute token embeddings
    with torch.no_grad():
        model_output = model(**encoded_defn)

    #Perform pooling. In this case, mean pooling
    defn_embeddings = mean_pooling(model_output, encoded_defn['attention_mask'])
    return defn_embeddings

#Sentence Embeddings
def extract_encode(extract):
    #Tokenize sentences
    encoded_topics = tokenizer(extract, padding=True, truncation=True, max_length=128, return_tensors='pt')
    #Compute token embeddings
    with torch.no_grad():
        model_output = model(**encoded_topics)

    #Perform pooling. In this case, mean pooling
    extract_embeddings = mean_pooling(model_output, encoded_topics['attention_mask'])
    return extract_embeddings

defn_embeddings = defn_encode()

def process():
    pairs = []
    extract_embeddings = extract_encode(extracts_list[random.randint(0,44)])
    cosine_scores = util.pytorch_cos_sim(defn_embeddings, extract_embeddings)        

    #Find the pairs with the highest cosine similarity scores
    for k in range(len(cosine_scores)-1):
        pairs.append({'index': [k], 'score': cosine_scores[k]})
    #Sort scores in decreasing order
    pairs = sorted(pairs, key=lambda x: x['score'], reverse=True)

    topics = []
    for pair in pairs[0:30]:
        i = pair['index'][0]
        topics.append(topic_list[i])
    
    res = []
    [res.append(x) for x in topics if x not in res]
    return res





