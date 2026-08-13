from pathlib import Path
from gemma4 import ask_gemma
import uuid
from sql_conversation import *

db_memory = "/home/janosch/KI & ML-Projekte/LLM-Obsidian/conversation/memory.db"
vault_path = Path("/home/janosch/AI-ML-Systems/AI & cML Systems")


def get_notes():
    return list(vault_path.rglob("*.md"))

def read_notes(path):
    return path.read_text(encoding="utf-8")

if __name__ == "__main__":
    notes = get_notes()
    context = ""
    for note in notes:
        relative_path = note.relative_to(vault_path)

        context += f"\n--- {relative_path} ---\n"
        context += read_notes(note)

    while True:

        question = input(
            "Stelle eine Frage an Denise ('exit' zum Beenden): "
        )

        if question.lower() == "exit":
            break

        answer = ask_gemma(
            question=question,
            context=context
        )

        print(f"Antwort: {answer}")

        if "other" in answer:
            print("Die Antwort enthält 'other', daher wird sie nicht in die Datenbank eingefügt.")
            conversation_id = str(uuid.uuid4())
            insert_memory(db_memory, "user", question)
            insert_memory(db_memory, "assistant", answer)




    

