<script setup>
import '@mux/mux-player'
import Chat from "./Chat.vue"
import { ref, watch, onUnmounted, onMounted, computed } from 'vue'
import {
  STATUS_TEXT,
  STATUS_TYPE,
  STREAM_SERVER_URL,
  API_URL,
  BASE_URL
} from "../constants.js"

const PLAYBACK_ID = ref(null);
const STREAM_KEY = ref(null);
const STREAM_ID = ref(null);
const STREAM_URL = computed(() => `${BASE_URL}/#/view/${PLAYBACK_ID.value}`)
const STREAM_STATUS = ref("unknown");
let statusWs = null;

async function createStream(){
  try{
    const res = await fetch(`${API_URL}/create_stream`, {
      method: 'POST'
    });
    const data = await res.json();
    PLAYBACK_ID.value = data.playback_id;
    STREAM_KEY.value = data.stream_key;
    STREAM_ID.value = data.stream_id;

    connectWebSocket();
  }catch(e){
    console.log('err: ', e);
  }
}

function connectWebSocket(){
  const wsUrl = import.meta.env.DEV
    ?`ws://localhost:8000/ws/status/${STREAM_ID.value}`
    : `wss://vue-live-player.zeabur.app/ws/status/${STREAM_ID.value}`;

  statusWs = new WebSocket(wsUrl);

  statusWs.onopen = () => {
    console.log("狀態 WebSocket 連線成功");
  }

  statusWs.onmessage = (e) => {
    STREAM_STATUS.value = e.data;
    console.log(`狀態更新: ${e.data}`);
  }

  statusWs.onclose = () => {
    console.log("狀態 WebSocket 連線關閉");
  }
}

onUnmounted(() => {
  if(statusWs){
    statusWs.close();
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

    if (statusWs) {
      statusWs.close()
      statusWs = null
    }

    ElMessage.success('刪除成功');
  }catch(e){
    console.log('err: ', e);
  }
}



function copy(text) {
  navigator.clipboard.writeText(text)
  ElMessage.primary('複製成功')
}

</script>

<template>
<el-container>
  <el-main style="border: 1px solid black">
    <h2>串流設定</h2>
    <el-button type="primary" @click="createStream">建立直播</el-button>
    <el-button type="danger" @click="deleteStream">刪除直播</el-button>
    <el-form-item label="串流金鑰">
      <el-input
        style="width: 500px"
        v-model="STREAM_KEY"
        readonly
        type="password"
        show-password
      >
        <template #append>
          <el-button @click="copy(STREAM_KEY)">複製</el-button>
        </template>
      </el-input>
    </el-form-item>
    <el-form-item label="串流伺服器">
      <el-input
        style="width: 500px"
        :value="STREAM_SERVER_URL"
        readonly
      >
        <template #append>
        <el-button @click="copy(STREAM_SERVER_URL)">複製</el-button>
        </template>
      </el-input>
    </el-form-item>
    <el-form-item label="串流網址">
      <el-input
        style="width: 500px"
        :value="STREAM_URL"
        readonly
      >
        <template #append>
        <el-button @click="copy(STREAM_URL)">複製</el-button>
        </template>
      </el-input>
    </el-form-item>
    <el-form-item>
      <span>串流狀態 </span>
      <el-tag :type="STATUS_TYPE[STREAM_STATUS]" size="large">{{STATUS_TEXT[STREAM_STATUS]}}</el-tag>
    </el-form-item>
    <h2>串流畫面預覽</h2>
    <mux-player
      v-if="PLAYBACK_ID && PLAYBACK_ID !== 'null'"
      :playback-id="PLAYBACK_ID"
      controls
      autoplay
      muted
    ></mux-player>
    <div v-else >尚未建立直播</div>
  </el-main>
  <el-aside width="500px" style="border: 1px solid black">
    <Chat
      :stream-id="STREAM_ID"
      nickname="主播"
    />
  </el-aside>
</el-container>
</template>

<style scoped>
:deep(.el-tag__content) {
  font-size: 14px;
}

:deep(.el-form-item){
  margin: 10px;
}
</style>
