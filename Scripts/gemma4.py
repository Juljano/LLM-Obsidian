from ollama import chat
from sql_conversation import *

db_conversation = "../conversation/conversation_history.db"
db_memory = "../conversation/memory.db"

def read_assistant_prompt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def ask_gemma(prompt_file, question, context):

    messages = [{"role": "system", "content": read_assistant_prompt(prompt_file)}]

    print(messages)

    messages.extend(read_history_messages(db_conversation))
    messages.extend(read_memory(db_memory))

    messages.append(
        {
            "role": "user",
            "content": f"""
{context}

{question}
""",
        }
    )

    response = chat(model="gemma4:e2b", messages=messages)

    return response["message"]["content"]
