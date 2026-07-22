from vector_store import knowledge_collection
from chunking import simple_chunk
from sample_docs import SAMPLE_DOCUMENT


chroma_client_ids = knowledge_collection.get()["ids"]
if chroma_client_ids:
    knowledge_collection.delete(ids=chroma_client_ids)


all_chunks = []
all_ids = []

for doc_idx, doc in enumerate(SAMPLE_DOCUMENT):
    chunks = simple_chunk(doc, max_chars=300)
    for chunk_ids, chunk in enumerate(chunks):
        all_chunks.append(chunk)
        all_ids.append(f"doc{doc_idx}_chunk{chunk_ids}")


knowledge_collection.add(
    documents=all_chunks,
    ids=all_ids
)

print(f"Berhasil penyimpan {len(all_chunks)} chunks ke knowledge base")