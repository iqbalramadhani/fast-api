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
    

client = chromadb.PersistentClient(path="../chroma_data")
collection = client.get_or_create_collection(
    name="my_documents",
    embedding_function=GeminiEmbeddingFunction()
)

collection.add(
    documents=[
        "Minum susu hangat sebelum tidur bisa membantu relaksasi",
        "Kopi sebaiknya dihindari menjelang malam hari"
    ],
    ids=["doc1","doc2"]
)

print("Berhasil, tanpa perlu dowload model apapun!")