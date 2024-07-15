from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse
import json
import re

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

def get_links(url):
    url = "https://docs.nvidia.com/cuda/"

    # Set up Selenium WebDriver with headless option
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

def get_page_source(driver, url):
    driver.get(url)
    time.sleep(3)  # Wait for the page to load completely
    return driver.page_source

# Function to scrape data from a single URL
def scrape_data(driver, url):
    print(f"Scraping data from: {url}")
    page_source = get_page_source(driver, url)
    soup = BeautifulSoup(page_source, "html.parser")
    text_content = soup.get_text(separator="\n").strip()
    # Remove excessive newlines
    text_content = re.sub(r'\n+', '\n', text_content)
    return text_content

def main():
    # Example list of URLs to scrape # Replace with your list of URLs
    url="https://docs.nvidia.com/cuda"
    links=get_links(url)
    # Set up Selenium WebDriver with headless option
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)  # Ensure ChromeDriver is installed and in your PATH

    # Initialize a list to store all the text content
    all_text_content = []

    # Iterate through each URL and scrape the data
    for url in links:
        text_content = scrape_data(driver, url)
        all_text_content.append({"url": url, "content": text_content})

    # Write the combined content to a JSON file
    with open("scraped_data1.json", 'w', encoding="utf-8") as file:
        json.dump(all_text_content, file, ensure_ascii=False, indent=4)

    # Close the browser
    driver.quit()

if __name__ == "__main__":
    main()
