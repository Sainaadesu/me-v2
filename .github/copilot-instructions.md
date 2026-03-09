# Copilot Instructions — Second-Me v2

## Language

All CLI output text, comments, user-facing strings, and error messages in this project must be written in **Mongolian**. Do not write any user-visible text in English.

## Architecture Overview

Local personal AI system built on a RAG pipeline:

```
User input → Embedding → ChromaDB search → Memory ranking → Persona reasoning (5 agents) → Ollama LLM → CLI output
```

- **LLM**: Ollama with `llama3:latest` (quantized, CPU-friendly)
- **Embeddings**: `nomic-embed-text` via Ollama
- **Vector DB**: ChromaDB stored at `data/chroma_db/`
- **Personas**: Strategist, Philosopher, Discipline, Observer, Emotional (configs in `backend/persona/configs/`)
- **Config**: All tuneable constants (`TOP_K`, `CHUNK_SIZE`, `CONTEXT_SIZE`, `THREADS`) are in `backend/config.py`

## Running the Project

**Always run from the project root** (`C:\Users\sotgo\Second-me-v2`). Relative paths like `data/chroma_db` and `backend/persona/configs` only resolve correctly from there.

```powershell
# Correct
cd C:\Users\sotgo\Second-me-v2
python -m cli.main

# Or use the global command (via me-v2.bat + pip install -e .)
me-v2
```

Do **not** run as `python cli/main.py` — it breaks relative imports.

## Prerequisites (must be running before starting)

```powershell
ollama serve              # Ollama server
ollama pull llama3:latest
ollama pull nomic-embed-text
```

When diagnosing errors, always check that Ollama is running and both models are available.

## Install

```powershell
pip install -e .
```

Dependencies: `chromadb`, `requests`, `rich`, `InquirerPy`.

## Key Paths

| Path | Purpose |
|------|---------|
| `backend/config.py` | Central config (TOP_K, CHUNK_SIZE, CONTEXT_SIZE, THREADS, model names) |
| `data/chroma_db/` | Vector database (auto-created) |
| `data/raw_journals/` | Drop `.txt` files here for batch ingestion |
| `data/processed_journals/` | Processed files moved here (auto-created) |
| `backend/persona/configs/` | JSON persona definitions |
| `cli/main.py` | Entry point (`main()` function) |
