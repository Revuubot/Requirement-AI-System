def chunk_text(text: str, max_chars: int = 4000):
    """
    Splits text into overlapping chunks to avoid context loss.
    """

    chunks = []
    start = 0
    overlap = 400

    while start < len(text):
        end = start + max_chars
        chunk = text[start:end]

        chunks.append(chunk)
        start = end - overlap

    return chunks
