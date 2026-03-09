from backend.persona.persona_engine import run_single_persona
from backend.persona.persona_engine import run_personas
from backend.rag.rag_service import retrieve_memories
from backend.utils.timer import thinking_timer
from rich.console import Console
import threading
import sys

# энэ хэсэг нь хэрэглэгчтэй харилцан ярилцах хэсгийг хариуцан авч буй энэ нт мөн 5 persona болон ганц хувь persona-тай ярилцах юм

console = Console()


def _run_in_thread(fn, *args):
    """fn-г daemon thread дотор ажиллуулж, (result, error) буцаана.
    Ctrl+C дарах үед stop_event тавьж, thread дуустал хүлээнэ."""
    stop_event = threading.Event()
    result_box = [None]
    error_box = [None]

    def worker():
        try:
            result_box[0] = fn(*args, stop_event)
        except Exception as e:
            error_box[0] = e

    worker_thread = threading.Thread(target=worker, daemon=True)
    timer_thread = threading.Thread(target=thinking_timer, args=(stop_event,))

    timer_thread.start()
    worker_thread.start()

    try:
        while worker_thread.is_alive():
            worker_thread.join(timeout=0.1)
    except KeyboardInterrupt:
        stop_event.set()
        worker_thread.join()
        timer_thread.join()
        console.print("\n\nMe-v2 зогслоо.", style="red")
        sys.exit(0)

    stop_event.set()
    timer_thread.join()

    if error_box[0]:
        raise error_box[0]

    return result_box[0]


# 5 persona ярих
def chat_loop():

    console.print("\nЧат горим ('exit' гэж бичвэл гарна)\n", style="green")

    try:
        while True:

            user = input("\nТа: ")

            if user.lower() == "exit":
                break

            memories = retrieve_memories(user)

            persona_outputs = _run_in_thread(run_personas, user, memories)

            if persona_outputs is None:
                continue

            console.print("\nAI:\n", style="cyan")

            for name, response in persona_outputs:
                console.print(f"[{name}]\n{response}\n")

    except KeyboardInterrupt:
        console.print("\n\nMe-v2 зогслоо.", style="red")
        sys.exit(0)


#ганц хувь хүнтэй ярилцах
def persona_chat_loop(persona):

    print("exit гэж бичвэл гарна.\n")

    try:
        while True:

            user_input = input("Та: ")

            if user_input.lower() == "exit":
                break

            response = _run_in_thread(run_single_persona, user_input, persona, [])

            if response is not None:
                print(f"\n{persona}: {response}\n")

    except KeyboardInterrupt:
        console.print("\n\nMe-v2 зогслоо.", style="red")
        sys.exit(0)