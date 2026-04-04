# 2026-03-29 — Skill 安裝與合併實戰

## 我們做了什麼？

安裝了兩個第三方 Skill，還動手合併了一個 Skill 的中英版本：

### 1. UI/UX Pro Max

一個設計智慧資料庫，有 67 種 UI 風格、161 套色票、73 組字體配對。

**安裝方式：**
```bash
# 從 home 目錄執行（安裝到全域 ~/.claude/skills/）
cd ~
npx uipro-cli init --ai claude
```

**它不是直接幫你設計**，而是提供設計數據讓 Claude 做更好的選擇。想像它是一本 500 頁的設計百科全書，Claude 可以隨時翻閱。

### 2. Humanizer 繁體中文版（合併版）

把 `blader/humanizer`（英文原版）和 `kevintsai1202/Humanizer-zh-TW`（繁中翻譯版）合併成一個最強版本。

**為什麼要合併？**

| | 原版（英文） | zh-TW 版 | 我們的合併版 |
|---|---|---|---|
| 語言 | 英文 | 繁中 | 繁中 |
| 規則數 | 25 | 24 | 24（移除英文才有的連字號規則） |
| 改寫流程 | 9 步（雙重審查） | 5 步（單次） | **9 步（雙重審查）** |
| 品質評分 | 無 | 50 分制 | **50 分制** |

合併版 = zh-TW 的中文內容 + 原版的雙重審查流程 + zh-TW 的品質評分。

**安裝位置：** `~/.claude/skills/humanizer-zh-tw/SKILL.md`

## 為什麼這樣做？

### 為什麼不直接用 zh-TW 版就好？

因為它省略了原版最重要的步驟：改完後自問「哪裡還像 AI？」然後再改一次。這個「第二輪自我批判」是品質差異的關鍵。就像寫作文——寫完馬上交 vs 放一下再檢查一遍，品質差很多。

### 為什麼不直接用英文原版？

因為它的觸發詞清單（「additionally」「crucial」「delve into」）是英文的。寫中文內容時，需要中文版的觸發詞（「此外」「至關重要」「深入探討」）才能真正抓到 AI 痕跡。

## 學到的小知識

### Skill 的本質就是一個 Markdown 檔案

不管多複雜的 Skill，核心都是一個 `SKILL.md`。它不是程式碼，是**給 Claude 看的操作手冊**。你可以直接打開來看、修改、合併。

### YAML frontmatter 裡的 description 是靈魂

```yaml
---
name: humanizer-zh-tw
description: 去除 AI 生成文字的痕跡，使文字更自然...
---
```

Claude 用 `description` 來決定要不要載入這個 Skill。寫得不好 = Claude 永遠不會自動觸發它。

### Skill 可以用 npx 安裝，也可以手動複製

- 有 CLI 安裝工具的（像 UI/UX Pro Max）→ `npx` 一行搞定
- 沒有的（像 Humanizer）→ `git clone` 到 `~/.claude/skills/`
- 自己做的 → 直接在 `.claude/skills/` 裡建資料夾和 SKILL.md

## 遇到的問題與解決方式

### npx 互動式選單卡住

`npx uipro-cli init` 跳出選單要你選平台，但自動化環境沒辦法選。

**解法：** 加 `--ai claude` 參數。不是每個 CLI 都支援這種跳過方式，要先看 `--help`。

### Python 版本問題

UI/UX Pro Max 的搜尋腳本寫 `python3`，Windows 上找不到。

**解法：** Windows 上用 `python`（不是 `python3`）。以後遇到類似問題，先跑 `python --version` 確認。

## 未來小提醒

- Skill 會持續更新，可以定期 `git pull` 拉新版本
- 如果裝了太多 Skill，Claude 的 Context Window 會被佔掉很多空間（每個 Skill 約 500-2000 token）
- 全域 Skill（`~/.claude/skills/`）會影響所有專案，不需要的可以移到特定專案的 `.claude/skills/` 裡
