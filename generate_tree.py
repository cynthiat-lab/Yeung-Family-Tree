"""
generate_tree.py
Reads the latest CSV from data/ to get the data date,
then generates index.html with the full hand-structured family tree,
and saves a dated version to versions/.

The HTML structure is hand-crafted to match the canonical tree layout.
To update the tree content, edit the BODY constant below and commit.
The script handles: date stamping, file writing, and version archiving.
"""

import csv
import glob
import os
import re
from datetime import date

# ── Find the most recently modified CSV in data/ ──────────────────────────────
csv_files = sorted(glob.glob("data/*.csv"), key=os.path.getmtime, reverse=True)
if not csv_files:
    raise FileNotFoundError("No CSV files found in data/")

csv_path = csv_files[0]
csv_filename = os.path.basename(csv_path)

# Parse data date from filename if it contains a date, otherwise use file mtime
date_match = re.search(r'(\d{1,2})-(\d{1,2})-(\d{2,4})', csv_filename)
if date_match:
    m, d, y = date_match.groups()
    y = int(y) + 2000 if len(y) == 2 else int(y)
    try:
        from datetime import datetime
        data_date = datetime(y, int(m), int(d)).strftime("%B %-d, %Y")
    except Exception:
        data_date = date.fromtimestamp(os.path.getmtime(csv_path)).strftime("%B %-d, %Y")
else:
    data_date = date.fromtimestamp(os.path.getmtime(csv_path)).strftime("%B %-d, %Y")

print(f"Using: {csv_path} — data date: {data_date}")

