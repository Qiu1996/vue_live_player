<script setup>
import { ref, watch } from 'vue'
const props = defineProps(["streamKey", "streamUrl", "streamServer", "streamStatus", "statusText", "statusType", "playbackId"]);
const emit = defineEmits(["create-stream", "delete-stream"]);
const localStreamKey = ref(props.streamKey)

watch(() => props.streamKey, (newVal) => {
  localStreamKey.value = newVal
})

function copy(text) {
  navigator.clipboard.writeText(text)
  ElMessage.primary('複製成功')
}

</script>

<template>
<el-container direction="vertical">
  <el-main>
    <h2>串流設定</h2>
    <el-button type="primary" @click="emit('create-stream')">建立直播</el-button>
    <el-button type="danger" @click="emit('delete-stream')">刪除直播</el-button>
    <el-form-item label="串流金鑰">
      <el-input
        style="width: 500px"
        v-model="localStreamKey"
        readonly
        type="password"
        show-password
      >
        <template #append>
          <el-button @click="copy(localStreamKey)">複製</el-button>
        </template>
      </el-input>
    </el-form-item>
    <el-form-item label="串流伺服器">
      <el-input
        style="width: 500px"
        :value="streamServer"
        readonly
      >
        <template #append>
        <el-button @click="copy(streamServer)">複製</el-button>
        </template>
      </el-input>
    </el-form-item>
    <el-form-item label="串流網址">
      <el-input
        style="width: 500px"
        :value="streamUrl"
        readonly
      >
        <template #append>
        <el-button @click="copy(streamUrl)">複製</el-button>
        </template>
      </el-input>
    </el-form-item>
    <el-form-item>
      <span>串流狀態 </span>
      <el-tag :type="statusType" size="large">{{statusText}}</el-tag>
    </el-form-item>
    <h2>串流畫面預覽</h2>
    <mux-player
      v-if="playbackId && playbackId !== 'null'"
      :playback-id="playbackId"
      controls
      autoplay
      muted
    ></mux-player>
    <div v-else class="videobox">尚未建立直播</div>
  </el-main>
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
