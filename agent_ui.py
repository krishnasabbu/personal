# server.py
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from host_agent import root_agent

app = FastAPI()

async def event_stream(user_message: str):
    state = {"user_message": user_message}

    async for event in root_agent.run_iter(state):
        data = {
            "agent": event.get("agent", "unknown"),
            "output": event.get("output", str(event))
        }
        yield f"data: {data}\n\n"

@app.get("/chat/stream")
async def chat_stream(message: str):
    return StreamingResponse(event_stream(message), media_type="text/event-stream")
