# StepsAi-assesment

## Overview

To develop a robust Question Answering (QA) system leveraging the capabilities of Large Language Models (LLMs) to provide comprehensive and accurate answers to user queries.

## Table of Contents

- [Installation](#installation)
- [Methods](#methods)
  - [Direct Pixel Extraction](#direct-pixel-extraction)
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
''' python:
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse

# Function to get page source after JavaScript execution
def get_page_source(driver, url):
    driver.get(url)
    time.sleep(3)  # Wait for the page to load completely
    return driver.page_source

# Function to extract internal links with specific class 'reference internal'
def extract_links(soup, base_url):
    links = set()
    base_domain = urlparse(base_url).netloc
    for a_tag in soup.find_all('a', class_='reference internal', href=True):
        href = a_tag['href']
        full_url = urljoin(base_url, href)
        if urlparse(full_url).netloc == base_domain:
            links.add(full_url)
    return links

def main():
    url = "https://docs.nvidia.com/cuda/"

    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)  # Ensure ChromeDriver is installed and in your PATH

    print(f"Extracting links from: {url}")
    page_source = get_page_source(driver, url)
    soup = BeautifulSoup(page_source, "html.parser")

    # Extract links with the specified class
    links = extract_links(soup, url)
    print(f"Found {len(links)} links with class 'reference internal'")

    # Convert the set to a list
    links_list = list(links)
    links_list[0]='https://docs.nvidia.com/cuda'
    # Print the list of links
    for link in links_list:
        print(link)

    # Close the browser
    driver.quit()
    links_list=list(set(links_list))

    return links_list

if __name__ == "__main__":
    links = main()
    '''
### Using Openai without using BM25
