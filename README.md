# Vue Live Player

## 專案簡介
---
一個輕量級直播串流應用，展示影音串流的完整流程：
從 OBS 推流、透過 Mux 處理轉碼與分發，到 Vue 前端播放。

## 技術架構
---

### 後端
- **Python 3.12**
- **FastAPI** - Web 框架
- **Uvicorn** - ASGI 伺服器
- **mux-python SDK** - Mux API 客戶端
- **uv** - 套件管理

### 前端
- **Vue 3** - 前端框架
- **Vite** - 建置工具

### 串流相關
- **推流端**: OBS Studio (RTMP/RTMPS)
- **Mux** - 串流服務
- **Mux Player** - 播放器

## 專案結構
---
```
vue_live_player/
├── backend/          # FastAPI 後端
│   ├── app/
│   │   ├── main.py
│   │   ├── schemas.py
│   │   └── data_generator.py
│   ├── pyproject.toml
│   └── Makefile
└── frontend/         # Vue 3 前端
    ├── src/
    ├── package.json
    └── vite.config.js
```

## 本地開發
---
### 後端

```bash
cd backend
uv sync                # 安裝依賴
make server           # 啟動開發伺服器
```
伺服器會在 `http://localhost:8000` 啟動。

### 前端
```bash
cd frontend
npm install           # 安裝依賴
npm run dev          # 啟動開發伺服器
```
前端會在 `http://localhost:5173` 啟動。

## 部署環境
---
- **後端**：[Zeabur](https://zeabur.com)
  - 生產網址：https://vue-live-player.zeabur.app/
  - API 文檔：https://vue-live-player.zeabur.app/docs

- **前端**：GitHub Pages
  - 透過 GitHub Actions 自動部署
  - 生產網址：https://qiu1996.github.io/vue_live_player/

## 環境變數設定

  1. 註冊 [Mux](https://www.mux.com) 帳號：https://mux.com
  2. 取得 API Token：
     - 登入 Mux Dashboard
     - Settings → Access Tokens
     - 建立新 Token，勾選「Mux Video」
  3. 在 `backend/` 目錄建立 `.env` 檔案：
     MUX_TOKEN_ID=your_token_id
     MUX_TOKEN_SECRET=your_token_secret
