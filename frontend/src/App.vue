<script setup>
import '@mux/mux-player';
import { ref, onUnmounted } from 'vue';


const API_URL = import.meta.env.DEV
  ? 'http://localhost:8000'
  : 'https://vue-live-player.zeabur.app'
const PLAYBACK_ID = ref(null);
const STREAM_KEY = ref(null);
const STREAM_ID = ref(null);
const STREAM_URL = ref("https://player.mux.com/");
const STREAM_STATUS = ref('unknown');
let pollingInterval = null;

async function postapi(){
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


</script>

<template>
<button @click="postapi">Click</button>
<div v-if="PLAYBACK_ID">
  <p>STREAM_KEY: {{STREAM_KEY}}</p>
  <p>PLAYBACK_ID: {{PLAYBACK_ID}}</p>
  <p>STREAM_ID: {{STREAM_ID}}</p>
  <p>串流狀態：{{STREAM_STATUS}}</p>
  <a :href="STREAM_URL + PLAYBACK_ID">串流網址</a>
</div>
</template>

<style scoped>
</style>
