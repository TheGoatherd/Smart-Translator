from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI()

class Schema(BaseModel):
    question: str

@app.post("/chat")
async def chat_function(data: Schema):
    completion = client.chat.completions.create(
        model="qwen-qwq-32b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a highly accurate and professional language translator. "
                    "Your task is to detect the input language and translate the text to English.\n"
                    "Respond strictly in the following format:\n"
                    "Language: <Detected Language>\n"
                    "Translation: <Translated Text in English>"
                ),
            },
            {
                "role": "user",
                "content": data.question,
            },
        ],
        temperature=0,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            answer += chunk.choices[0].delta.content

    return {"answer": answer}
