#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_guide_html.py
將 Claude Code 學習指南 Markdown 轉換為精美 HTML 文件網站。
Design: Swiss Minimalism + Noto Serif TC/Noto Sans TC + Indigo palette
"""

import re, json
import html as H

INPUT  = 'Claude-Code-學習指南-從入門到精通.md'
OUTPUT = 'Claude-Code-學習指南-從入門到精通.html'

CN = {'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'十':10,
      '十一':11,'十二':12,'十三':13,'十四':14,'十五':15,'十六':16,'十七':17,
      '十八':18,'十九':19,'二十':20,'二十一':21,'二十二':22,'二十三':23,
      '二十四':24,'二十五':25,'二十六':26,'二十七':27,'二十八':28,'二十九':29,
      '三十':30,'三十一':31,'三十二':32,'三十三':33,'三十四':34}

# ═══════════════════════════════════════
# Markdown Parser
# ═══════════════════════════════════════

class Parser:
    def __init__(self):
        self.hid = 0
        self.headings = []

    def convert(self, md):
        lines = md.replace('\r\n','\n').split('\n')
        out, i, n = [], 0, len(lines)
        while i < n:
            line = lines[i]
            if not line.strip():
                i += 1; continue

            # Code block
            if line.strip().startswith('```'):
                lang = line.strip()[3:].strip()
                i += 1; code = []
                while i < n and not lines[i].strip().startswith('```'):
                    code.append(lines[i]); i += 1
                if i < n: i += 1
                # Mermaid diagrams: render as <pre class="mermaid"> (no escaping!)
                if lang == 'mermaid':
                    mermaid_src = '\n'.join(code).strip()
                    out.append(f'<div class="my-6 overflow-x-auto"><pre class="mermaid">\n{mermaid_src}\n</pre></div>')
                else:
                    out.append(self._code(code, lang))
                continue

            # Heading
            hm = re.match(r'^(#{1,6})\s+(.+)$', line)
            if hm:
                out.append(self._heading(len(hm[1]), hm[2])); i += 1; continue

            # HR
            if line.strip() in ('---','***','___'):
                out.append('<hr class="my-12 border-0 h-px bg-gradient-to-r from-transparent via-slate-300 dark:via-slate-700 to-transparent">'); i += 1; continue

            # Table
            if '|' in line and i+1 < n and re.match(r'^\s*\|[\s\-:|]+\|\s*$', lines[i+1]):
                i, t = self._table(lines, i, n); out.append(t); continue

            # Blockquote
            if line.startswith('>'):
                i, bq = self._bquote(lines, i, n); out.append(bq); continue

            # Unordered list
            if re.match(r'^[\-\*]\s', line):
                i, ul = self._ulist(lines, i, n); out.append(ul); continue

            # Ordered list
            if re.match(r'^\d+\.\s', line):
                i, ol = self._olist(lines, i, n); out.append(ol); continue

            # Paragraph
            i, p = self._para(lines, i, n); out.append(p)

        return '\n'.join(out)

    def _heading(self, lv, text):
        self.hid += 1
        hid = f's{self.hid}'
        txt = self._inline(text)
        raw = re.sub(r'<[^>]+>', '', txt)
        self.headings.append({'id': hid, 'level': lv, 'text': raw})
        css = {
            1: 'text-4xl md:text-5xl font-black mt-8 mb-6 font-display text-indigo-950 dark:text-indigo-200 leading-tight',
            2: 'chapter-heading group text-2xl md:text-3xl font-bold mt-20 mb-6 pt-6 font-display text-indigo-900 dark:text-indigo-300 scroll-mt-24 leading-snug',
            3: 'text-xl md:text-2xl font-semibold mt-12 mb-4 text-slate-900 dark:text-white scroll-mt-24',
            4: 'text-lg md:text-xl font-semibold mt-8 mb-3 text-slate-800 dark:text-slate-100 scroll-mt-24',
            5: 'text-base font-semibold mt-6 mb-2 text-slate-700 dark:text-slate-200 scroll-mt-24',
        }.get(lv, 'text-base font-semibold mt-4 mb-2 scroll-mt-20')
        return f'<h{lv} id="{hid}" class="{css}">{txt}</h{lv}>'

    def _code(self, code_lines, lang):
        escaped = H.escape('\n'.join(code_lines))
        label = H.escape(lang) if lang else 'code'
        return (f'<div class="group relative my-6 rounded-xl overflow-hidden ring-1 ring-slate-900/10 dark:ring-white/10">'
                f'<div class="flex items-center justify-between px-4 py-2 bg-slate-800 text-xs text-slate-400">'
                f'<span class="font-mono">{label}</span>'
                f'<button onclick="copyCode(this)" class="opacity-0 group-hover:opacity-100 hover:text-white transition-all text-xs cursor-pointer">複製</button></div>'
                f'<pre class="p-4 bg-[#0d1117] overflow-x-auto text-sm leading-relaxed"><code class="text-slate-300 font-mono">{escaped}</code></pre></div>')

    def _split_row(self, line):
        """拆表格欄位，保留空格子。"""
        cells = line.split('|')
        # 去頭尾（ |col1|col2| 拆開後首尾是空字串）
        if cells and not cells[0].strip(): cells = cells[1:]
        if cells and not cells[-1].strip(): cells = cells[:-1]
        return [c.strip() for c in cells]

    def _table(self, lines, i, n):
        hdr = self._split_row(lines[i])
        i += 2
        rows = []
        while i < n and lines[i].strip().startswith('|'):
            row = self._split_row(lines[i])
            # 補齊欄數（避免少欄時錯位）
            while len(row) < len(hdr): row.append('')
            rows.append(row); i += 1
        th = ''.join(f'<th class="px-4 py-3 text-left text-xs font-bold uppercase tracking-wider text-indigo-700 dark:text-indigo-300">{self._inline(c)}</th>' for c in hdr)
        trs = ''.join(
            '<tr class="border-t border-slate-100 dark:border-slate-800 hover:bg-slate-50/50 dark:hover:bg-slate-800/30 transition-colors">'
            + ''.join(f'<td class="px-4 py-3 text-sm">{self._inline(c)}</td>' for c in r) + '</tr>' for r in rows)
        return i, (f'<div class="my-6 overflow-x-auto rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">'
                   f'<table class="w-full text-slate-700 dark:text-slate-300"><thead class="bg-indigo-50/80 dark:bg-indigo-950/30"><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>')

    def _bquote(self, lines, i, n):
        ql = []
        while i < n:
            line = lines[i]
            if line.startswith('> '): ql.append(line[2:])
            elif line.strip() == '>': ql.append('')
            elif line.startswith('>'): ql.append(line[1:])
            else: break
            i += 1
        content = '<br>'.join(self._inline(l) if l else '<br>' for l in ql)
        return i, f'<blockquote class="my-6 pl-5 border-l-4 border-indigo-400 dark:border-indigo-500 bg-indigo-50/50 dark:bg-indigo-950/20 py-4 pr-5 rounded-r-lg leading-7">{content}</blockquote>'

    def _ulist(self, lines, i, n):
        items = []
        while i < n and re.match(r'^[\-\*]\s', lines[i]):
            items.append(f'<li>{self._inline(re.sub(r"^[\\-\\*]\\s+", "", lines[i]))}</li>'); i += 1
        return i, f'<ul class="my-4 ml-6 list-disc space-y-1.5 text-slate-700 dark:text-slate-300 marker:text-indigo-400">{"".join(items)}</ul>'

    def _olist(self, lines, i, n):
        items = []
        while i < n and re.match(r'^\d+\.\s', lines[i]):
            items.append(f'<li>{self._inline(re.sub(r"^\\d+\\.\\s+", "", lines[i]))}</li>'); i += 1
        return i, f'<ol class="my-4 ml-6 list-decimal space-y-1.5 text-slate-700 dark:text-slate-300 marker:text-indigo-500">{"".join(items)}</ol>'

    def _para(self, lines, i, n):
        pl = []
        while i < n:
            line = lines[i]
            if not line.strip(): break
            if line.strip() in ('---','***','___'): break
            if re.match(r'^#{1,6}\s', line): break
            if line.strip().startswith('```'): break
            if line.startswith('>'): break
            if re.match(r'^[\-\*]\s', line): break
            if re.match(r'^\d+\.\s', line): break
            if '|' in line and i+1 < n and re.match(r'^\s*\|[\s\-:|]+\|\s*$', lines[i+1]): break
            pl.append(line); i += 1
        parts = []
        for j, line in enumerate(pl):
            raw = line.rstrip('\r\n')       # keep trailing spaces
            has_br = raw.endswith('  ')      # detect markdown line break
            s = raw.rstrip()                 # now strip spaces
            if has_br:
                parts.append(s + '<br>')
            elif j < len(pl) - 1:
                parts.append(s + ' ')
            else:
                parts.append(s)
        return i, f'<p class="my-3 leading-7 text-slate-700 dark:text-slate-300">{"".join(self._inline(p) for p in ["".join(parts)])}</p>'

    def _inline(self, text):
        if not text: return ''
        parts = re.split(r'(`[^`]+?`)', text)
        out = []
        for p in parts:
            if p.startswith('`') and p.endswith('`') and len(p) > 2:
                out.append(f'<code class="px-1.5 py-0.5 bg-slate-100 dark:bg-slate-800 rounded text-[0.9em] text-indigo-600 dark:text-indigo-400 font-mono">{H.escape(p[1:-1])}</code>')
            else:
                p = re.sub(r'\*\*(.+?)\*\*', r'<strong class="font-semibold text-slate-900 dark:text-white">\1</strong>', p)
                p = re.sub(r'\[(.+?)\]\((.+?)\)', lambda m: f'<a href="{H.escape(m[2])}" class="text-indigo-600 dark:text-indigo-400 hover:underline underline-offset-2" target="_blank" rel="noopener">{m[1]}</a>', p)
                out.append(p)
        return ''.join(out)


# ═══════════════════════════════════════
# Navigation Builder
# ═══════════════════════════════════════

def nav_label(text):
    m = re.match(r'第(.+?)章[：:](.+)', text)
    if m:
        num = CN.get(m[1], m[1])
        title = re.split(r'\s*[—\-]\s*', m[2].strip())[0]
        return str(num), title
    return None, text[:35] + ('…' if len(text) > 35 else '')

def build_nav(headings):
    nav = []
    in_group = False
    h3buf = []

    def flush_h3():
        if h3buf:
            nav.append('<div class="nav-sub hidden ml-4 mt-1 space-y-0.5 border-l-2 border-slate-200 dark:border-slate-700 pl-3">')
            nav.extend(h3buf)
            nav.append('</div>')
            h3buf.clear()

    for h in headings:
        if h['level'] == 2:
            flush_h3()
            if in_group: nav.append('</div>')
            num, title = nav_label(h['text'])
            badge = f'<span class="w-6 h-6 flex items-center justify-center rounded-full bg-indigo-100 dark:bg-indigo-900/40 text-indigo-600 dark:text-indigo-400 text-[10px] font-bold shrink-0">{num}</span>' if num else '<span class="w-6 h-6 flex items-center justify-center rounded-full bg-slate-200 dark:bg-slate-700 text-slate-500 dark:text-slate-400 text-[10px] shrink-0">+</span>'
            nav.append(f'<div class="nav-group">')
            nav.append(f'<a href="#{h["id"]}" class="nav-item flex items-center gap-2.5 px-3 py-2 rounded-lg text-[13px] text-slate-600 dark:text-slate-400 hover:bg-indigo-50 dark:hover:bg-indigo-950/30 hover:text-indigo-700 dark:hover:text-indigo-300 transition-all cursor-pointer" data-id="{h["id"]}">{badge}<span class="truncate">{H.escape(title)}</span></a>')
            in_group = True
        elif h['level'] == 3 and in_group:
            short = h['text'][:30] + ('…' if len(h['text']) > 30 else '')
            h3buf.append(f'<a href="#{h["id"]}" class="nav-sub-item block px-2 py-1 rounded text-xs text-slate-500 dark:text-slate-500 hover:text-indigo-600 dark:hover:text-indigo-400 hover:bg-indigo-50/50 dark:hover:bg-indigo-950/20 transition-all truncate cursor-pointer" data-id="{h["id"]}">{H.escape(short)}</a>')

    flush_h3()
    if in_group: nav.append('</div>')
    return '\n'.join(nav)


# ═══════════════════════════════════════
# HTML Assembly
# ═══════════════════════════════════════

HEAD = '''<!DOCTYPE html>
<html lang="zh-Hant" class="scroll-smooth">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Claude Code 完全學習指南：從入門到精通</title>
<meta name="description" content="Claude Code 完全學習指南 — 34 章 + 85 個實戰案例，從零開始學會 AI 輔助開發。">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700;900&family=Noto+Serif+TC:wght@700;900&family=JetBrains+Mono:wght@400;500&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script>
<script>
tailwind.config={darkMode:'class',theme:{extend:{fontFamily:{
display:['"Noto Serif TC"','serif'],
heading:['"Plus Jakarta Sans"','"Noto Sans TC"','sans-serif'],
body:['"Noto Sans TC"','sans-serif'],
mono:['"JetBrains Mono"','monospace']
}}}}
</script>
<style>
body{font-family:'Noto Sans TC',sans-serif}
h1,h2{font-family:'Noto Serif TC',serif}
h3,h4,h5,h6{font-family:'Plus Jakarta Sans','Noto Sans TC',sans-serif}
code,pre{font-family:'JetBrains Mono',monospace}
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:#94A3B8;border-radius:9px}
.dark ::-webkit-scrollbar-thumb{background:#475569}
.nav-item.active{background:#EEF2FF;color:#4338CA;font-weight:600}
.dark .nav-item.active{background:rgba(99,102,241,.12);color:#A5B4FC}
.nav-sub-item.active{color:#4F46E5;font-weight:500}
.dark .nav-sub-item.active{color:#818CF8}
::selection{background:#C7D2FE;color:#312E81}
.dark ::selection{background:#3730A3;color:#E0E7FF}
@media print{#sidebar,#header,#progress,#back-top,#overlay{display:none!important}main{margin-left:0!important}}
</style>
</head>
<body class="bg-[#FAFBFF] dark:bg-slate-950 text-slate-800 dark:text-slate-200 font-body antialiased">
<div id="progress" class="fixed top-0 left-0 h-[3px] bg-gradient-to-r from-indigo-600 via-indigo-400 to-emerald-400 z-[100] transition-[width] duration-100" style="width:0%"></div>

<header id="header" class="fixed top-0 left-0 right-0 h-14 bg-white/90 dark:bg-slate-900/90 backdrop-blur-xl border-b border-slate-200/80 dark:border-slate-800/80 z-50 flex items-center px-4 gap-3">
<button id="menu-btn" class="lg:hidden p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors cursor-pointer" aria-label="Menu">
<svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" d="M4 6h16M4 12h16M4 18h16"/></svg></button>
<a href="#" class="font-display text-lg font-bold text-indigo-700 dark:text-indigo-400 truncate">Claude Code 學習指南</a>
<div class="flex-1"></div>
<button id="theme-btn" class="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors cursor-pointer" aria-label="Theme">
<svg class="w-5 h-5 dark:hidden" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/></svg>
<svg class="w-5 h-5 hidden dark:block" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/></svg>
</button></header>
'''

CHAPTER_BAR = '''<div id="chapter-bar" class="fixed top-14 left-0 right-0 h-10 bg-indigo-50/95 dark:bg-indigo-950/80 backdrop-blur-sm border-b border-indigo-100 dark:border-indigo-900/50 z-[45] flex items-center px-4 lg:pl-[19rem] transition-all duration-300 opacity-0 -translate-y-2" style="pointer-events:none">
<span id="chapter-label" class="text-sm font-semibold text-indigo-700 dark:text-indigo-300 truncate font-heading"></span>
</div>
'''

SIDEBAR_START = '''<aside id="sidebar" class="fixed top-14 left-0 bottom-0 w-72 bg-white/95 dark:bg-slate-900/95 backdrop-blur-sm border-r border-slate-200/80 dark:border-slate-800/80 z-40 overflow-y-auto transform -translate-x-full lg:translate-x-0 transition-transform duration-300">
<div class="p-3 space-y-0.5">
'''

SIDEBAR_END = '''</div></aside>
<div id="overlay" class="fixed inset-0 bg-black/40 z-30 hidden lg:hidden"></div>
'''

MAIN_START = '''<main class="lg:ml-72 pt-14 min-h-screen">
<div class="max-w-3xl mx-auto px-5 sm:px-8 py-10" id="content">
'''

MAIN_END = '''</div></main>
'''

SEARCH_MODAL = ''


BACK_TOP = '''<button id="back-top" class="fixed bottom-6 right-6 p-3 bg-indigo-600 hover:bg-indigo-700 text-white rounded-full shadow-lg shadow-indigo-600/20 opacity-0 translate-y-4 transition-all duration-300 z-40 cursor-pointer" aria-label="Back to top">
<svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" d="M5 10l7-7m0 0l7 7m-7-7v18"/></svg></button>
'''

def script_block():
    return '''<script>
const html=document.documentElement;
if(localStorage.theme==='dark'||(!localStorage.theme&&matchMedia('(prefers-color-scheme:dark)').matches))html.classList.add('dark');
document.getElementById('theme-btn').onclick=()=>{html.classList.toggle('dark');localStorage.theme=html.classList.contains('dark')?'dark':'light'};

function toggleSB(){
  const sb=document.getElementById('sidebar'),ov=document.getElementById('overlay');
  const closed=sb.classList.contains('-translate-x-full');
  sb.classList.toggle('-translate-x-full',!closed);
  sb.classList.toggle('translate-x-0',closed);
  ov.classList.toggle('hidden',!closed);
}
document.getElementById('menu-btn').onclick=toggleSB;
document.getElementById('overlay').onclick=toggleSB;

document.querySelectorAll('.nav-item').forEach(a=>{
  a.addEventListener('click',function(){
    const sub=this.parentElement.querySelector('.nav-sub');
    if(sub){document.querySelectorAll('.nav-sub').forEach(s=>{if(s!==sub)s.classList.add('hidden')});sub.classList.toggle('hidden')}
    if(innerWidth<1024)toggleSB();
  });
});
document.querySelectorAll('.nav-sub-item').forEach(a=>{
  a.addEventListener('click',()=>{if(innerWidth<1024)toggleSB()});
});

const secs=document.querySelectorAll('[id^="s"]');
const navs=document.querySelectorAll('.nav-item,.nav-sub-item');
const chHeadings=document.querySelectorAll('.chapter-heading');
const chBar=document.getElementById('chapter-bar');
const chLabel=document.getElementById('chapter-label');
let tick=false,lastCh='';
function onScroll(){
  if(tick)return;tick=true;
  requestAnimationFrame(()=>{
    const y=scrollY,total=document.documentElement.scrollHeight-innerHeight;
    document.getElementById('progress').style.width=(total>0?(y/total)*100:0)+'%';
    const btn=document.getElementById('back-top');
    if(y>500){btn.style.opacity='1';btn.style.transform='translateY(0)'}
    else{btn.style.opacity='0';btn.style.transform='translateY(1rem)'}

    // Chapter bar
    let curCh='';
    chHeadings.forEach(h=>{if(h.getBoundingClientRect().top<=130)curCh=h.textContent.trim()});
    if(curCh&&y>300){
      if(curCh!==lastCh){chLabel.textContent=curCh;lastCh=curCh}
      chBar.style.opacity='1';chBar.style.transform='translateY(0)';chBar.style.pointerEvents='auto';
    }else{
      chBar.style.opacity='0';chBar.style.transform='translateY(-0.5rem)';chBar.style.pointerEvents='none';
    }

    // Active nav
    let cur='';
    secs.forEach(s=>{if(s.getBoundingClientRect().top<=130)cur=s.id});
    navs.forEach(a=>{
      const active=a.dataset.id===cur;
      a.classList.toggle('active',active);
      if(active){
        const sub=a.closest('.nav-sub');
        if(sub)sub.classList.remove('hidden');
        if(a.classList.contains('nav-item')){
          const s2=a.parentElement.querySelector('.nav-sub');
          if(s2)s2.classList.remove('hidden');
        }
        a.scrollIntoView&&a.scrollIntoView({block:'nearest',behavior:'auto'});
      }
    });
    tick=false;
  });
}
addEventListener('scroll',onScroll,{passive:true});

function copyCode(btn){
  const code=btn.closest('.group').querySelector('code').textContent;
  navigator.clipboard.writeText(code).then(()=>{btn.textContent='已複製!';setTimeout(()=>btn.textContent='複製',2e3)});
}
document.getElementById('back-top').onclick=()=>scrollTo({top:0,behavior:'smooth'});
onScroll();
</script>
<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
mermaid.initialize({startOnLoad:true,theme:'base',
securityLevel:'loose',
themeVariables:{
primaryColor:'#e0e7ff',primaryTextColor:'#1e1b4b',primaryBorderColor:'#4f46e5',
lineColor:'#6366f1',secondaryColor:'#f1f5f9',tertiaryColor:'#faf5ff',
fontFamily:'"Noto Sans TC",sans-serif',fontSize:'18px'},
flowchart:{useMaxWidth:true,htmlLabels:true,curve:'basis',padding:15},
sequence:{useMaxWidth:true,actorFontSize:16,messageFontSize:15,width:180},
timeline:{fontSize:24,sectionFontSize:28,useMaxWidth:true}});
</script>
</body></html>'''


# ═══════════════════════════════════════
# Main
# ═══════════════════════════════════════

def main():
    print('Reading markdown...')
    with open(INPUT, 'r', encoding='utf-8') as f:
        md = f.read()

    print('Converting to HTML...')
    parser = Parser()
    content = parser.convert(md)
    print(f'  {len(parser.headings)} headings parsed')

    nav_html = build_nav(parser.headings)

    print('Assembling HTML...')
    html = HEAD + CHAPTER_BAR + SIDEBAR_START + nav_html + SIDEBAR_END + MAIN_START + content + MAIN_END + BACK_TOP + script_block()

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(html)

    kb = len(html.encode('utf-8')) / 1024
    print(f'Done => {OUTPUT} ({kb:.0f} KB)')

if __name__ == '__main__':
    main()
