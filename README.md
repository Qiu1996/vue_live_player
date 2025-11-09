# Q's VuePlayer

## 專案簡介
一個輕量級直播串流應用，展示影音串流的完整流程：
從 OBS 推流、透過 Mux 處理轉碼與分發，到 Vue 前端播放。

## 技術架構
- **推流端**: OBS Studio (RTMP)
- **串流服務**: Mux (轉碼/CDN)
- **播放端**: Vue 3 + Mux Player
