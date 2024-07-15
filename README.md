# StepsAi-assesment

## Overview

To develop a robust Question Answering (QA) system leveraging the capabilities of Large Language Models (LLMs) to provide comprehensive and accurate answers to user queries.

## Table of Contents

- [Installation](#installation)
- [Methods](#methods)
  - [Using Openai without using QueryExpander](#Using-Openai-without-using-BM25)
  - [Using-GenAi-and-Groq-integrating-BM25-for-QueryExpansion ](#Using-GenAi-and-Groq-integrating-BM25-for-QueryExpansion )
- [Advantages and Disadvantages](#Advantages-and-Disadvantages)
  - [Advantages](#Advantages)
  - [Disadvantages](#Disadvantages)
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
- Fetches content from these URLs and stores them in a txt file.
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

### Using-GenAi-and-Groq-integrating-BM25-for-QueryExpansion
#### 1. Data Scraping:
- Extracts URLs from the NVIDIA CUDA documentation using BeautifulSoup.
- Fetches content from these URLs and stores them in a JSON file.
#### 2. Data Preprocessing:
- Splits the extracted text into semantically meaningful chunks using Sentence Transformer embeddings and Langchain's SemanticChunker.
- Embeds each chunk using Google Generative AI Embeddings and sentence-transformers to understand embeddings more clearly.
- we embed chunks for efficient similarity search
#### 3. Vector Database:
- Stores the embedded chunks in a Milvus vector database for fast retrieval.
- Create a database name and create the tables to store, also initialize the size for table along with metrics for semantic search, finally start pushing the chunks to db.
#### 4. Question Expander:
- Create a LLM model either Google Generative AI or Groq/
- Set the system prompt, variables and pass your query to make it more meaningful and declare it as variable.
#### 5. Hybrid Retrieval:
- Combines BM25 and DPR retrieval methods for improved accuracy.
- Now Embed the Expanded query and search in the db.
- Create a functions to pass to our llm
#### 6. Question Answering:
- Uses Google Generative AI's Gemini model or Groq models to generate answers based on the retrieved context and the user's query.

### Advantages-and-Disadvantages
#### Advantages
- Improved accessibility: Provides easy and quick access to information from the complex NVIDIA CUDA documentation.
- Time-saving: Users can find answers to their queries without spending hours searching through the documentation.
- Enhanced user experience: Offers a user-friendly interface for interacting with the information.
- Potential for automation: Can be integrated into other tools or platforms to automate tasks related to CUDA.
- Knowledge base: Serves as a valuable resource for learning and understanding CUDA concepts.
#### Disadvantages
- Dependency on data quality: The accuracy of the QA system relies heavily on the quality of the scraped data.
- Limitations of language models: The quality of the generated answers is dependent on the capabilities of the LLM used.
- Computational resources: Requires significant computational resources for data processing, embedding, and model training.
- Maintenance: The system requires ongoing maintenance to ensure data accuracy and model performance.
- Potential for bias: The LLM used might introduce biases into the generated answers.
