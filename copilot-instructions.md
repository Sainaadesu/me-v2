 <!--                    venv\Scripts\activate                            -->
 <!--                    python -m cli.main                    -->
 <!--                    pip uninstall me-v2                    -->
 <!--                    pip install -e .                   -->

Сайнаа, ойлголоо. Доорх нь **өөр AI систем шууд ойлгож чадахуйц, бүтцэт, техникийн тайлан**.
Чи үүнийг **бүхлээр нь copy хийгээд** өөр AI-д өгч болно.

---

# PERSONAL AI SYSTEM — TECHNICAL PROJECT REPORT

## 1. Project Overview

This project builds a **local personal AI system** designed as a **Second-Me architecture**.
The goal is to create a lightweight, controllable **personal cognitive system** that can:

- remember user information
- retrieve relevant memories
- reason using multiple personas
- run locally on CPU hardware
- operate through a CLI interface

The system uses **Retrieval-Augmented Generation (RAG)** instead of model fine-tuning.

---

# 2. System Goals

Primary objectives:

1. Build a **local AI assistant**
2. Implement **long-term memory**
3. Support **multiple reasoning perspectives**
4. Keep system **lightweight (CPU friendly)**
5. Avoid complex pipelines
6. Maintain **simple debuggable architecture**

---

# 3. Core Architecture

The system pipeline:

```
User input
↓
Memory retrieval (RAG)
↓
Memory ranking
↓
Persona reasoning
↓
LLM generation
↓
CLI output
```

Detailed flow:

```
User question
↓
Embedding generation
↓
Vector search (Chroma)
↓
Top-K memory retrieval
↓
Memory re-ranking
↓
Persona reasoning (5 agents)
↓
LLM response
↓
CLI output
```

---

# 4. Model Configuration

LLM runtime:

```
Ollama
Model: llama3:8b
Quantization: q4
Context length: 2048
```

Reason for this choice:

- CPU friendly
- small memory footprint
- acceptable reasoning capability

---

# 5. Embedding System

Embedding model:

```
nomic-embed-text
```

Embedding workflow:

```
text
↓
embedding generation
↓
vector storage
↓
semantic similarity search
```

---

# 6. Memory System

Vector database:

```
ChromaDB
```

Collection:

```
sainaa_memory
```

Stored data:

```
document text
embedding vector
metadata
```

Metadata structure:

```
{
  source: "journal",
  date: "ISO timestamp",
  importance: float
}
```

---

# 7. Memory Retrieval (RAG)

Search process:

```
User query
↓
query embedding
↓
Chroma similarity search
↓
Top 5 candidate memories
```

Configuration:

```
top_k = 5
chunk_size = 400
```

---

# 8. Memory Ranking System

After retrieval the system performs **memory re-ranking**.

Score calculation:

```
score =
  0.5 * importance
+ 0.5 * recency
```

Recency function:

```
recency = 1 / (days_since_memory + 1)
```

Purpose:

- prioritize recent memories
- prioritize important memories

---

# 9. Memory Ingestion System

The system supports **two ingestion methods**.

### Manual journal input

```
CLI
↓
User writes journal entry
↓
Text chunking
↓
Embedding
↓
Stored in Chroma
```

---

### File ingestion (.txt)

User can import files.

Pipeline:

```
txt file
↓
text loader
↓
chunking
↓
embedding
↓
vector storage
```

---

### Folder scanning

System can scan a folder:

```
data/raw_journals/
```

Workflow:

```
scan folder
↓
read txt files
↓
process journal
↓
move processed files to
data/processed_journals/
```

Purpose:

- prevent duplicate ingestion
- batch import journals

---

# 10. Text Chunking

Large texts are split before embedding.

Chunk function:

```
chunk_size = 400 tokens
```

Purpose:

- improve retrieval quality
- avoid long embedding vectors

---

# 11. Persona Reasoning System

The system implements **multi-agent reasoning** using five personas.

Personas:

```
Strategist
Philosopher
Discipline
Observer
Emotional
```

Each persona has a separate prompt configuration.

Example persona config:

```
{
  name: "Strategist",
  prompt: "Provide strategic analysis and practical solutions"
}
```

---

### Persona reasoning pipeline

```
User query
↓
memory context injected
↓
persona prompt
↓
LLM call
↓
response generated
```

Each persona runs **sequentially**.

```
Strategist
↓
Philosopher
↓
Discipline
↓
Observer
↓
Emotional
```

Outputs are displayed separately in CLI.

Example output:

```
AI:

[Strategist]
...

[Philosopher]
...

[Discipline]
...

[Observer]
...

[Emotional]
...
```

---

# 12. CLI Interface

The system uses a **terminal-based interface**.

Main menu:

```
Chat
Journal
Import journal file
Scan journal folder
Exit
```

Chat mode allows conversational interaction.

---

# 13. Thinking Indicator (UX Feature)

A timer indicator informs the user that the AI is processing.

Example:

```
You: I feel anxious about studying
AI thinking... 0s
AI thinking... 1s
AI thinking... 2s
```

Implementation:

- separate thread
- updates a single terminal line
- stops when AI response completes

---

# 14. Concurrency

Thinking indicator uses:

```
Python threading
```

Two parallel operations:

```
Thread 1 → AI reasoning
Thread 2 → thinking timer
```

Timer stops when reasoning finishes.

---

# 15. Project Folder Structure

```
second-me/

backend/
   embedding/
   memory/
   persona/
   rag/

cli/
   main.py

data/
   raw_journals/
   processed_journals/
   chroma_db/

venv/
```

---

# 16. Backend Components

### Memory Layer

Handles:

```
embedding
storage
retrieval
ranking
```

Files:

```
memory_service.py
chunk_service.py
journal_service.py
journal_scanner.py
memory_ranker.py
```

---

### Persona Layer

Handles reasoning personalities.

Files:

```
persona_loader.py
persona_engine.py
configs/
```

---

### RAG Layer

Handles retrieval orchestration.

File:

```
rag_service.py
```

---

### LLM Layer

Handles model interaction with Ollama.

Responsibilities:

```
send prompt
stream response
return tokens
```

---

# 17. Performance Constraints

Target hardware:

```
CPU laptop
no GPU
4 cores
```

Optimization decisions:

```
quantized model
CLI interface
small context window
limited retrieval size
```

Avoided features:

```
model fine-tuning
large pipelines
multi-stage LLM reasoning
```

---

# 18. Current Capabilities

The system currently supports:

```
local LLM
vector memory
RAG retrieval
memory ranking
multi-persona reasoning
journal ingestion
file ingestion
folder scanning
CLI interface
thinking indicator
```

---

# 19. System Type

This system can be categorized as:

```
Personal Cognitive AI System
```

or

```
Digital Twin Prototype
```

---

# 20. Future Extensions (Optional)

Potential upgrades:

```
parallel persona execution
emotion tagging
memory graph
reflection engine
auto-learning personality
recency weighting improvements
```

---

# 21. Key Design Principle

The system intentionally avoids fine-tuning.

Core idea:

```
Personal AI
=
Memory
+ Retrieval
+ Persona reasoning
```

---

# End of Report

---

Сайнаа, хэрвээ хүсвэл би дараагийн алхамд **өөр AI системүүд 100% ойлгох түвшний** илүү **супер-цэвэр “system specification document”** (architecture diagram + module contracts + API spec) хийж өгч чадна.
Тэрийг өгвөл **ямар ч AI system чиний төслийг шууд үргэлжлүүлж чадна**.
