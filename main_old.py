import json
import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from generate_message import generate_scam_message
from generate_response import generate_scam_response
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conversation_histories = {}


class Message(BaseModel):
    session_id:str
    content: str


@app.get("/")
def root():
    return {"messages:": "Hello World!"}


@app.post('/initial')
def get_response():
    session_id = str(uuid.uuid4())
    initial_scam_message = generate_scam_message()
    conversation_histories[session_id] = [
        {"role":"assistant", "content": initial_scam_message}
    ]
    # conversation_history.append({"role": "assistant", "content":initial_scam_message})
    return {"res": initial_scam_message}

@app.post('/chat')
def chat(user_message: Message):   
    session_id = user_message.session_id

    if session_id not in conversation_histories:
        raise HTTPException(status_code=400, detail="Session ID tidak ditemukan")

    # Ambil riwayat percakapan untuk session ini
    conversation_history = conversation_histories[session_id]

    # Generate response dari scammer
    response = generate_scam_response(user_message.content, conversation_history)

    # Simpan pesan ke riwayat percakapan
    conversation_history.append({"role": "user", "content": user_message.content})
    conversation_history.append({"role": "assistant", "content": response})

    return {"scammer": response}



    # response = generate_scam_response(user_message.content, conversation_history)
    # conversation_history.append({"role": "user", "content": user_message.content})
    # conversation_history.append({"role": "assistant", "content": response})
    # return {"scammer": response}




# conversation_history = []
# print("Chatbot edukasi scam dimulai! Ketik 'exit' untuk keluar.\n")

#     # Generate pesan scam awal
# initial_scam_message = generate_scam_message()
# print(f"Scammer: {initial_scam_message}")
# conversation_history.append({"role": "assistant", "content": initial_scam_message})

# while True:
#     user_input = input("Anda: ")
#     if user_input.lower() == 'exit':
#         print("Chatbot ditutup.")
#         break

#     response = generate_scam_response(user_input, conversation_history)
#     conversation_history.append({"role": "user", "content": user_input})
#     conversation_history.append({"role": "assistant", "content": response})
#     print(f"Scammer: {response}")