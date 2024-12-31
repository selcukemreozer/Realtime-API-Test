import os
import json
import base64
import asyncio
import websockets
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.websockets import WebSocketDisconnect
from twilio.twiml.voice_response import VoiceResponse, Connect, Say, Stream
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
PORT = int(os.getenv("PORT", 5050))
SYSTEM_MESSAGE = (
    "You are a helpful and bubbly AI assistant who loves to chat about "
    "anything the user is interested in and is prepared to offer them facts."
    "You have a penchant for dad jokes, owl jokes, and rickrolling - subtly. "
    "Always stay positive, but work in a joke when appropriate."
)

VOICE = 'alloy'

LOG_EVENT_TYPES = [
'response. content done', 'rate_limits. updated', 'response. done',
'input_audio_buffer.committed', 'input_audio_buffer.speech_stopped',
'input_audio_buffer speech_started', 'session.created']

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set")

app = FastAPI()

@app.get("/", response_class=JSONResponse)
async def index_page():
    return {"message": "Twilio Media Stream Server is running!"}

@app.api_route("/incoming-call", methods=["GET" , "POST"]) 
async def handle_incoming_call(request: Request):
    response = VoiceResponse ()
    response.say ("Please wait while we connect your call to the A. I. voice assistant, powered by Twilio and the Open-A.I. Realtime API")
    response.pause (length=1)
    response.say ("Now, you can talk")
    host = request.url.hostname
    connect = Connect()
    connect.stream(url=f'wss: //{host}/media-stream')
    response. append (connect)
    return HTMLResponse(content=str(response),media_type="application/xm1")

