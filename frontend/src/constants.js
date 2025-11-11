  export const STATUS_TEXT = {
    'video.live_stream.active': '直播中',
    'video.live_stream.idle': '閒置',
    'video.live_stream.connected': '連線中',
    'video.live_stream.disconnected': '已斷線',
    'video.live_stream.recording': '錄製中',
    'video.live_stream.created': '尚未開啟串流',
    'unknown': '閒置'
  }

  export const STATUS_TYPE = {
    'video.live_stream.active': 'success',
    'video.live_stream.idle': 'info',
    'video.live_stream.connected': 'warning',
    'video.live_stream.disconnected': 'danger',
    'video.live_stream.recording': 'success',
    'video.live_stream.created': 'info',
    'unknown': 'info'
  }

  export const STREAM_SERVER_URL =
  'rtmps://global-live.mux.com:443/app'

  export const BASE_URL = import.meta.env.DEV
    ? 'http://localhost:5173/vue_live_player'
    : 'https://qiu1996.github.io/vue_live_player'

  export const API_URL = import.meta.env.DEV
    ? 'http://localhost:8000'
    : 'https://vue-live-player.zeabur.app'
