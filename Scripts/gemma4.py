from ollama import chat
from sql_conversation import *

db_memory = "/home/janosch/KI & ML-Projekte/LLM-Obsidian/conversation/memory.db"
prompt_file = "/home/janosch/KI & ML-Projekte/LLM-Obsidian/config/prompt.txt"

def read_prompt_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def ask_gemma(question, context):


    messages = [{"role": "system", "content": read_prompt_file(prompt_file)}]
    messages.extend(read_memory(db_memory))

    messages.append(
        {
            "role": "user",
            "content": f"""
            {context}

            {question}
            """,
        })

    response = chat(model="gemma4:e2b", messages=messages)

    return response["message"]["content"]
