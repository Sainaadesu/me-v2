import requests
from backend.config import EMBED_MODEL

OLLAMA_EMBED_URL = "http://localhost:11434/api/embeddings"


def get_embedding(text: str):

    try:
        response = requests.post(
            OLLAMA_EMBED_URL,
            json={
                "model": EMBED_MODEL,
                "prompt": text
            }
        )
        response.raise_for_status()

        data = response.json()

        if "embedding" not in data:
            raise ValueError(f"Ollama буруу хариу өглөө: 'embedding' key олдсонгүй. Хариу: {data}")

        return data["embedding"]

    except requests.exceptions.ConnectionError:
        raise ConnectionError("Ollama сервертэй холбогдож чадсангүй. http://localhost:11434 ажиллаж байгаа эсэхийг шалгана уу.")

    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"Ollama embedding алдаа: {e}")