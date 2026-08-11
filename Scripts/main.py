from pathlib import Path
from gemma4 import ask_gemma
import uuid
from sql_conversation import *

db_conversation = "../conversation/conversation_history.db"
db_memory = "../conversation/memory.db"
vault_path = Path("/home/janosch/AI-ML-Systems/AI & ML Systems")


def get_notes():
    return list(vault_path.rglob("*.md"))

def read_notes(path):
    return path.read_text(encoding="utf-8")

if __name__ == "__main__":
    create_database(db_conversation)
    create_database(db_memory)

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
            prompt_file="../prompt.txt",
            question=question,
            context=context
        )

        print(f"Antwort: {answer}")

        conversation_id = str(uuid.uuid4())
        insert_message(db_conversation, conversation_id, "user", question)
        insert_message(db_conversation, conversation_id, "assistant", answer)

