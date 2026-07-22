
from chunking import simple_chunk

long_text = "Kalimat satu, Kalimat dua yang agak panjang. Kalimat tiga. " * 20
chunks = simple_chunk(long_text, max_chars=100)

for i, chunk in enumerate(chunks):
    print(f"Chunk {i} : {chunks}\n")