<script setup>
import '@mux/mux-player';
import { ref, onUnmounted, onMounted } from 'vue';
import Stream from "./components/Stream.vue"
import {
  STATUS_TEXT,
  STATUS_TYPE,
  STREAM_SERVER_URL,
  MUX_PLAYER_BASE_URL
} from "./constants.js"


const API_URL = import.meta.env.DEV
  ? 'http://localhost:8000'
  : 'https://vue-live-player.zeabur.app'

const PLAYBACK_ID = ref(null);
const STREAM_KEY = ref(null);
const STREAM_ID = ref(null);
const STREAM_STATUS = ref("unknown");
let pollingInterval = null;

async function createStream(){
  try{
    const res = await fetch(`${API_URL}/create_stream`, {
      method: 'POST'
    });
    const date = await res.json();
    PLAYBACK_ID.value = date.playback_id;
    STREAM_KEY.value = date.stream_key;
    STREAM_ID.value = date.stream_id;

    startPolling();
  }catch(e){
    console.log('err: ', e);
  }
}

function startPolling(){
  pollingInterval = setInterval(async () => {
    const res = await fetch(`${API_URL}/stream_status/${STREAM_ID.value}`);
    const data = await res.json();
    STREAM_STATUS.value = data.status;
    console.log(`STREAM_STATUS: `, STREAM_STATUS.value);
    if(data.status === 'video.live_stream.disconnected'){
      clearInterval(pollingInterval);
    }

  }, 3000)
}

onUnmounted(() => {
  if(pollingInterval){
    clearInterval(pollingInterval);
  }
})

async function deleteStream(){
  try{
    const res = await fetch(`${API_URL}/delete_stream/${STREAM_ID.value}`, {
      method: 'DELETE'
    });

    PLAYBACK_ID.value = null
    STREAM_KEY.value = null
    STREAM_ID.value = null
    STREAM_STATUS.value = 'unknown'

    if (pollingInterval) {
      clearInterval(pollingInterval)
      pollingInterval = null
    }

    ElMessage.success('刪除成功');
  }catch(e){
    console.log('err: ', e);
  }
}

</script>

<template>
<Stream
  :stream-key="STREAM_KEY"
  :stream-url="MUX_PLAYER_BASE_URL + PLAYBACK_ID"
  :stream-server="STREAM_SERVER_URL"
  :status-text="STATUS_TEXT[STREAM_STATUS]"
  :status-type="STATUS_TYPE[STREAM_STATUS]"
  :playback-id="PLAYBACK_ID"
  @create-stream="createStream"
  @delete-stream="deleteStream"
/>









</template>

<style scoped>

</style>
