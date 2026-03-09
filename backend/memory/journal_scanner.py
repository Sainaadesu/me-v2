import os
import shutil

from backend.memory.journal_service import import_journal_file

RAW_FOLDER = "data/raw_journals"
PROCESSED_FOLDER = "data/processed_journals"


def scan_journal_folder():

    # Raw хавтас байхгүй бол алдаа өгөхөөс сэргийлнэ
    if not os.path.exists(RAW_FOLDER):
        print(f"Raw журналын хавтас олдсонгүй: {RAW_FOLDER}")
        return

    # Processed хавтас байхгүй бол үүсгэнэ
    os.makedirs(PROCESSED_FOLDER, exist_ok=True)

    files = os.listdir(RAW_FOLDER)

    for file in files:

        if file.endswith(".txt"):

            path = os.path.join(RAW_FOLDER, file)

            print(f"Импортлож байна: {file}")

            try:
                import_journal_file(path)
                new_path = os.path.join(PROCESSED_FOLDER, file)
                shutil.move(path, new_path)
                print(f"Processed хавтас руу шилжүүлэгдлээ: {file}")
            except Exception as e:
                print(f"Алдаа гарлаа ({file}): {e}")