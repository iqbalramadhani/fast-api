import chromadb

# Bikin cliemt ChromaDN yang jallan lokal, daata simpa ke folder
client = chromadb.PersistentClient(path="../chroma_data")

# Collection itu serta "tabel" di SQL
collection = client.get_or_create_collection(name="my_documents")

# Tambah data
# collection.add(
#     documents=[
#         "Minum susu hangat sebelum tidur bisa membantu relaksasi",
#         "Kopi sebaiknya dihindari menjelang malam hari",
    #         # "Resep membuat nasi goreng yang enak dan mudah",
#         # "Olahraga teratur meningkatkan kualitas istirahat malam",
#         # "Cara merawat tanaman hias di dalam ruangan"
#     ],
#     metadatas=[
#         {"kategori":"tidur", "sumber":"artikel_kesehatan_1"},
#         {"kategori":"kafein", "sumber":"artikel_kesehatan_2"}
#     ],
#     ids=["doc6","doc7"]
# )

# print("Data berhasil disimpan!")
# print("Jumlah dokumen:",collection.count())

# result = collection.query(
#     query_texts=["bagai mana cara istirahat yang baik"],
#     n_results=3,
#     where={"kategori":"tidur"}
# )

# print("Hasil pencarian:")
# for doc, distance in zip(result["documents"][0],result["distances"][0]):
#     print(f"[Jarak: {distance:.4f}] {doc}")
# for doc, meta in zip(result["documents"][0],result["metadatas"][0]):
#     print(f"{doc} | kategori: {meta['kategori']}")

# update data
# collection.update(
#     ids=["doc1"],
#     documents=["Susu hangat dan teh chamolie bagus diminum sebelum tidur"]
# )

# results = collection.query(
#     query_texts=["tips supaya bisa tidur nyenyak"],
#     n_results=3
# )

# print("Hasil pencarian:")
# for doc, distance in zip(results["documents"][0], results["distances"][0]):
#     print(f"[jarak: {distance:.4f}] {doc}")

# delete documen
# collection.delete(ids=["doc3"])
# print("Sisa dokumen:",collection.count())


# eksperimen
for k in [1, 3, 5]:
    result = collection.query(
        query_texts=["tips supaya bisa tidur nyenyak"],
        n_results=k
    )

    print(f"\nTop {k} hasil:")
    for doc in result["documents"][0]:
        print(f"- {doc}")