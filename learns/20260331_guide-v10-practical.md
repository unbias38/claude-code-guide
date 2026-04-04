# 2026-03-31 — 學習指南 v10 實戰篇

## 我們做了什麼？

在指南裡新增了「實戰篇」（4 章）和 7 個 Lab，解決「知識覆蓋全但實戰太少」的問題。

### 新增的實戰篇（第 27-30 章）

| 章 | 主題 | 交付物 |
|----|------|--------|
| 27 | Plan Mode 設計升級藍圖 | CLAUDE.md 專案紀律 + Next.js 空專案 + Git 分支策略 |
| 28 | Vibe Coding 功能迭代 | Feature Skill + Supabase DB + Auth + CRUD |
| 29 | 測試 Skill + CI/CD | 測試 Skill + 完整測試套件 + GitHub Actions + 分支保護 |
| 30 | 多 Agent + Code Review + 部署 | Git Worktree 並行 + Code Review Skill + 部署到 Vercel |

### 7 個 Lab 插入現有章節

| Lab | 章 | 練習內容 |
|-----|----|---------|
| 1 | 第 6 章 | 故意製造 bug 讓 Claude 找 |
| 2 | 第 7 章 | 一次給三個需求，觀察依序處理 |
| 3 | 第 12 章 | 寫嚴格 CLAUDE.md 看 Claude 會不會自動遵守 |
| 4 | 第 16 章 | 自己寫 Skill 並比較有/無 Skill 的差異 |
| 5 | 第 20 章 | 設定 Prettier auto-format Hook |
| 6 | 第 21 章 | TDD 完整走一遍（紅 → 綠 → 重構） |
| 7 | 第 23 章 | 用 MCP 連接外部 API |

## 為什麼這樣設計？

### 為什麼選「記帳本升級」而不是全新專案？

讀者從第 4 章就開始建記帳本，已經有感情。升級它比從零開始一個陌生專案更有動力。而且技術跳躍（HTML → Next.js）本身就是一個很好的 Vibe Coding 練習——你不需要會 React，只需要告訴 Claude 你要什麼。

### 為什麼每章有明確的「交付物」？

參考了 Graduate School Bootcamp 的設計：每個模組結束時有 Lab + 可驗收的成果。學習的成就感來自「我做出了一個東西」，不是「我讀完了一段文字」。

### 為什麼融入工作坊大綱？

用戶提供了一份中文工作坊大綱（CLAUDE.md 紀律、Vibe Coding 迭代、測試 Skill、CI/CD、多 Agent、Code Review），這些主題正好填補了指南最弱的部分。把它們融入實戰篇，每個主題都有具體的動手操作。

## 參考的課程

| 課程 | 借鑑了什麼 |
|------|-----------|
| Graduate School Bootcamp | 7 Labs + Capstone 的遞進結構 |
| Coursera / Vanderbilt | Best of N 模式、多分支平行開發 |
| Udemy Prototype to Prod | 「原型之後的 90%」理念 |
| CC for PMs | 用 Skill 規範 AI 的工作流程 |
| claude-code-ultimate-guide | 225 個生產模板的分類方式 |
| 用戶提供的工作坊大綱 | CLAUDE.md 紀律、Vibe Coding、測試 Skill、CI/CD、多 Agent、Code Review |

## 學到的設計原則

1. **交付物驅動**：每章結束時能「驗收」一個東西，比「學會一個概念」有效 10 倍
2. **Lab 是最小實戰單位**：在概念章節末尾加一個 10 分鐘的練習，成本低但效果好
3. **技術棧跳躍是好的教學工具**：從 HTML 跳到 Next.js 聽起來嚇人，但讓 AI 來寫的話，讀者反而能專注在「指揮 AI」而不是「學 React 語法」
