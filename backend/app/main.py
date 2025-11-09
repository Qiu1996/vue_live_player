import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from mux_python import (
  Configuration,
  ApiClient,
  LiveStreamsApi,
  CreateLiveStreamRequest,
  PlaybackPolicy
)

load_dotenv()

app = FastAPI()

origins = ["http://localhost:5173", "https://qiu1996.github.io"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST"],
)

configuration = Configuration()
configuration.username = os.getenv('MUX_TOKEN_ID')
configuration.password = os.getenv('MUX_TOKEN_SECRET')

live_api = LiveStreamsApi(ApiClient(configuration))

@app.get("/")
def read_root():
  return {"Hello": "from backend!"}

@app.post("/create_stream")
def create_stream():
  try:
    create_request = CreateLiveStreamRequest(
      playback_policy=[PlaybackPolicy.PUBLIC]
    )

    live_stream = live_api.create_live_stream(create_request)

    return {
      "stream_key": live_stream.data.stream_key,
      "playback_id": live_stream.data.playback_ids[0].id
    }

  except Exception as e:
    return {"error": str(e)}
