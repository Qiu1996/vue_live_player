<script setup>
import '@mux/mux-player';
import { ref } from 'vue';


const PLAYBACK_ID = ref(null);
const STREAM_KEY = ref(null);
const STREAM_URL = ref("https://player.mux.com/");

async function postapi(){
  try{
    const res = await fetch("http://127.0.0.1:8000/create_stream", {
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
