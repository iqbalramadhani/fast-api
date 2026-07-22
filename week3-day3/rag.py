from vector_store import knowledge_collection
from ai_client import ask_gemini

def rag_answer(question: str, top_k: int = 3) -> str:
    # 1. RETRIEVAL - cari chunk yang paling relevan
    results = knowledge_collection.query(
        query_texts=[question],
        n_results=top_k
    )

    relevant_chunks = results["documents"][0]

    # 2. AUGMENT
    context = "\n\n".join(relevant_chunks)

    # 3. GENERATION
    prompt = f"""Jawab pertanyaan berikut HANYA berdasarkan konteks yang diberikan.
    kalau jawabannya tidak ada di konteks, katakan "Maaf, saya tidak menemukan informasi itu."
    
    Konteks:
    {context}
    
    Pertanyaan: {question}"""

    answer = ask_gemini(prompt, temperature=0.2)

    return answer