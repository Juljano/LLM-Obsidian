import json
import re
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


def extract_memory(content):
    json_match = re.search(r"```json\s*(.*?)\s*```", content, re.DOTALL)
    memory = json.loads(json_match.group(1))
    return memory.get("Zusammenfassung") if memory else None

if __name__ == "__main__":
    notes = get_notes()
    context = ""
    for note in notes:
        relative_path = note.relative_to(vault_path)

        context += f"\n--- {relative_path} ---\n"
        context += read_notes(note)

        print(context)

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

        print(f"Denise: {answer}")

        if "save" in answer and "true" in answer:
            print("Die Antwort enthält 'true', daher wird sie in die Datenbank eingefügt.")
            memory = extract_memory(answer)
            conversation_id = str(uuid.uuid4())
            insert_memory(db_memory, memory)




    

