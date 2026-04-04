# 2026-03-31 — 學習指南 v9 大補強

## 我們做了什麼？

參考 [claude.nagdy.me](https://claude.nagdy.me/) 這個互動式 Claude Code 學習平台，對照我們的指南找出 7 個缺口，逐一補強。

## 補強了什麼？

| 項目 | 變化 |
|------|------|
| 第 15 章斜線指令 | 5 個 → 30+ 個，分 7 類（基本/Session/專案/開發/自動化/其他） |
| 第 15 章 CLI Flags | 新增完整 flag 表 + 組合範例（`-p` + `--output-format json` 等） |
| 第 15 章快捷鍵 | 補充 `Ctrl+G`（外部編輯器開計畫）、`Ctrl+K`（搜尋） |
| 第 17 章 Permission | 3 種 → 6 種模式，新增 Allow/Deny Patterns、Auto Mode 信任設定、企業管控 |
| 第 20 章 Hooks | 2 種事件 → 8 種事件，新增 4 種實作方式（command/prompt/agent/http）、Matcher、Scoping |
| 第 25 章 Agent | 補完整 frontmatter（15 個選項）、4 種呼叫方式、存放位置優先級、Agent 鏈、Resumable、Agent Teams |
| 第 25 章 Workflow | 新增 4 個 Pattern（Develop and Verify、Parallel Review、Batch Processing、GitHub App） |
| 新增第 26 章 Plugins | 完整章節：架構、manifest、安裝分發、命名空間、LSP、環境變數、Marketplace、Inline Plugin |
| 新增附錄 C | Configuration Files 全覽：所有設定檔位置、作用、優先級地圖 |

## 為什麼這樣做？

### 為什麼參考 claude.nagdy.me？

它是一個結構化的互動學習平台，把 Claude Code 的功能按 Beginner → Intermediate → Advanced 分成 11 個模組。它的 Cheat Sheet 頁面特別完整，一張表就能看出我們的指南缺了什麼。

### 為什麼 Plugins 要獨立一章？

原本標記「等功能穩定後補充」，但 claude.nagdy.me 已經有完整的 Plugin 教學（包括 v2.1.80 的 Inline Plugin），顯示功能已經成熟。Plugin 是 Skill/Agent/Hook/MCP 的「打包」機制，不獨立一章的話讀者會不知道這些東西可以組合。

### 為什麼斜線指令要從 5 個擴充到 30+？

原本只列了最基本的 5 個，但實際上斜線指令是使用者最常用的互動方式。少列就等於讓讀者不知道有 `/diff`、`/plan`、`/batch` 這些強大功能。

## 學到的小知識

### 1. Hook 有 4 種實作方式，不只是 command

之前指南只教了 `command` 類型（跑 shell 指令）。但 `prompt` 類型（讓 Claude 自我檢查）可能更實用 — 例如 Stop hook 搭配 prompt 可以讓 Claude 每次回覆結束時自動驗證完成條件。

### 2. Permission Mode 的 auto 模式很聰明

不是簡單的「全部允許」，而是有一個分類器在背後判斷每個操作是否安全。搭配 `autoMode.environment` 的信任設定，可以做到「信任公司 repo 的操作，但外部操作還是要問」。

### 3. Agent Teams 是實驗性但很有潛力

需要設環境變數 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 才能啟用。跟普通的多 Agent 不同，Teams 有共享任務清單和信箱系統，Agent 之間可以互相溝通。

### 4. Plugin 的 LSP 整合是隱藏殺手功能

`.lsp.json` 可以讓 Claude 獲得即時的程式碼診斷（型別錯誤、未使用變數等），不用等到跑 build。這對 TypeScript 專案特別有用。

## 資料來源

- [claude.nagdy.me](https://claude.nagdy.me/) — 互動式學習平台，11 個模組 + Cheat Sheet + Config Builder
- 特別有用的頁面：`/learn/plugins`（Plugin 完整教學）、`/learn/subagents`（Agent 詳細設定）、`/learn/workflows`（Workflow Patterns）、`/reference`（Cheat Sheet）
