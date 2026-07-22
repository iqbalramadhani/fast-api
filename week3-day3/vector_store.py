import os
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from dotenv import load_dotenv
from google import genai

load_dotenv()

gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class GeminiEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input:Documents) -> Embeddings:
        result = gemini_client.models.embed_content(
            model="gemini-embedding-001",
            contents=input
        )
        return [e.values for e in result.embeddings]


chroma_client = chromadb.PersistentClient(path="../chroma_data")
knowledge_collection = chroma_client.get_or_create_collection(
    name="knowledge_base",
    embedding_function=GeminiEmbeddingFunction()
)