import os
from langchain_community.document_loaders import WebBaseLoader
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def scrape_brainlox_courses():
    url = "https://brainlox.com/courses/category/technical"
    loader = WebBaseLoader(url)
    documents = loader.load()
    return documents

if __name__ == "__main__":
    data = scrape_brainlox_courses()
    print(f"Extracted {len(data)} documents")
