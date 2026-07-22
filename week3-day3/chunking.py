def simple_chunk(text:str, max_chars: int = 300) -> list[str]:
    """Memecah teks panjang jadi potongan kecil berdasarkan paragraf/kalimat."""

    text = text.strip().replace("\n"," ").replace(" "," ")

    if len(text) <= max_chars:
        return [text]
    
    # pecah berdasarkan kalimat (titik), gabung sampai mendekat max_chars
    sentences = text.split(". ")
    chunks = []
    current_chunk = ""

    for sentense in sentences:
        if len(current_chunk) + len(sentences) <= max_chars:
            current_chunk += sentense + ". "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentense + ". "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks