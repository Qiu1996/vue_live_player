<script setup>
import { onMounted, ref, onUnmounted, watch } from "vue";

const props = defineProps(["streamId", "nickname"]);
const messages = ref([]);
const inputMessage = ref("");

let ws = null;

watch(() => props.streamId, (newStreamId) => {
  if (!newStreamId) {
    console.log('尚未建立直播，聊天室待命中...')
    return
  }
  if (ws) {
    return
  }
  const wsUrl = import.meta.env.DEV
    ? `ws://localhost:8000/ws/chat/${props.streamId}`
    : `wss://vue-live-player.zeabur.app/ws/chat/${props.streamId}`;

  ws = new WebSocket(wsUrl);

  ws.onopen = () => {
    console.log("ws 連線成功");
  }

  ws.onmessage = (e) => {
    messages.value.push(e.data)
  }

  ws.onclose = () => {
    console.log("ws 連線關閉")
  }

}, { immediate: true })

onUnmounted(() => {
  if (ws) {
    ws.close()
  }
})

function sendMessage() {
  if (inputMessage.value.trim() && ws) {
    const message = `[${props.nickname}]${inputMessage.value}`
    ws.send(message)
    inputMessage.value = ''
  }
}

</script>

<template>
  <div class="chat-area">
    <h3>聊天室</h3>

    <!-- 訊息列表 -->
    <el-scrollbar v-if="!props.streamId" height="600px">
      <h4> 尚未建立直播，聊天室待命中... </h4>
    </el-scrollbar>
    <el-scrollbar v-else height="600px">
      <div v-for="(msg, index) in messages" :key="index">
        {{ msg }}
      </div>
    </el-scrollbar>

    <!-- 輸入框 -->
    <div class="input-msg">
      <el-input v-if="!props.streamId" disabled >
        <template #append>
          <el-button>發送</el-button>
        </template>
      </el-input>
      <el-input v-else v-model="inputMessage" placeholder="輸入訊息..." >
        <template #append>
          <el-button @click="sendMessage">發送</el-button>
        </template>
      </el-input>
    </div>
  </div>
</template>

<style scoped>
:deep(.el-scrollbar){
  padding: 0 10px;
}

h3{
  padding: 10px;
  border-bottom: 1px solid black;
}

.input-msg{
  padding: 10px;
  border-top: 1px solid black;
}
</style>
