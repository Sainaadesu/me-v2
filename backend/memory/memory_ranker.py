from datetime import datetime


def recency_score(date_string):

    memory_date = datetime.fromisoformat(date_string)

    days = (datetime.now() - memory_date).days

    return 1 / (days + 1)

def rank_memories(memories):

    ranked = []

    for m in memories:

        meta = m["metadata"]

        # metadata байхгүй бол default
        if meta is None:
            meta = {}

        importance = meta.get("importance", 0.5)

        # date байхгүй бол default date
        date = meta.get("date", "2000-01-01T00:00:00")

        recency = recency_score(date)

        score = importance * 0.5 + recency * 0.5

        ranked.append((score, m["text"]))

    ranked.sort(reverse=True)

    return [m[1] for m in ranked]