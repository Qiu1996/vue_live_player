<script setup>
import '@mux/mux-player'
import Chat from "./Chat.vue"
import { useRoute } from 'vue-router'
import { ref, onUnmounted } from 'vue'
import {
  STATUS_TEXT,
  STATUS_TYPE,
  API_URL
} from "../constants.js"

const ROUTE = useRoute()
const PLAYBACK_ID = ROUTE.params.playbackId
const STREAM_STATUS = ref("unknown")
const STREAM_ID = ref(null)
let pollingInterval = null;

function startPolling(){
  pollingInterval = setInterval(async () => {
    const res = await fetch(`${API_URL}/view_stream_status/${PLAYBACK_ID}`);
    const data = await res.json();
    STREAM_STATUS.value = data.status;
    STREAM_ID.value = data.stream_id
    console.log("View >>> ", STREAM_ID.value);
    if(data.status === 'unknown' || data.status === 'video.live_stream.disconnected'){
      clearInterval(pollingInterval);
    }
  }, 3000)
}

startPolling();

onUnmounted(() => {
  if(pollingInterval){
    clearInterval(pollingInterval);
  }
})
</script>
<template>
<el-container>
<el-main style="border: 1px solid black">
<div v-if="STREAM_STATUS === 'unknown' || STREAM_STATUS === 'video.live_stream.disconnected'">
  <h2>直播已結束</h2>
  <p>感謝觀看</p>
</div>
<div v-else>
  <h2>直播畫面</h2>
  <el-form-item>
    <span>直播狀態 </span>
    <el-tag :type="STATUS_TYPE[STREAM_STATUS]" size="large">{{STATUS_TEXT[STREAM_STATUS]}}</el-tag>
  </el-form-item>
  <mux-player
    v-if="PLAYBACK_ID && PLAYBACK_ID !== 'null'"
    :playback-id="PLAYBACK_ID"
    controls
    autoplay
    muted
  ></mux-player>
</div>
</el-main>
<el-aside width="500px" style="border: 1px solid black">
  <Chat
    :stream-id="STREAM_ID"
    nickname="觀眾"
  />
</el-aside>
</el-container>

</template>
<style scoped></style>