# ── CSS ───────────────────────────────────────────────────────────────────────
CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: Georgia, 'Times New Roman', serif; background: #f7f5f0; color: #222; padding: 24px 16px; }
h1 { text-align: center; font-size: 22px; font-weight: 400; color: #2a2520; margin-bottom: 4px; letter-spacing: 0.02em; }
.subtitle { text-align: center; font-size: 13px; color: #999; margin-bottom: 10px; font-style: italic; }
.datestamp-wrap { text-align: center; margin-bottom: 20px; }
.datestamp { display: inline-block; font-size: 12px; color: #aaa; background: #fff; padding: 5px 14px; border-radius: 20px; border: 0.5px solid #e0ddd5; letter-spacing: 0.02em; }
.legend { display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; margin-bottom: 24px; }
.legend-item { display: flex; align-items: center; gap: 6px; font-size: 11px; color: #777; }
.legend-dot { width: 10px; height: 10px; border-radius: 2px; flex-shrink: 0; }
.section { background: #fff; border-radius: 12px; border: 0.5px solid #e0ddd5; padding: 20px 16px; margin-bottom: 18px; }
.section-title { font-size: 11px; font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase; color: #aaa; margin-bottom: 14px; padding-bottom: 8px; border-bottom: 0.5px solid #ece9e2; }
.subsection { margin-top: 16px; padding-top: 14px; border-top: 0.5px dashed #e5e2db; }
.subsection-title { font-size: 10px; font-weight: 500; letter-spacing: 0.06em; text-transform: uppercase; color: #bbb; margin-bottom: 10px; }
.gen-row { display: flex; flex-wrap: wrap; justify-content: center; gap: 9px; margin-bottom: 8px; }
.gen-label { font-size: 10px; color: #ccc; text-align: center; letter-spacing: 0.04em; margin: 4px 0 8px; }
.card { width: 118px; background: #fff; border: 0.5px solid #ccc; border-radius: 8px; padding: 7px 8px 8px; text-align: center; flex-shrink: 0; }
.card.yang { border-top: 2.5px solid #4A7FBB; }
.card.in-law { border-top: 2.5px solid #7BAF8E; }
.card.deceased { opacity: 0.65; }
.card.deceased .card-name::before { content: "† "; color: #999; font-weight: 400; }
.card-name { font-size: 11.5px; font-weight: 500; color: #1a1a1a; line-height: 1.3; }
.card-year { font-size: 10px; color: #aaa; margin-top: 2px; line-height: 1.3; }
.card-note { font-size: 9.5px; color: #999; margin-top: 2px; font-style: italic; line-height: 1.25; }
.card-alias { font-size: 9.5px; color: #bbb; margin-top: 2px; line-height: 1.3; }
.couple { display: flex; align-items: flex-start; gap: 4px; }
.sx { font-size: 11px; color: #ccc; padding-top: 14px; flex-shrink: 0; line-height: 1; }
.arr { text-align: center; font-size: 11px; color: #ccc; margin: 3px 0 4px; }
.tree-footer { font-size: 10px; color: #ccc; text-align: center; margin-top: 6px; line-height: 1.9; font-style: italic; }
"""

# ── BODY HTML — edit this section to update tree content ─────────────────────
# This is the canonical hand-structured tree. Update when new CSV data arrives.
BODY = """
<!-- ANCESTORS -->
<div class="section">
  <div class="section-title">Ancestors — Generations 0 &amp; 1</div>
  <div class="gen-label">Generation 0</div>
  <div class="gen-row">
    <div class="couple">
      <div class="card yang deceased"><div class="card-name">楊鳳旌</div><div class="card-year">b. 1800 · d. 1874</div></div>
      <div class="sx">×</div>
      <div class="card in-law deceased"><div class="card-name">廖氏</div><div class="card-year">b. 1803 · d. 1844</div></div>
    </div>
  </div>
  <div class="arr">↓</div>
  <div class="gen-label">Generation 1</div>
  <div class="gen-row">
    <div class="couple">
      <div class="card yang deceased"><div class="card-name">楊奕祥</div><div class="card-year">b. 1850 · d. 1930</div></div>
      <div class="sx">×</div>
      <div class="card in-law deceased"><div class="card-name">鍾氏</div><div class="card-year">b. 1851 · d. 1919</div></div>
    </div>
  </div>
  <div class="arr">↓ Generation 2 children</div>
  <div class="gen-row">
    <div class="card yang deceased"><div class="card-name">楊煒廷</div><div class="card-year">b. 1882 · d. 1962</div><div class="card-note">→ two families below</div></div>
    <div class="card yang deceased"><div class="card-name">楊尊三</div><div class="card-year">b. 1892 · d. 1945</div><div class="card-note">→ five children below</div></div>
    <div class="card yang deceased"><div class="card-name">楊用好</div><div class="card-note">適陳氏</div></div>
    <div class="card yang deceased"><div class="card-name">楊先行</div><div class="card-note">適黃氏</div></div>
    <div class="card yang deceased"><div class="card-name">楊尋</div><div class="card-note">適李氏</div></div>
  </div>
</div>


<!-- 楊煒廷 × 黃惠蘭 -->
<div class="section">
  <div class="section-title">楊煒廷 × 黃惠蘭 — First Family</div>
  <div class="gen-row">
    <div class="couple">
      <div class="card yang deceased"><div class="card-name">楊煒廷</div><div class="card-year">b. 1882 · d. 1962</div></div>
      <div class="sx">×</div>
      <div class="card in-law deceased"><div class="card-name">黃惠蘭</div><div class="card-alias">aka 黃才喜</div><div class="card-year">b. 1883 · d. 1918</div></div>
    </div>
  </div>
  <div class="arr">↓ Generation 3 children</div>
  <div class="gen-row">
    <div class="card yang deceased"><div class="card-name">楊伯章</div><div class="card-alias">楊育之</div><div class="card-year">d. 1959</div><div class="card-note">2 wives · see below</div></div>
    <div class="card yang deceased"><div class="card-name">楊伯贊</div><div class="card-year">b. 1903</div><div class="card-note">2 wives · see below</div></div>
    <div class="card yang deceased"><div class="card-name">楊英鰲</div><div class="card-alias">楊鰲</div><div class="card-year">b. 1913 · d. 1993</div><div class="card-note">× 馬靜如 · see below</div></div>
    <div class="card yang deceased"><div class="card-name">楊秀貞</div><div class="card-alias">Jean Wong</div><div class="card-note">× 黃存欽 · see below</div></div>
    <div class="card yang deceased"><div class="card-name">楊玉容</div><div class="card-year">b. 1915</div><div class="card-note">× 李沃芬 · see below</div></div>
  </div>

  <!-- 楊英鰲 -->
  <div class="subsection">
    <div class="subsection-title">楊英鰲's Family</div>
    <div class="gen-row">
      <div class="couple">
        <div class="card yang deceased"><div class="card-name">楊英鰲</div><div class="card-year">b. 1913 · d. 1993</div></div>
        <div class="sx">×</div>
        <div class="card in-law deceased"><div class="card-name">馬靜如</div><div class="card-year">b. 1918 · d. 2014</div></div>
      </div>
    </div>
    <div class="arr">↓ Generation 4 children</div>
    <div class="gen-row">
      <div class="card yang"><div class="card-name">楊碧玹</div><div class="card-alias">Rachel Courchesne</div><div class="card-year">b. 1941 · San Diego</div><div class="card-note">× Eric Courchesne (div.)</div></div>
      <div class="card yang"><div class="card-name">楊碧琳</div><div class="card-year">b. 1944 · Seattle</div><div class="card-note">× 利忠能</div></div>
      <div class="card yang"><div class="card-name">楊碧瓘</div><div class="card-alias">Bik Tye</div><div class="card-year">b. 1947 · Seattle</div><div class="card-note">× 戴自海 (Henry Tye)</div></div>
      <div class="card yang deceased"><div class="card-name">楊祖由</div><div class="card-year">b. 1948 · d. 2023</div><div class="card-note">× Chefin Bobonis</div></div>
      <div class="card yang deceased"><div class="card-name">楊碧瓖</div><div class="card-year">b. 1949 · d. 2023</div><div class="card-note">× Nagi Awas</div></div>
    </div>
    <div class="gen-label" style="margin-top:10px;">楊碧玹 → Gen 5</div>
    <div class="gen-row">
      <div class="card yang"><div class="card-name">楊奇葩</div><div class="card-alias">Khyber Courchesne</div><div class="card-year">b. 1974 · San Diego</div><div class="card-note">× Katrin Jogi (div.) → Maasika</div></div>
    </div>
    <div class="gen-label" style="margin-top:8px;">楊碧琳 × 利忠能 → Gen 5</div>
    <div class="gen-row">
      <div class="card yang"><div class="card-name">利思維</div><div class="card-year">b. 1969 · Seattle</div><div class="card-note">× 鄭溫薇</div></div>
      <div class="card yang"><div class="card-name">利思欣</div><div class="card-year">b. 1972 · Antwerp</div><div class="card-note">× Rajmund Glowczinski</div></div>
    </div>
    <div class="gen-label">Gen 6</div>
    <div class="gen-row">
      <div class="card yang"><div class="card-name">利樂真</div><div class="card-year">b. 2004</div></div>
      <div class="card yang"><div class="card-name">利樂中</div><div class="card-year">b. 2006</div></div>
      <div class="card yang"><div class="card-name">高靜慧</div><div class="card-alias">Sofie Glow</div><div class="card-year">b. 2006</div></div>
      <div class="card yang"><div class="card-name">高靖博</div><div class="card-alias">Tibo Glow</div><div class="card-year">b. 2008</div></div>
    </div>
    <div class="gen-label" style="margin-top:8px;">楊碧瓘 × 戴自海 → Gen 5</div>
    <div class="gen-row">
      <div class="card yang"><div class="card-name">戴琦</div><div class="card-alias">Kay Tye</div><div class="card-year">b. 1981 · San Diego</div><div class="card-note">× James Wagner (div.)</div></div>
      <div class="card yang"><div class="card-name">戴琳</div><div class="card-alias">Lynne Tye</div><div class="card-year">b. 1988 · Seattle</div><div class="card-note">× 葉冠廷</div></div>
    </div>
    <div class="gen-label">Gen 6</div>
    <div class="gen-row">
      <div class="card yang"><div class="card-name">戴奇華</div><div class="card-alias">Keeva Tye-Wagner</div></div>
      <div class="card yang"><div class="card-name">戴傑華</div><div class="card-alias">Jet Tye-Wagner</div></div>
      <div class="card yang"><div class="card-name">葉靜</div><div class="card-alias">Illumi</div></div>
      <div class="card yang"><div class="card-name">葉君安</div><div class="card-alias">Revel</div></div>
      <div class="card yang"><div class="card-name">葉留餘</div><div class="card-alias">Ten</div></div>
    </div>
    <div class="gen-label" style="margin-top:8px;">楊碧瓖 × Nagi Awas → Gen 5</div>
    <div class="gen-row">
      <div class="card in-law"><div class="card-name">Darek Awas</div><div class="card-year">b. 1981 · E. Brunswick NJ</div><div class="card-note">× Alina Kozlova</div></div>
    </div>
    <div class="gen-label">Gen 6 — Darek's children</div>
    <div class="gen-row">
      <div class="card in-law"><div class="card-name">Marshall Awas</div></div>
      <div class="card in-law"><div class="card-name">Afina Awas</div></div>
      <div class="card in-law"><div class="card-name">Anderson Awas</div></div>
    </div>
  </div>

  <!-- 楊秀貞 -->
  <div class="subsection">
    <div class="subsection-title">楊秀貞's Family (Jean Wong)</div>
    <div class="gen-row">
      <div class="couple">
        <div class="card yang deceased"><div class="card-name">楊秀貞</div><div class="card-alias">Jean Wong</div></div>
        <div class="sx">×</div>
        <div class="card in-law deceased"><div class="card-name">黃存欽</div></div>
      </div>
    </div>
    <div class="arr">↓ Generation 4 children</div>
    <div class="gen-row">
      <div class="card yang deceased"><div class="card-name">黃海棠</div><div class="card-alias">Nora</div><div class="card-year">b. 1927</div><div class="card-note">× 黃永琪 → Edwin, Chichi, Karen</div></div>
      <div class="card yang deceased"><div class="card-name">黃啟光</div><div class="card-alias">Alan</div><div class="card-year">b. 1930</div><div class="card-note">× Maria So → Amy, Serina</div></div>
      <div class="card yang deceased"><div class="card-name">黃啟祥</div><div class="card-alias">Roger</div><div class="card-year">b. 1931</div><div class="card-note">× Evelyn Chan → Derek, Julie, Terry</div></div>
      <div class="card yang deceased"><div class="card-name">黃啟昌</div><div class="card-alias">Casey</div><div class="card-year">b. 1934 · d. 1992</div><div class="card-note">× Ping (Woo) → Brenda, Andy, Pamala, Jason</div></div>
      <div class="card yang"><div class="card-name">黃海珊</div><div class="card-alias">Susan Chan</div><div class="card-year">b. 1936 · Oakland CA</div><div class="card-note">× Tim Chan</div></div>
      <div class="card yang"><div class="card-name">黃啟信</div><div class="card-alias">Carson</div><div class="card-year">b. 1938 · Jerome ID</div><div class="card-note">× Ronda (div.) · × Sue Miller</div></div>
    </div>
    <div class="gen-label" style="margin-top:8px;">黃海珊 (Susan Chan) × Tim Chan → Gen 5</div>
    <div class="gen-row">
      <div class="card yang"><div class="card-name">Bill Chan</div><div class="card-year">Denville CA</div><div class="card-note">× Michelle → Stephen, Brian, Heather, Jennifer</div></div>
      <div class="card yang"><div class="card-name">Wendy Chan</div><div class="card-year">Moraga CA</div><div class="card-note">× Neil → Tim</div></div>
    </div>
    <div class="gen-label" style="margin-top:6px;">黃海棠 (Nora) × 黃永琪 → Gen 5</div>
    <div class="gen-row">
      <div class="card in-law"><div class="card-name">黃頌尹</div><div class="card-alias">Edwin</div><div class="card-note">× Laura · San Jose CA</div></div>
      <div class="card in-law"><div class="card-name">頌慈</div><div class="card-alias">Chichi</div></div>
      <div class="card in-law"><div class="card-name">頌惠</div><div class="card-alias">Karen</div></div>
    </div>
    <div class="gen-label" style="margin-top:6px;">黃啟信 (Carson) → Gen 5</div>
    <div class="gen-row">
      <div class="card in-law"><div class="card-name">Jeff Wong</div></div>
      <div class="card in-law"><div class="card-name">Chris Wong</div></div>
    </div>
  </div>

  <!-- 楊伯章 -->
  <div class="subsection">
    <div class="subsection-title">楊伯章's Family (d. 1959 · two wives)</div>
    <div class="gen-label">Wife 1: 梁Pauline</div>
    <div class="gen-row">
      <div class="card yang"><div class="card-name">楊祖敏</div></div>
      <div class="card yang deceased"><div class="card-name">楊碧玫</div><div class="card-note">× Richard Wong → Irenie, Elisa</div></div>
      <div class="card yang deceased"><div class="card-name">楊碧瑤</div></div>
    </div>
    <div class="gen-label">Wife 2: 劉南絲</div>
    <div class="gen-row">
      <div class="card yang"><div class="card-name">楊祖建</div><div class="card-year">b. 1953</div></div>
    </div>
  </div>

  <!-- 楊伯贊 -->
  <div class="subsection">
    <div class="subsection-title">楊伯贊's Family (b. 1903 · two wives)</div>
    <div class="gen-label">Wife 1: 劉玉如 (1904–1932)</div>
    <div class="gen-row">
      <div class="card yang deceased"><div class="card-name">楊麗坤</div><div class="card-year">b. 1925 · d. 1935</div></div>
      <div class="card yang deceased"><div class="card-name">楊祖銘</div><div class="card-year">b. 1929 · d. 1992</div><div class="card-note">× Carlyn Hamaan (b. 1942)</div></div>
      <div class="card yang deceased"><div class="card-name">楊祖榆</div><div class="card-year">b. 1931</div><div class="card-note">→ 楊虹, 楊靖環 (Alison), 楊澤宇 (Jason)</div></div>
    </div>
    <div class="gen-label">楊靖環 (Alison) × Wong Chi-Chin (Renee) · Melbourne</div>
    <div class="gen-row">
      <div class="card yang"><div class="card-name">黃弘楓</div><div class="card-alias">Charlie</div></div>
      <div class="card yang"><div class="card-name">黃芝蕊</div><div class="card-alias">Ariana</div></div>
      <div class="card yang"><div class="card-name">黃芝婉</div><div class="card-alias">Emmeline</div></div>
      <div class="card yang"><div class="card-name">黃芝麗</div><div class="card-alias">Coralie</div></div>
    </div>
    <div class="gen-label">楊澤宇 (Jason) × 江賢金 (Kim) · Melbourne</div>
    <div class="gen-row">
      <div class="card yang"><div class="card-name">楊竣棋</div><div class="card-alias">Jacob</div></div>
      <div class="card yang"><div class="card-name">楊小瑩</div><div class="card-alias">Emily</div></div>
    </div>
    <div class="gen-label" style="margin-top:8px;">Wife 2: 陳潤桂 (1914–2014)</div>
    <div class="gen-row">
      <div class="card yang"><div class="card-name">楊碧琪</div><div class="card-year">b. 1948 · Washington DC</div><div class="card-note">× Xuyen Vuong (王青川) → 王青律, 王青綸, 王青彬</div></div>
      <div class="card yang"><div class="card-name">楊祖良</div><div class="card-year">b. 1951 · Toronto</div></div>
    </div>
  </div>

  <!-- 楊玉容 -->
  <div class="subsection">
    <div class="subsection-title">楊玉容's Family</div>
    <div class="gen-row">
      <div class="couple">
        <div class="card yang deceased"><div class="card-name">楊玉容</div><div class="card-year">b. 1915</div></div>
        <div class="sx">×</div>
        <div class="card in-law"><div class="card-name">李沃芬</div><div class="card-alias">Gilbert Lee</div></div>
      </div>
    </div>
    <div class="arr">↓</div>
    <div class="gen-row">
      <div class="card in-law deceased"><div class="card-name">李世侃</div><div class="card-alias">Anthony</div><div class="card-year">b. 1943 · d. 2020</div><div class="card-note">× 黃穗珠 (Grace, b. 1946)</div></div>
      <div class="card in-law"><div class="card-name">李世任</div><div class="card-alias">Sumner</div><div class="card-year">b. 1946 · Edmonton</div><div class="card-note">× Annie → Ivar, Samantha?</div></div>
      <div class="card in-law"><div class="card-name">李世儒</div><div class="card-alias">Winston</div><div class="card-year">b. 1949 · Isle of Wight UK</div><div class="card-note">→ Benjamin, Daniel, Mathew, Sebastian</div></div>
    </div>
  </div>
</div>


<!-- 楊煒廷 × 胡氏 -->
<div class="section">
  <div class="section-title">楊煒廷 × 胡氏 — Second Family</div>
  <div class="gen-row">
    <div class="couple">
      <div class="card yang deceased"><div class="card-name">楊煒廷</div><div class="card-year">b. 1882 · d. 1962</div></div>
      <div class="sx">×</div>
      <div class="card in-law deceased"><div class="card-name">胡氏</div><div class="card-year">b. 1904 · d. 1952</div></div>
    </div>
  </div>
  <div class="arr">↓ Generation 3 children</div>
  <div class="gen-row">
    <div class="card yang deceased"><div class="card-name">楊金愛</div><div class="card-note">× 鐘士豪 · see below</div></div>
    <div class="card yang deceased"><div class="card-name">楊伯駿</div><div class="card-year">b. 1932 · d. 2006</div><div class="card-note">× 鄧慧賢 · see below</div></div>
    <div class="card yang deceased"><div class="card-name">楊伯馴</div><div class="card-alias">Albert Young</div><div class="card-year">b. 1936 · d. 2025</div><div class="card-note">× 羅慧嘉 · see below</div></div>
    <div class="card yang"><div class="card-name">楊玉影</div><div class="card-year">b. 1938 · Hong Kong</div><div class="card-note">× 李志剛 · see below</div></div>
  </div>

  <!-- 楊金愛 -->
  <div class="subsection">
    <div class="subsection-title">楊金愛's Family</div>
    <div class="gen-row">
      <div class="couple">
        <div class="card yang deceased"><div class="card-name">楊金愛</div></div>
        <div class="sx">×</div>
        <div class="card in-law"><div class="card-name">鐘士豪</div></div>
      </div>
    </div>
    <div class="arr">↓ child</div>
    <div class="gen-row">
      <div class="couple">
        <div class="card in-law"><div class="card-name">鐘伊雲</div><div class="card-alias">Evelyn</div><div class="card-note">Toronto</div></div>
        <div class="sx">×</div>
        <div class="card in-law"><div class="card-name">鐘啟明</div><div class="card-alias">Andrew</div></div>
      </div>
    </div>
    <div class="gen-label">Gen 5</div>
    <div class="gen-row">
      <div class="card in-law"><div class="card-name">Cheryl 鐘</div></div>
    </div>
  </div>

  <!-- 楊伯駿 -->
  <div class="subsection">
    <div class="subsection-title">楊伯駿's Family · Media PA</div>
    <div class="gen-row">
      <div class="couple">
        <div class="card yang deceased"><div class="card-name">楊伯駿</div><div class="card-year">b. 1932 · d. 2006</div></div>
        <div class="sx">×</div>
        <div class="card in-law"><div class="card-name">鄧慧賢</div><div class="card-alias">Julianna</div><div class="card-year">b. 1937 · Media PA</div></div>
      </div>
    </div>
    <div class="arr">↓ Gen 4 children</div>
    <div class="gen-row">
      <div class="card yang"><div class="card-name">楊碧瑩</div><div class="card-alias">Doreen</div><div class="card-year">b. 1966</div><div class="card-note">× 屈振祥 (Trevor, b. 1963) → 屈穎琳 (Andrea, b. 2004)</div></div>
      <div class="card yang deceased"><div class="card-name">楊祖恩</div><div class="card-year">b. 1968 · d. 2023</div><div class="card-note">× 楊詠紅 (b. 1966)</div></div>
    </div>
  </div>

  <!-- 楊伯馴 -->
  <div class="subsection">
    <div class="subsection-title">楊伯馴's Family</div>
    <div class="gen-row">
      <div class="couple">
        <div class="card yang deceased"><div class="card-name">楊伯馴 (Albert)</div><div class="card-year">b. 1936 · d. 2025</div></div>
        <div class="sx">×</div>
        <div class="card in-law deceased"><div class="card-name">羅慧嘉 (Barbara)</div><div class="card-year">b. 1941 · d. 2019</div></div>
      </div>
    </div>
    <div class="arr">↓ Gen 4 child</div>
    <div class="gen-row">
      <div class="couple">
        <div class="card yang"><div class="card-name">楊祖能 (Jonas)</div><div class="card-year">b. 1971 · Vancouver</div></div>
        <div class="sx">×</div>
        <div class="card in-law"><div class="card-name">伍惠娟 (Sharon)</div><div class="card-year">b. 1970 · Vancouver</div></div>
      </div>
    </div>
    <div class="gen-label">Gen 5</div>
    <div class="gen-row">
      <div class="card yang"><div class="card-name">楊靖婷</div><div class="card-alias">Laura Stella Young</div><div class="card-year">b. 2019 · Vancouver</div></div>
    </div>
  </div>

  <!-- 楊玉影 -->
  <div class="subsection">
    <div class="subsection-title">楊玉影's Family · Hong Kong</div>
    <div class="gen-row">
      <div class="couple">
        <div class="card yang"><div class="card-name">楊玉影</div><div class="card-year">b. 1938 · HK</div></div>
        <div class="sx">×</div>
        <div class="card in-law"><div class="card-name">李志剛</div><div class="card-year">b. 1939 · HK</div></div>
      </div>
    </div>
    <div class="arr">↓ Gen 4 children</div>
    <div class="gen-row">
      <div class="card in-law"><div class="card-name">李道恩</div><div class="card-year">b. 1969 · HK</div><div class="card-note">× 鄧佩雯 → 李國義 (2019)</div></div>
      <div class="card in-law"><div class="card-name">李道真</div><div class="card-year">b. 1972 · HK</div><div class="card-note">× 陸靜儀 → 李謙羭 (2001), 李謙翔 (2003)</div></div>
      <div class="card in-law"><div class="card-name">李道賢</div><div class="card-year">b. 1977 · HK</div><div class="card-note">× 甘振揚 → 甘來恩 (2014), 甘來希 (2017)</div></div>
    </div>
  </div>
</div>


<!-- 楊尊三 branch -->
<div class="section">
  <div class="section-title">楊尊三's Family — Five Siblings</div>
  <div class="gen-row">
    <div class="couple">
      <div class="card yang deceased"><div class="card-name">楊尊三</div><div class="card-year">b. 1892 · d. 1945</div></div>
      <div class="sx">×</div>
      <div class="card in-law deceased"><div class="card-name">陳幗卿</div><div class="card-year">b. 1892</div></div>
    </div>
  </div>
  <div class="arr">↓ Generation 3 children</div>
  <div class="gen-row">
    <div class="card yang deceased"><div class="card-name">楊伯鵬</div><div class="card-year">b. 1913 · d. 2009</div><div class="card-note">× 李紅梅 · see below</div></div>
    <div class="card yang deceased"><div class="card-name">楊琇珍</div><div class="card-note">× 李清慰 (both dec.)</div></div>
    <div class="card yang deceased"><div class="card-name">楊琇娟</div><div class="card-year">1923–2014</div><div class="card-note">× 劉裕瑄 · see below</div></div>
    <div class="card yang deceased"><div class="card-name">楊琇瑛</div><div class="card-year">b. 1929 · d. 2020</div><div class="card-note">× 林正基 · see below</div></div>
    <div class="card yang deceased"><div class="card-name">楊伯倫</div><div class="card-year">b. 1931 · d. 2023</div><div class="card-note">× 林幼梅 · see below</div></div>
  </div>

  <!-- 楊伯鵬 -->
  <div class="subsection">
    <div class="subsection-title">楊伯鵬's Family (1913–2009)</div>
    <div class="gen-row">
      <div class="couple">
        <div class="card yang deceased"><div class="card-name">楊伯鵬</div><div class="card-year">b. 1913 · d. 2009</div></div>
        <div class="sx">×</div>
        <div class="card in-law deceased"><div class="card-name">李紅梅</div><div class="card-year">b. 1914 · d. 1989</div></div>
      </div>
    </div>
    <div class="arr">↓ Gen 4 children</div>
    <div class="gen-row">
      <div class="card yang"><div class="card-name">楊碧文</div><div class="card-year">b. 1941 · Los Angeles</div><div class="card-note">× 周士光 → 周詠詞, 周詠詳</div></div>
      <div class="card yang"><div class="card-name">楊祖志</div><div class="card-year">b. 1946</div><div class="card-note">× 朱麗萍 → 楊忻忻, 楊永匡</div></div>
      <div class="card yang"><div class="card-name">楊碧心</div><div class="card-year">b. 1948</div><div class="card-note">× 顏耀璋 → 顏芳瑜 (× 吳敏華)</div></div>
      <div class="card yang deceased"><div class="card-name">楊祖成</div><div class="card-year">b. 1950 · d. 2017</div><div class="card-note">× 鍾麗霞 → 楊忻玪 (× 黃頴生)</div></div>
      <div class="card yang deceased"><div class="card-name">楊祖浩</div><div class="card-year">b. 1952 · d. 2017</div></div>
    </div>
  </div>

  <!-- 楊琇娟 -->
  <div class="subsection">
    <div class="subsection-title">楊琇娟's Family (1923–2014)</div>
    <div class="gen-row">
      <div class="couple">
        <div class="card yang deceased"><div class="card-name">楊琇娟</div><div class="card-year">1923–2014</div></div>
        <div class="sx">×</div>
        <div class="card in-law deceased"><div class="card-name">劉裕瑄</div><div class="card-year">1918–2014</div></div>
      </div>
    </div>
    <div class="arr">↓ Gen 4 child</div>
    <div class="gen-row">
      <div class="couple">
        <div class="card in-law"><div class="card-name">劉芳之</div><div class="card-year">b. 1955</div></div>
        <div class="sx">×</div>
        <div class="card in-law"><div class="card-name">謝明</div><div class="card-alias">Ming Hsieh</div><div class="card-year">b. 1956</div><div class="card-note">divorced · Founder, Cogent Systems</div></div>
      </div>
    </div>
    <div class="arr">↓ Gen 5 children</div>
    <div class="gen-row">
      <div class="card in-law"><div class="card-name">謝沛琳</div><div class="card-year">b. 1988</div></div>
      <div class="card in-law"><div class="card-name">謝沛婷</div><div class="card-year">b. 1991</div><div class="card-note">× 李芳杰 (b. 1991)</div></div>
    </div>
    <div class="gen-label">Gen 6 — 謝沛婷's children</div>
    <div class="gen-row">
      <div class="card in-law"><div class="card-name">李式明</div><div class="card-year">b. 2024</div></div>
      <div class="card in-law"><div class="card-name">李式浩</div><div class="card-year">b. 2026</div></div>
    </div>
  </div>

  <!-- 楊琇瑛 -->
  <div class="subsection">
    <div class="subsection-title">楊琇瑛's Family (1929–2020)</div>
    <div class="gen-row">
      <div class="couple">
        <div class="card yang deceased"><div class="card-name">楊琇瑛</div><div class="card-year">b. 1929 · d. 2020</div></div>
        <div class="sx">×</div>
        <div class="card in-law deceased"><div class="card-name">林正基</div><div class="card-year">b. 1931 · d. 2022</div></div>
      </div>
    </div>
    <div class="arr">↓ Gen 4 children</div>
    <div class="gen-row">
      <div class="card in-law"><div class="card-name">林澤崑</div><div class="card-year">b. 1959</div><div class="card-note">× 孫䁱滌 → 林恩瀚 (b. 2009)</div></div>
      <div class="card in-law"><div class="card-name">林澤堅</div><div class="card-alias">Daniel</div><div class="card-year">b. 1964</div><div class="card-note">× 李淑賢 (Helen) → 林綽渝 (2003), 林子浩 (2008)</div></div>
    </div>
  </div>

  <!-- 楊伯倫 -->
  <div class="subsection">
    <div class="subsection-title">楊伯倫's Family · Hong Kong</div>
    <div class="gen-row">
      <div class="couple">
        <div class="card yang deceased"><div class="card-name">楊伯倫</div><div class="card-year">b. 1931 · d. 2023</div></div>
        <div class="sx">×</div>
        <div class="card in-law"><div class="card-name">林幼梅</div><div class="card-year">b. 1939 · Hong Kong</div></div>
      </div>
    </div>
    <div class="arr">↓ Gen 4 children</div>
    <div class="gen-row">
      <div class="card yang"><div class="card-name">楊碧惠</div><div class="card-year">b. 1968</div><div class="card-note">× 詹兆輝 (b. 1961)</div></div>
      <div class="card yang"><div class="card-name">楊碧樺</div><div class="card-year">b. 1969</div></div>
      <div class="card yang"><div class="card-name">楊祖權</div><div class="card-year">b. 1973 · SF Bay Area</div><div class="card-note">× 何佳穎 (b. 1977)</div></div>
    </div>
    <div class="gen-label" style="margin-top:8px;">楊碧惠 × 詹兆輝 → Gen 5</div>
    <div class="gen-row">
      <div class="card in-law"><div class="card-name">詹弘信</div><div class="card-year">b. 1999</div></div>
      <div class="card in-law"><div class="card-name">詹詠心</div><div class="card-year">b. 2003</div></div>
    </div>
    <div class="gen-label">楊祖權 × 何佳穎 → Gen 5</div>
    <div class="gen-row">
      <div class="card yang"><div class="card-name">楊澤凱</div><div class="card-year">b. 2007 · N. California</div></div>
      <div class="card yang"><div class="card-name">楊澤安</div><div class="card-year">b. 2011 · N. California</div></div>
    </div>
  </div>
</div>
"""

# ── Assemble full HTML ────────────────────────────────────────────────────────
html = f"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>楊氏家族樹 · Yeung Family Tree</title>
<style>{CSS}</style>
</head>
<body>
<h1>楊氏家族樹 · Yeung Family Tree</h1>
<div class="subtitle">Six generations · Seattle · Hong Kong · Antwerp · San Diego · Melbourne · Vancouver · New Jersey · Northern California</div>
<div class="datestamp-wrap"><span class="datestamp">Data last updated: {data_date}</span></div>
<div class="legend">
  <div class="legend-item"><div class="legend-dot" style="background:#4A7FBB;"></div>楊氏 bloodline</div>
  <div class="legend-item"><div class="legend-dot" style="background:#7BAF8E;"></div>Married in</div>
  <div class="legend-item" style="opacity:0.65;"><div class="legend-dot" style="background:#4A7FBB;"></div>† Deceased (faded)</div>
</div>
{BODY}
<div class="tree-footer">
  Generated {date.today().strftime('%B %-d, %Y')} · Source: {csv_filename} · 楊氏家族樹
</div>
</body>
</html>"""

# ── Write index.html ──────────────────────────────────────────────────────────
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Written: index.html")

# ── Save versioned copy ───────────────────────────────────────────────────────
os.makedirs("versions", exist_ok=True)
version_filename = f"versions/Yeung_Family_Tree_{date.today().strftime('%Y-%m-%d')}.html"
with open(version_filename, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Written: {version_filename}")
