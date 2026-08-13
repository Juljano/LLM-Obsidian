import json
import re
from pathlib import Path
from gemma4 import ask_gemma
import uuid
from sql_conversation import *

__db_memory = "/home/janosch/KI & ML-Projekte/LLM-Obsidian/conversation/memory.db"
__vault_path = Path("/home/janosch/AI-ML-Systems/AI & ML Systems12")


def get_notes():
    return list(__vault_path.rglob("*.md"))

def read_notes(path):
    return path.read_text(encoding="utf-8")


def extract_memory(content):
    json_match = re.search(r"```json\s*(.*?)\s*```", content, re.DOTALL)
    memory = json.loads(json_match.group(1))
    return memory.get("Zusammenfassung") if memory else None

if __name__ == "__main__":
    all_notes = get_notes()
    if not all_notes:
        print("Keine Notizen gefunden.")
        context = ""
    else:
        context_parts = []
        for note in all_notes:
            relative_path = note.relative_to(__vault_path)
            context_parts.append(f"Pfad- & Dateiname: {relative_path} ---\n")
            context_parts.append(read_notes(note))
        context = "".join(context_parts)

while True:
    question = input("Stelle eine Frage an Denise ('exit' zum Beenden): ")

    if question.lower() == "exit":
        break

    answer = ask_gemma(question=question, context=context)

    print(f"Denise: {answer}")

    if "save" in answer and "true" in answer:
        print("Die Erinnerung wird gespeichert in die Datenbank.")
        memory = extract_memory(answer)
        conversation_id = str(uuid.uuid4())
        insert_memory(__db_memory, memory)


