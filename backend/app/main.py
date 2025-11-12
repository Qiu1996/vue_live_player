import os
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from datetime import datetime, timedelta
from mux_python import (
  Configuration,
  ApiClient,
  LiveStreamsApi,
  CreateLiveStreamRequest,
  PlaybackPolicy
)

load_dotenv()

logging.basicConfig(
  level=logging.INFO,
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

app = FastAPI()

stream_states = {}

active_connections = {}

playback_to_stream = {}

origins = ["http://localhost:5173", "https://qiu1996.github.io"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST", "DELETE"],
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
    stream_key = live_stream.data.stream_key
    stream_id = live_stream.data.id
    playback_id = live_stream.data.playback_ids[0].id

    stream_states[stream_id] = {
      "status": "unknown",
      "playback_id": playback_id
    }
    playback_to_stream[playback_id] = stream_id

    logger.info(f"建立直播成功: stream_id={stream_id}")
    return {
      "stream_key": stream_key,
      "playback_id": playback_id,
      "stream_id": stream_id
    }

  except Exception as e:
    logger.error(f"建立直播失敗: {str(e)}")
    return {"error": str(e)}

@app.post("/webhook")
def receive_webhook(request: dict):
  stream_id = request.get("data", {}).get("id")
  event_type = request.get("type")

  logger.info(f"收到 Webhook: {event_type}, stream_id={stream_id}")
  if stream_id and stream_id in stream_states:
    stream_states[stream_id]["status"] = event_type
  return {"status": "received"}

@app.get("/stream_status/{stream_id}")
def get_stream_status(stream_id):
  data = stream_states.get(stream_id, {})
  status = data.get("status", "unknown")
  return {"stream_id": stream_id, "status": status}

@app.get("/view_stream_status/{playback_id}")
def get_view_stream_status(playback_id):
  stream_id = playback_to_stream.get(playback_id)
  if stream_id:
    status = stream_states[stream_id].get("status", "unknown")
    return {"status": status, "stream_id": stream_id}
  return {"status": "unknown", "stream_id": None}


@app.delete("/delete_stream/{stream_id}")
def delete_stream(stream_id):
  try:
    live_api.delete_live_stream(stream_id)
    playback_id = stream_states.get(stream_id, {}).get("playback_id")
    stream_states.pop(stream_id, None)
    if playback_id:
      playback_to_stream.pop(playback_id, None)
    logger.info(f"刪除直播: {stream_id}")
    return {"stream_id": stream_id, "status": "deleted"}
  except Exception as e:
    logger.error(f"刪除直播失敗: {stream_id}, 錯誤: {str(e)}")
    return {"error": str(e)}


def clean_idle_stream():
  try:
    streams = live_api.list_live_streams()
    logger.info(f"開始清理閒置 stream，共 {len(streams.data)} 個")
    now = datetime.now()

    for stream in streams.data:
      created_at = datetime.fromtimestamp(int(stream.created_at))
      idle_time = now - created_at
      if stream.status == 'idle' and idle_time > timedelta(hours=24):
        live_api.delete_live_stream(stream.id)
        playback_id = stream_states.get(stream.id, {}).get("playback_id")
        stream_states.pop(stream.id, None)
        if playback_id:
          playback_to_stream.pop(playback_id, None)
        logger.info(f"刪除閒置 stream: {stream.id}")

  except Exception as e:
    logger.error(f"清理失敗: {str(e)}")

@app.websocket("/ws/chat/{stream_id}")
async def ws_chat(websocket: WebSocket, stream_id: str):
  await websocket.accept()

  if stream_id not in active_connections:
    active_connections[stream_id] = []
  active_connections[stream_id].append(websocket)

  try:
    while True:
      data = await websocket.receive_text()

      for connection in active_connections[stream_id]:
        await connection.send_text(data)
  except WebSocketDisconnect:
    active_connections[stream_id].remove(websocket)
    logger.info(f"WebSocket 斷線: stream_id={stream_id}")


scheduler = BackgroundScheduler()
scheduler.add_job(clean_idle_stream, 'interval', hours=24)
scheduler.start()
logger.info("APScheduler 已啟動，每 24 小時清理一次閒置 stream")
