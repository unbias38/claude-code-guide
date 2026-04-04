# 2026-03-29 — 前端設計實戰：兩個 Skill 搭配使用

## 我們做了什麼？

用兩個 Skill 搭配，把 25 章的 Claude Code 學習指南做成一個漂亮的網頁（`claude-code-guide.html`），有側邊欄導航、閱讀進度追蹤、滾動動畫。

### 搭配方式

| Skill | 角色 | 提供什麼 |
|-------|------|---------|
| **ui-ux-pro-max** | 設計數據顧問 | 色票、字體配對、UX 準則、產業推薦 |
| **frontend-design** | 美學創意總監 | 確保設計不無聊、有個性、不像 AI 生成 |

一個負責「選對的東西」，一個負責「做得好看」。

### 設計決策

從 UI/UX Pro Max 拿到的資料：
- **色票：** Indigo 主色 `#4F46E5` + 進度綠 `#22C55E`（教育類推薦）
- **字體：** Noto Serif TC（標題）+ Noto Sans TC（正文）+ JetBrains Mono（程式碼）
- **風格：** Claymorphism（教育類推薦），但我們調整成更專業的 Soft UI
- **UX 規則：** smooth scroll、sticky sidebar、prefers-reduced-motion

從 frontend-design 得到的創意方向：
- 顆粒感紋理（grain overlay）營造氛圍
- 終端機風格的程式碼區塊（紅黃綠三個點）
- 四種不同風格的 callout 框（生活比喻/動手做/警告/提示）
- 深色側邊欄像 IDE 的檔案樹
- 章節滾動時淡入動畫

## 為什麼這樣做？

### 為什麼不直接用一個 Skill？

**UI/UX Pro Max 單獨用**會做出「正確但無聊」的設計——色票對、字體對，但沒有個性。

**frontend-design 單獨用**會做出「漂亮但可能不適合」的設計——很有創意，但可能選了跟教育主題不搭的配色。

兩個一起用 = 正確 + 有趣。

### 為什麼選 Noto Serif TC + Noto Sans TC？

因為內容是繁體中文。UI/UX Pro Max 的字體資料庫有「Chinese Traditional」配對，專門針對繁中內容設計。Noto 字體的繁中支援最完整，不會出現缺字。

## 學到的小知識

### UI/UX Pro Max 的搜尋指令

```bash
# 產生完整設計系統推薦
python scripts/search.py "education documentation" --design-system -p "My Project"

# 搜尋特定領域
python scripts/search.py "elegant serif" --domain typography -n 5

# 搜尋 UX 準則
python scripts/search.py "sidebar navigation" --domain ux -n 5
```

它背後是一個 BM25 搜尋引擎，會在 15 個 CSV 資料庫裡找最匹配的結果。不是隨機推薦，是有排序邏輯的。

### CSS 變數讓整個設計系統可控

```css
:root {
    --primary: #4f46e5;
    --bg-content: #faf8f5;
    --font-serif: 'Noto Serif TC', serif;
}
```

只要改這幾個變數，整個頁面的配色和字體就會跟著變。這就是為什麼 UI/UX Pro Max 推薦的是「語意色票」（Primary、Secondary、Accent），而不是具體的十六進位色碼。

### IntersectionObserver 做滾動動畫

網頁裡章節滾動時的淡入效果，不是用 scroll event（效能差），而是用 `IntersectionObserver`（瀏覽器原生 API，效能好）。這是 frontend-design Skill 推薦的做法。

## 遇到的問題與解決方式

### UI/UX Pro Max 推薦的風格不完全適合

它推薦了 Claymorphism（軟 3D、圓潤、適合教育類），但記帳本指南是給開發者看的，不是給小孩看的。

**解法：** 不照單全收，取它推薦的色票和字體，但風格自己調整成更專業的方向。Skill 的推薦是起點，不是終點。

### 中文字體載入很慢

Noto Serif TC + Noto Sans TC 的完整字體檔很大（中文字體的宿命）。

**解法：** 用 Google Fonts 的 `display=swap`，讓頁面先用系統字體顯示，字體載入完再切換，避免白屏等待。

## 未來小提醒

- 如果要改設計風格，先跑 UI/UX Pro Max 的 `--design-system` 拿新的推薦，再讓 frontend-design 發揮創意
- HTML 目前是單一檔案（CSS + JS 都內嵌），如果要部署到正式環境，建議拆分成獨立檔案
- 目前沒有深色模式（dark mode），可以用 CSS 變數快速加上
- 網頁沒有搜尋功能，25 章的內容量已經需要了
