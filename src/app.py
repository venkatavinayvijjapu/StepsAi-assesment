from milvus import default_server
from pymilvus import connections
from pymilvus import FieldSchema, CollectionSchema, DataType, Collection
import json
import json
import torch
from transformers import DPRContextEncoder, DPRContextEncoderTokenizer, DPRQuestionEncoder, DPRQuestionEncoderTokenizer
from rank_bm25 import BM25Okapi
from pymilvus import utility


import streamlit as st
connections.connect(
   host='127.0.0.1',
   port=19530)
import os
from dotenv import load_dotenv
load_dotenv()

with open('encoding_chunks.json', 'r') as f:
    data = json.load(f)

# Extract passages and embeddings into separate lists
passages = [entry['content'] for entry in data]
embeddings = torch.tensor([entry['embedding'] for entry in data])


bm25 = BM25Okapi([passage.split() for passage in passages])

# Load DPR models and tokenizers
context_encoder = DPRContextEncoder.from_pretrained('facebook/dpr-ctx_encoder-single-nq-base')
context_tokenizer = DPRContextEncoderTokenizer.from_pretrained('facebook/dpr-ctx_encoder-single-nq-base')
question_encoder = DPRQuestionEncoder.from_pretrained('facebook/dpr-question_encoder-single-nq-base')
question_tokenizer = DPRQuestionEncoderTokenizer.from_pretrained('facebook/dpr-question_encoder-single-nq-base')

def encode_query(query):
    inputs = context_tokenizer(query, return_tensors='pt', padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        query_embedding = context_encoder(**inputs).pooler_output
    return query_embedding

def retrieve_passages_dpr(query_embedding, embeddings, passages, top_k=3):
    similarities = torch.matmul(query_embedding, embeddings.T).squeeze(0)
    top_k_indices = torch.topk(similarities, k=top_k).indices
    return [(passages[idx], similarities[idx].item()) for idx in top_k_indices]

def retrieve_passages_bm25(query, passages, top_k=3):
    bm25_scores = bm25.get_scores(query.split())
    top_k_indices = torch.topk(torch.tensor(bm25_scores), k=top_k).indices
    return [(passages[idx], bm25_scores[idx]) for idx in top_k_indices]

def hybrid_retriever(query, embeddings, passages, top_k=3, alpha=0.5):
    query_embedding = encode_query(query)
    
    assert query_embedding.shape[1] == embeddings.shape[1], f"Query embedding size {query_embedding.shape} does not match passage embedding size {embeddings.shape}"
    
    dpr_results = retrieve_passages_dpr(query_embedding, embeddings, passages, top_k)
    bm25_results = retrieve_passages_bm25(query, passages, top_k)

    # Combine DPR and BM25 results
    combined_scores = {}
    for passage, score in dpr_results:
        combined_scores[passage] = combined_scores.get(passage, 0) + alpha * score
    for passage, score in bm25_results:
        combined_scores[passage] = combined_scores.get(passage, 0) + (1 - alpha) * score

    sorted_passages = sorted(combined_scores.items(), key=lambda item: item[1], reverse=True)
    return sorted_passages[:top_k]


def preprocess():
    file_path = 'encoding_chunks.json'
    
    # Check if the file exists and is not empty
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        print("File does not exist or is empty")
        return
    
    # Attempt to load the JSON data
    try:
        with open(file_path, 'r') as f:
            chunks = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return
    
    # Define the schema for your collection
    fields = [
        FieldSchema(name="url", dtype=DataType.VARCHAR, max_length=500, is_primary=True),
        FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=65535),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=768)
    ]
    collection_schema = CollectionSchema(fields=fields, schema="DenseVector")
    collection_name_ivf = "stepAI_assignment"

    # Define IVF parameters
    nlist = 128
    metric = "L2" 

    # Create the collection
    collection = Collection(name=collection_name_ivf, schema=collection_schema, use_index="IVF_FLAT", params={"nlist": nlist, "metric": metric})

    # Prepare entities for insertion
    entity = []
    for chunk in chunks:
        dic = {
            'url': chunk['url'],
            'content': chunk['content'],
            'embedding': chunk['embedding']
        }
        entity.append(dic)

    # Insert entities into the collection
    collection.insert(entity)

def load_llm():
    import google.generativeai as genai
    genai.configure(api_key='AIzaSyDjLdpNwGuMxKlJECVD2p7MYGWZz7G1ukI')
    llm = genai.GenerativeModel('models/gemini-1.5-pro')
    return llm

def query_expander(query):
    llm=load_llm()
    prompt = f"""
    System: You are my helpful assistant, I want you to help me as a technical expert, Analyze the query and give me in detail with a case study, that might be found in webscraped data.
    
    User: {query}
    """

    return llm.generate_content(prompt).text


def generate_answer(query, modified_query):
    context = hybrid_retriever(modified_query, embeddings, passages)

    prompt = f"""
    You are my helpful assistant, Consider my query and context, using the context and your own knowledge, answer my query.

    Context:
    {context}

    Query:
    {query}
    """
    llm=load_llm()
    answer = llm.generate_content(prompt).text
    return answer


if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
if query:=st.chat_input("Enter your Query"):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.write(query)
if not utility.has_collection("stepAI_assignment"):
    preprocess()
modified_query=query_expander(query)
# with st.chat_message("user"):
#     st.write(query)

# top_passages=ranking(modified_query=modified_query)
# answer=generate_answer(query=query,top_passages=top_passages)
with st.expander("Expanded_query"):
    st.write(modified_query)
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_answer(query=query,modified_query=modified_query) 
            st.write(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)