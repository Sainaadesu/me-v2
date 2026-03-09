import hashlib
import chromadb
from backend.config import VECTOR_DB_PATH, COLLECTION_NAME
from backend.embedding.embedding_service import get_embedding


client = chromadb.PersistentClient(path=VECTOR_DB_PATH)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)


def add_memory(text, metadata=None):
    if metadata is None:
        metadata = {
            "source": "unknown",
            "importance": 0.5
        }

    embedding = get_embedding(text)

    # hash() нь программ ажиллах бүр өөр утга өгдөг тул md5 ашиглана
    stable_id = hashlib.md5(text.encode("utf-8")).hexdigest()

    # upsert: ижил ID байвал шинэчилнэ, байхгүй бол нэмнэ
    collection.upsert(
        documents=[text],
        embeddings=[embedding],
        metadatas=[metadata],
        ids=[stable_id]
    )

def search_memory(query, top_k=5):

    # Collection хоосон байвал хоосон жагсаалт буцаана
    if collection.count() == 0:
        return []

    query_embedding = get_embedding(query)

    # Байгаа document-ийн тооноос хэтрэхгүй байлгана
    actual_top_k = min(top_k, collection.count())

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=actual_top_k
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    memories = []

    for doc, meta in zip(documents, metadatas):

        memories.append({
            "text": doc,
            "metadata": meta
        })

    return memories

