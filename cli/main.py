from InquirerPy import inquirer
from rich.console import Console
from backend.chat_service import chat_loop 
from backend.chat_service import persona_chat_loop
from backend.memory.journal_service import add_journal_entry, import_journal_file
from backend.memory.journal_scanner import scan_journal_folder
from backend.memory.memory_service import search_memory
import sys

console = Console()

# журналийн цэс хэсэг эндээс хэрэглэгч өөрийн талаарх мэдээллийг олон байлаар илгээж уншуулж болно
def journal_menu():
    try:
        sub = inquirer.select(
            message="Журналы сонголт:",
            choices=[
                "Гараас бичих",
                "txt файл импортлох",
                "Журналын хавтас скан хийх",
                "Буцах"
            ],
        ).execute()

        if sub == "Гараас бичих":

            text = input("\nГараас бичвэр оруулах:\n")

            add_journal_entry(text)

            console.print("\nГар бичвэр журнал амжилттай хадгалагдлаа.", style="green")


        elif sub == "txt файл импортлох":

            path = input("\ntxt файлын зам:\n")

            import_journal_file(path)

            console.print("\nФайл амжилттай импорт хийгдлээ", style="green")

        elif sub == "Журналын хавтас скан хийх":

            scan_journal_folder()

            console.print("\nБүх журналын файл уншигдлаа", style="green")
    
    except KeyboardInterrupt:
        return

# хэрэглэгч нь өөрийн өгсөн дурсамж буюу мэдээлэл дундаас хайх боломжтой
def search_memory_user():
    try:
        print("\nДурсамж хайх(Exit гэж бичээд гарна):\n")

        query = input("\nЯмар дурсамж хайх вэ: ")

        if query.lower() == "exit":
            return

        results = search_memory(query)

        if not results:
            print("\nДурсамж олдсонгүй.\n")
            return

        print("\nОлдсон дурсамжууд:\n")

        for i, memory in enumerate(results, 1):

            text = memory["text"]
            meta = memory["metadata"]

            importance = meta.get("importance", "unknown")

            print(f"{i}. {text}")
            print(f"   importance: {importance}\n")
    
    except KeyboardInterrupt:
        return

        
# хэрэглэгч нь 5 persona дундаас сонгон ганцаарчлан ярих боломжтой
def talk_persona():
    try:
        print("\n🧠 Аль хувь хүнтэй ярилцах вэ?\n")
        choice1 = inquirer.select(
            message="Me-v2",
            choices=[
                "strategist",
                "philosopher",
                "discipline",
                "rational",
                "emotional",
                "Буцах"
                ],
            ).execute()
        if choice1 == "Буцах":
            return
        
        persona = choice1

        print(f"\n💬 {persona} persona-тай ярьж байна.\n")

        persona_chat_loop(persona)
    
    except KeyboardInterrupt:
        return

def main_menu():    
    try:
        while True:
            choice = inquirer.select(
                message="Me-v2",
                choices=[
                    "Чат",
                    "Журнал",
                    "Дурсамж хайх",
                    "Хувь хүнтэй ярих",
                    "Гарах"
                ],
            ).execute()

            if choice == "Чат":
                chat_loop()

            elif choice == "Журнал":
                journal_menu()
            elif choice == "Дурсамж хайх":
                search_memory_user()
            elif choice == "Хувь хүнтэй ярих":
                talk_persona()
            elif choice == "Гарах":
                break
    except KeyboardInterrupt:
        console.print("\n\nMe-v2 зогслоо.", style="red")
        sys.exit(0)

def main():
    main_menu()

if __name__ == "__main__":
    main()
    