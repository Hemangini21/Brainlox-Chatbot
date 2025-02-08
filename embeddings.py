import os
import faiss
import pickle
from langchain_community.vectorstores import FAISS
from sentence_transformers import SentenceTransformer  # Use SentenceTransformer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MODEL_NAME = "all-MiniLM-L6-v2"  # A lightweight and efficient embedding model
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH")

def create_embeddings(documents):
    # Load SentenceTransformer model
    embeddings_model = SentenceTransformer(MODEL_NAME)

    # Convert documents to embeddings
    texts = [doc.page_content for doc in documents]
    embeddings = embeddings_model.encode(texts)

    # Create a FAISS vector database
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Save FAISS vector database
    faiss.write_index(index, VECTOR_DB_PATH)
    print("Vector database saved successfully.")

if __name__ == "__main__":
    from scraper import scrape_brainlox_courses
    docs = scrape_brainlox_courses()
    create_embeddings(docs)
