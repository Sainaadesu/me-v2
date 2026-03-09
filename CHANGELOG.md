# Second-me-v2 — Засварын тайлан

---

## 2026-03-09

### 1. `setup.py` — Entry point алдаа засав

**Асуудал:**  
`setup.py`-д entry point `cli.main:main` гэж бүртгэгдсэн байсан боловч `cli/main.py`-д `main()` функц байхгүй, зөвхөн `main_menu()` байсан. Тиймээс `me-v2` командыг ажиллуулахад `AttributeError` өгч байсан.

**Засвар:**  
`cli/main.py`-д `main()` wrapper функц нэмсэн.

```python
def main():
    signal.signal(signal.SIGINT, handle_interrupt)
    main_menu()
```

---

### 2. `setup.py` — Багц олдохгүй байсан алдаа засав

**Асуудал:**  
`find_packages()` нь `__init__.py` файл шаарддаг. Төсөлд `__init__.py` байхгүй тул ямар ч багц олдохгүй байсан. `pip install -e .` хийсэн ч кодын багцууд суугдахгүй байв.

**Засвар:**  
`find_packages()` → `find_namespace_packages()` болгон өөрчилсөн.

```python
from setuptools import setup, find_namespace_packages

setup(
    packages=find_namespace_packages(),
    ...
)
```

---

### 3. `setup.py` — `chromadb` dependency дутуу байсан

**Асуудал:**  
`backend/memory/memory_service.py`-д `import chromadb` хэрэглэгдэж байсан боловч `setup.py`-д dependency-д бүртгэгдээгүй байсан. `pip install -e .` хийхэд `chromadb` автоматаар суугддаггүй байсан тул `ModuleNotFoundError` өгч байв.

**Засвар:**  
`setup.py`-д `install_requires` нэмж, шаардлагатай бүх dependency-г бүртгэсэн. `.venv`-д `chromadb` суулгасан.

```python
install_requires=[
    "chromadb",
    "requests",
    "rich",
    "InquirerPy",
],
```

---

### 4. `C:\tools\me-v2.bat` — Working directory тогтоогүй байсан

**Асуудал:**  
Bat файл нь venv-г activate хийгээд шууд `python cli/main.py` ажиллуулдаг байв. Харин `data/chroma_db`, `backend/persona/configs` зэрэг харьцангуй зам (relative path) нь ажиллуулж буй директороос хамаардаг тул өөр фолдерт `me-v2` гэж дуудвал зам буруу болж алдаа өгдөг байв.

**Засвар:**  
Bat файлд `cd /d` нэмсэн.

```bat
@echo off
cd /d C:\Users\sotgo\Second-me-v2
call C:\Users\sotgo\Second-me-v2\.venv\Scripts\activate
python C:\Users\sotgo\Second-me-v2\cli\main.py
```

---

### 5. Ctrl+C — Программыг хаана ч цэвэрхэн зогсоох

**Асуудал:**  
- `signal.signal(SIGINT, ...)` нь зөвхөн `if __name__ == "__main__"` дотор дуудагдаж байсан тул `me-v2` entry point-ээр ажиллахад бүртгэгдэхгүй байв.  
- `chat_loop()`, `persona_chat_loop()` функцүүдэд `KeyboardInterrupt` боловсруулдаггүй байсан тул Ctrl+C дарахад timer thread зогсохгүй, traceback харагддаг байв.

**Засвар:**

**`cli/main.py`:**
- `signal.signal()` дуудлагыг `main()` функц руу шилжүүлсэн — entry point болон шууд ажиллуулах аль аль тохиолдолд бүртгэгдэнэ.
- `main_menu()` дотор `KeyboardInterrupt` барьж, `"Me-v2 stopped."` мессеж хэвлэн `sys.exit(0)` дуудна.

**`backend/chat_service.py`:**
- `chat_loop()` болон `persona_chat_loop()` хоёуланд `try/except KeyboardInterrupt` нэмсэн.
- Ctrl+C дарагдвал ажиллаж байгаа timer thread-г `stop_event.set()` + `timer_thread.join()`-аар цэвэрхэн зогсооно.

```python
except KeyboardInterrupt:
    if stop_event:
        stop_event.set()
    if timer_thread:
        timer_thread.join()
```

---

## Өөрчлөгдсөн файлууд

| Файл | Өөрчлөлт |
|------|-----------|
| `setup.py` | `find_namespace_packages()`, `install_requires` нэмсэн |
| `cli/main.py` | `main()` wrapper, `signal.signal()` шилжүүлсэн, Ctrl+C handler |
| `backend/chat_service.py` | `chat_loop()`, `persona_chat_loop()` Ctrl+C + timer cleanup |
| `C:\tools\me-v2.bat` | `cd /d` нэмсэн |
