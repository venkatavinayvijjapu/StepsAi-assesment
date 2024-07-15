# StepsAi-assesment

## Overview

To develop a robust Question Answering (QA) system leveraging the capabilities of Large Language Models (LLMs) to provide comprehensive and accurate answers to user queries.

## Table of Contents

- [Installation](#installation)
- [Methods](#methods)
  - [Using Openai without using BM25](#Using-Openai-without-using-BM25)
  - [Pre-trained Segmentation Model](#pre-trained-segmentation-model)
- [Advantages and Disadvantages](#advantages-and-disadvantages)
  - [Direct Pixel Extraction](#advantages-and-disadvantages-of-direct-pixel-extraction)
  - [Pre-trained Segmentation Model](#advantages-and-disadvantages-of-pre-trained-segmentation-model)
- [Visualization](#visualization)
- [Contributing](#contributing)
- [License](#license)

## Installation
- python 3x
- langchain_openai
- langchain_google_genai
- selenium
- Beautifulsoup
- sentence-transformers
- langchain_experimental
- pymilvus
- milvus
- transformers
- langchain_openai
- langchain_core
- langchain_community

## Methods

### Using-Openai-without-using-BM25 
#### 1. Data Scraping:
- Extracts URLs from the NVIDIA CUDA documentation using BeautifulSoup.
- Fetches content from these URLs and stores them in a JSON file.
#### 2. Data Preprocessing:
- Loads the scraped data.
- Splits the text into chunks using semantic chunking.
- Embeds each chunk using a sentence transformer model.
- Stores the chunks and their embeddings in another JSON file.
#### 3. Milvus Integration:
- Initializes a Milvus connection.
- Creates a Milvus collection to store the embedded data.
- Inserts the embedded chunks into the Milvus collection.
- LLM and Vector Database Integration:
#### 4. Initializes an OpenAI LLM.
- Creates a vector database using Milvus and the embedded data.
- Constructs a conversational retrieval chain using the LLM and vector database.
#### 5. Question Answering:
- Demonstrates the QA system by providing a sample query ("Summarize the data").
- Retrieves relevant information from the vector database using the query.
- Generates a response using the LLM based on the retrieved information.
