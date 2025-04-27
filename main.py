from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from generate_message import generate_scam_message
from generate_response import generate_scam_response
from user_input import Message
import uuid

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conversations = {}

@app.get('/root')
async def root():
    return {"message:": "Hello World"}

@app.post('/start_chat')
async def start_chat():
    """Memulai percakapan dan mengembalikan initial message serta session_id."""
    session_id = str(uuid.uuid4())  
    initial_scam_message = await generate_scam_message()
    
    conversations[session_id] = [{"role": "assistant", "content": initial_scam_message}]
    
    return {
        "session_id": session_id,
        "scammer": initial_scam_message
    }

@app.post('/chat')
async def chat(user_message: Message):
    session_id = user_message.session_id

    if session_id not in conversations:
        raise HTTPException(status_code=404, detail="Session ID not found")

    response = await generate_scam_response(user_message.content, conversations[session_id]) 
    conversations[session_id].append({"role": "user", "content": user_message.content})
    conversations[session_id].append({"role": "assistant", "content": response})
    
    return {"scammer": response}
