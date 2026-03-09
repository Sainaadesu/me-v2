from backend.memory.memory_service import search_memory
from backend.memory.memory_ranker import rank_memories
from backend.config import TOP_K


def retrieve_memories(query):

    memories = search_memory(query)

    ranked = rank_memories(memories)

    formatted = ""

    # config.py-н TOP_K утгыг ашиглана
    for m in ranked[:TOP_K]:
        formatted += f"- {m}\n"

    return formatted