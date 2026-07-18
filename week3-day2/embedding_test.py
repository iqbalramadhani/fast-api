import os
import numpy as np
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_embedding(text: str):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return np.array(result.embeddings[0].values)

def consine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# bandingkan beberapa kalimat
# kalimat1 = "Sayaaya suka minum kopi di pagi hari"
# kalimat2 = "Aku senang ngopi waktu pagi"
# kalimat3 = "Kucing saya suka tidur di sofa"

# emb1 = get_embedding(kalimat1)
# emb2 = get_embedding(kalimat2)
# emb3 = get_embedding(kalimat3)

# print(f"Kemiripan kalimat 1 & 2 : {consine_similarity(emb1,emb2):.4f}")
# print(f"Kemiripan kalimat 1 & 3 : {consine_similarity(emb1,emb3):.4f}")

# test experimen
query = "tips supaya bisa tidur nyenyak"

documents = [
    "Minum susu hangat sebelum tidur bisa membantu relaksasi",
    "Kopi sebaiknya dihindari menjelang malam hari",
    "Resep membuat nasi goreng yang enak dan mudah",
    "Olahraga teratur mengingkatkan kualitas istirahat malam",
    "Cara merawat tanaman hias di dalam ruangan"
]

query_emb = get_embedding(query)

results = []
for doc in documents:
    doc_emb = get_embedding(doc)
    similarity = consine_similarity(query_emb, doc_emb)
    results.append((doc, similarity))

# Ururtin dari yang palimg mirip
results.sort(key=lambda x: x[1], reverse=True)

print(f"Query: {query}\n")
for doc, score in results:
    print(f"[{score:.4f}] {doc}")
