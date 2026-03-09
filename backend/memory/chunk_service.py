from backend.config import CHUNK_SIZE


def chunk_text(text, chunk_size=None):

    # chunk_size өгөгдөөгүй бол config.py-н утгыг ашиглана
    if chunk_size is None:
        chunk_size = CHUNK_SIZE

    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))

    return chunks