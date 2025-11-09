<script setup>
import '@mux/mux-player';
import { ref } from 'vue';


const PLAYBACK_ID = ref(null);
const STREAM_KEY = ref(null);
const STREAM_URL = ref("https://player.mux.com/");
const API_URL = import.meta.env.DEV
  ? 'http://localhost:8000'
  : 'https://vue-live-player.zeabur.app'

async function postapi(){
  try{
    const res = await fetch(`${API_URL}/create_stream`, {
      method: 'POST'
    });
    const date = await res.json();
    PLAYBACK_ID.value = date.playback_id;
    STREAM_KEY.value = date.stream_key;

  }catch(e){
    console.log('err: ', e);
  }

}

</script>

<template>
<button @click="postapi">Click</button>
<div v-if="PLAYBACK_ID">
  <p>STREAM_KEY: {{STREAM_KEY}}</p>
  <a :href="STREAM_URL + PLAYBACK_ID">串流網址</a>
</div>
</template>

<style scoped>
</style>
