# 2026-03-29 — Claude Code 學習指南製作全記錄

## 我們做了什麼？

從零開始打造了一份 **25 章的 Claude Code 完全學習指南**，同時有 Markdown 版（文字）和 HTML 版（漂亮的網頁，有側邊欄導航）。

整個過程經歷了 8 個版本的迭代：

| 版本 | 變化 |
|------|------|
| v1 | 10 章，純文字說明 |
| v2 | 20 章，加入「我的記帳本」貫穿全書的實作專案 |
| v3 | 補強 Agent Loop、Token 管理、安全觀念（參考 learn-claude-code repo） |
| v4 | 擴充到 24 章：新增 Model 選擇、Hooks、TDD、Agent 編排（參考 everything-claude-code repo） |
| v5 | 25 章：新增 Skill 系統章節（參考 YT 影片字幕） |
| v6 | Humanizer 去 AI 味 + 縮寫全稱展開（13 個專有名詞） |
| v7 | 讀者分流指引 + 6 個進階實戰（解決「高手不屑看，小白看不懂」的問題） |
| v8 | 官方文件補強：Rewind、快捷鍵、語音、圖片PDF、Sandbox、Custom Agent、Remote Control |

最後還補了「怎麼打開終端機」和「程式碼框三種意思」的說明，確保真正的初學者不會在第 3 章就卡住。

## 為什麼這樣做？

### 為什麼要貫穿一個練習專案（記帳本）？

光說「你可以改檔案」沒有感覺。需要一個具體的專案讓讀者**親手操作**，才能真的學會。就像學游泳不能只看課本，得下水。

### 為什麼要 25 章不是 10 章？

10 章的時候都是「說明書式」的文字，讀者看完只知道 Claude Code 能做什麼，但不知道怎麼做。25 章的版本每個知識點都有「動手做」的練習。

### 為什麼要讀者分流指引？

因為發現一個尷尬問題：前面太基礎（高手覺得浪費時間），後面太進階（小白跟不上）。加了分流指引後，四種讀者都能找到自己的入口。

## 學到的小知識

### 1. 用 GitHub repo 當內容來源超有效

我們參考了三個 GitHub repo：
- `shareAI-lab/learn-claude-code` — 底層原理（Agent Loop、Context 壓縮）
- `affaan-m/everything-claude-code` — 進階功能（Hooks、TDD、Eval、Agent 編排）
- `nextlevelbuilder/ui-ux-pro-max-skill` — 第三方 Skill 怎麼做

每個 repo 都有我們指南缺少的東西。**把別人的開源知識整合進自己的教材**，比自己從零想高效十倍。

### 2. Skill 的精髓是三層架構

```
Command（便利貼）→ Skill（操作手冊）→ Agent（有專長的員工）
```

- Command：一張紙寫得完的固定指令
- Skill：提供知識和流程，但不會自己判斷
- Agent：有自己的角色、工具、記憶，能獨立思考

### 3. 兩個前端 Skill 搭配使用效果最好

- `ui-ux-pro-max`：給具體的設計數據（色票、字體、產業推薦）
- `frontend-design`：確保最終成品有創意、不無聊

一個負責「對的選擇」，一個負責「美的呈現」。

### 4. Humanizer 的雙重審查是關鍵

zh-TW 版省略了原版的步驟 6-9（改完後自問「哪裡還像 AI？」再改一次）。我們合併了兩邊的優勢：中文內容 + 原版的 9 步流程。

### 5. 官方文件是寶藏

光是 docs.anthropic.com 就有 70+ 頁文件，我們的指南只覆蓋了一半左右。最被低估的功能：
- **Rewind（Esc+Esc）**— 隨時回溯修改，比 Git 更即時
- **Effort Level** — 控制思考深度，省錢又省時間
- **Custom Agent** — 自己定義 Agent 的角色和工具限制

## 遇到的問題與解決方式

### 問題 1：章節重新編號地獄

每次插入新章節，後面的所有章節都要改編號。MD 和 HTML 兩個檔案要同步改。

**解法：** 用 Agent 背景並行處理，一個改 MD、一個改 HTML，同時給明確的「從底部往上改」指令避免衝突。

### 問題 2：Python 指令在 Windows 上是 `python` 不是 `python3`

UI/UX Pro Max 的搜尋腳本用 `python3`，但 Windows 上只認 `python`。

**解法：** 先跑 `python --version` 確認，然後改用 `python` 執行。

### 問題 3：npx 互動式安裝在自動化時會卡住

`npx uipro-cli init` 需要選擇平台，不支援非互動模式。

**解法：** 加上 `--ai claude` 參數跳過選擇，或從 home 目錄執行讓它安裝到全域 skills。

## 未來小提醒

- 官方文件還有 **Plugins 系統**、**Channels（Telegram/Discord 整合）**、**Agent Teams** 等功能沒加進指南，等這些功能穩定後可以考慮補充
- 指南的 HTML 版沒有搜尋功能，如果內容繼續增長可以考慮加上
- 目前 HTML 版的 code block 沒有語法高亮（syntax highlighting），未來可以加 Prism.js 或 Highlight.js
- 記得定期對照官方文件更新指南，Claude Code 更新很快
