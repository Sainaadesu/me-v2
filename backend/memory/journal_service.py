from datetime import datetime

from backend.memory.chunk_service import chunk_text
from backend.memory.memory_service import add_memory
from backend.memory.file_loader import load_txt_file


def add_journal_entry(text):

    chunks = chunk_text(text)

    for chunk in chunks:

        metadata = {
            "source": "journal",
            "date": datetime.now().isoformat(),
            "importance": 0.5
        }

        add_memory(chunk, metadata)


def import_journal_file(path):

    text = load_txt_file(path)

    add_journal_entry(text)