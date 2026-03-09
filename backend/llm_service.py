import requests
import json
from backend.config import MODEL_NAME


OLLAMA_URL = "http://localhost:11434/api/generate"


def stream_chat(prompt, stop_event=None):

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": True
            },
            stream=True
        )
        response.raise_for_status()

        for line in response.iter_lines():
            if stop_event and stop_event.is_set():
                response.close()
                return
            if line:
                data = json.loads(line.decode("utf-8"))

                if "response" in data:
                    yield data["response"]

    except requests.exceptions.ConnectionError:
        raise ConnectionError("Ollama сервертэй холбогдож чадсангүй. http://localhost:11434 ажиллаж байгаа эсэхийг шалгана уу.")

    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"Ollama LLM алдаа: {e}")