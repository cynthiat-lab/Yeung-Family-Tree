"""
generate_tree.py
Reads the latest CSV from data/, generates index.html,
and saves a dated version to versions/.
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
csv_date = date.fromtimestamp(os.path.getmtime(csv_path)).strftime("%B %-d, %Y")
csv_filename = os.path.basename(csv_path)
print(f"Using: {csv_path} (dated {csv_date})")

# ── Parse CSV ─────────────────────────────────────────────────────────────────
people = {}   # name -> dict of fields

def clean(s):
    return (s or "").strip()

with open(csv_path, encoding="utf-8-sig") as f:
    reader = csv.reader(f)
    header_row = None
    for row in reader:
        # Find header row
        if header_row is None:
            joined = ",".join(row)
            if "Full Name" in joined:
                header_row = [c.strip().replace("\n", " ") for c in row]
            continue

        if len(row) < len(header_row):
            row += [""] * (len(header_row) - len(row))

        def get(col):
            try:
                idx = next(i for i, h in enumerate(header_row) if col.lower() in h.lower())
                return clean(row[idx])
            except StopIteration:
                return ""

        name = get("Full Name")
        if not name:
            continue

        birth  = get("Birth Year")
        father = get("Father")
        mother = get("Mother")
        spouse = get("Spouse")
        maiden = get("Maiden")
        children = get("Children")
        notes  = get("Notes")

        # Normalise birth — keep only year portion for display
        birth_display = re.sub(r"\s+\d{1,2}-\d{1,2}", "", birth).strip()

        # Detect deceased from notes
        deceased = bool(re.search(r"去世|d\.\s*\d|died|\d{4}–\d{4}|\d{4}-\d{4}", notes + birth, re.I))

        # Detect deceased from birth field that contains death year (e.g. "1913-2009")
        if re.search(r"\d{4}[-–]\d{4}", birth):
            deceased = True
            birth_display = birth.strip()

        people[name] = {
            "name": name,
            "birth": birth_display,
            "father": father,
            "mother": mother,
            "spouse": spouse,
            "maiden": maiden,
            "children": [c.strip() for c in re.split(r"[，,]", children) if c.strip()],
            "notes": notes,
            "deceased": deceased,
        }

# ── HTML helpers ──────────────────────────────────────────────────────────────

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def is_yang(name):
    """True if the person carries the 楊 surname or was born Yang."""
    p = people.get(name, {})
    maiden = p.get("maiden", "")
    return name.startswith("楊") or maiden == "楊"

def card(name, extra_note=""):
    p = people.get(name, {})
    yang = is_yang(name)
    dead = p.get("deceased", False) if p else False
    birth = p.get("birth", "") if p else ""
    notes = p.get("notes", "") if p else ""
    spouse = p.get("spouse", "") if p else ""

    cls = "card " + ("yang" if yang else "in-law") + (" deceased" if dead else "")

    # English alias from notes or name field (text in parentheses)
    alias_match = re.search(r"\(([A-Za-z][^)]+)\)", name)
    alias = alias_match.group(1) if alias_match else ""
    display_name = name.replace(f"({alias})", "").strip() if alias else name

    # Location hint
    loc = ""
    for kw in ["Seattle", "Antwerp", "San Diego", "Hong Kong", "NJ", "California",
               "Bay Area", "Media PA", "Manila"]:
        if kw in notes:
            loc = kw
            break

    html = f'<div class="{cls}">'
    html += f'<div class="card-name">{esc(display_name)}</div>'
    if alias:
        html += f'<div class="card-alias">{esc(alias)}</div>'
    if birth:
        html += f'<div class="card-year">{esc(birth)}</div>'
    if loc:
        html += f'<div class="card-note">{esc(loc)}</div>'
    if extra_note:
        html += f'<div class="card-note">{esc(extra_note)}</div>'
    html += "</div>"
    return html

def couple_row(p1, p2, note1="", note2=""):
    return (
        '<div class="gen-row"><div class="couple">'
        + card(p1, note1)
        + '<div class="sx">×</div>'
        + card(p2, note2)
        + "</div></div>"
    )

def gen_row(names, notes=None):
    notes = notes or {}
    html = '<div class="gen-row">'
    for n in names:
        html += card(n, notes.get(n, ""))
    html += "</div>"
    return html

def arr(text="↓"):
    return f'<div class="arr">{text}</div>'

def gen_label(text):
    return f'<div class="gen-label">{esc(text)}</div>'

def section(title, content):
    return (
        '<div class="section">'
        f'<div class="section-title">{esc(title)}</div>'
        + content
        + "</div>"
    )

def subsection(title, content):
    return (
        '<div class="subsection">'
        f'<div class="subsection-title">{esc(title)}</div>'
        + content
        + "</div>"
    )

# ── Build HTML body ───────────────────────────────────────────────────────────

body = ""

# ── ANCESTORS ────────────────────────────────────────────────────────────────
body += section("Ancestors — Generations 0 &amp; 1",
    gen_label("Generation 0")
    + couple_row("楊鳳旌", "廖氏")
    + arr()
    + gen_label("Generation 1")
    + couple_row("楊亦祥", "鍾氏")
    + arr("↓ Generation 2 children")
    + gen_row(["楊煒廷", "楊專三", "楊用好", "楊先行", "楊尋"],
              {"楊煒廷": "→ 2 families below", "楊專三": "→ 5 children below",
               "楊用好": "適陳氏", "楊先行": "適黃氏", "楊尋": "適李氏"})
)

# ── 楊煒廷 × 黃惠蘭 ──────────────────────────────────────────────────────────
body += section("楊煒廷 × 黃惠蘭 — First Family",
    couple_row("楊煒廷", "黃惠蘭")
    + arr("↓ Generation 3 children")
    + gen_row(["楊伯章", "楊伯贊", "楊英鰲", "楊金重", "楊玉容"],
              {"楊伯章": "2 wives · see below", "楊伯贊": "2 wives · see below",
               "楊英鰲": "× 馬靜如 · see below", "楊金重": "no further data",
               "楊玉容": "× 李沃芬 · see below"})

    # 楊英鰲
    + subsection("楊英鰲's Family",
        couple_row("楊英鰲", "馬靜如")
        + arr("↓ Generation 4 children")
        + gen_row(["楊碧玹", "楊碧琳", "楊碧瓘", "楊祖由", "楊碧瓖"])
        + gen_label("楊碧玹 → Gen 5")
        + gen_row(["楊奇葩"], {"楊奇葩": "× Katrin Jogi (div.) → Maasika"})
        + gen_label("楊碧琳 × 利忠能 → Gen 5")
        + gen_row(["利思維", "利思欣"])
        + gen_label("Gen 6 — their children")
        + gen_row(["利樂真", "利樂中", "高靜慧", "高靖博"])
        + gen_label("楊碧瓘 × 戴自海 → Gen 5")
        + gen_row(["戴琦", "戴琳"])
        + gen_label("Gen 6 — their children")
        + gen_row(["戴奇華", "戴傑華", "葉靜", "葉君安", "葉留餘"])
        + gen_label("楊碧瓖 × Nagi Awas → Gen 5")
        + gen_row(["Darek Awas"])
        + gen_label("Gen 6 — Darek's children")
        + gen_row(["Marshall Awas", "Afina Awas", "Anderson Awas"])
    )

    # 楊伯章
    + subsection("楊伯章's Family (d. 1959 · two wives)",
        gen_label("Wife 1: 梁Pauline")
        + gen_row(["楊祖敏", "楊碧玫", "楊碧瑤"],
                  {"楊碧玫": "× Richard Wong → Irenie, Elisa"})
        + gen_label("Wife 2: 劉南絲")
        + gen_row(["楊祖建"])
    )

    # 楊伯贊
    + subsection("楊伯贊's Family (b. 1903 · two wives)",
        gen_label("Wife 1: 劉玉如 (1904–1932)")
        + gen_row(["楊麗坤", "楊祖銘", "楊祖榆"],
                  {"楊祖銘": "× Carlyn Hamaan",
                   "楊祖榆": "→ 楊虹, 楊靖睘 (Allison), 楊澤宇 (Jason)"})
        + gen_label("Wife 2: 陳潤桂 (1914–2014)")
        + gen_row(["楊碧琪", "楊祖良"],
                  {"楊碧琪": "× Xuyen Vuong → 王青律, 王青綸, 王青彬"})
    )

    # 楊玉容
    + subsection("楊玉容's Family",
        couple_row("楊玉容", "李沃芬")
        + arr()
        + gen_row(["李世侃", "李世任", "李世儒"],
                  {"李世侃": "b.1943 · d.2020", "李世任": "→ Ivar, Samantha?",
                   "李世儒": "→ Benjamin, Daniel, Mathew, Sebastian"})
    )
)

# ── 楊煒廷 × 胡氏 ────────────────────────────────────────────────────────────
body += section("楊煒廷 × 胡氏 — Second Family",
    couple_row("楊煒廷", "胡氏")
    + arr("↓ Generation 3 children")
    + gen_row(["楊金愛", "楊伯駿", "楊伯馴 (Albert Young)", "楊玉影"],
              {"楊金愛": "× 鐘士豪 → 鐘伊雲 → Cheryl",
               "楊伯駿": "× 鄧慧賢 · see below",
               "楊伯馴 (Albert Young)": "× 羅慧嘉 · see below",
               "楊玉影": "× 李志剛 · see below"})

    # 楊伯駿
    + subsection("楊伯駿's Family · Media PA",
        couple_row("楊伯駿", "鄧慧賢 (Julianna)")
        + arr("↓ Gen 4 children")
        + gen_row(["楊碧瑩 ", "楊祖恩"],
                  {"楊碧瑩 ": "× 屈振祥 → 屈穎琳 (b.2004)",
                   "楊祖恩": "× 楊詠紅 (b.1966)"})
    )

    # 楊伯馴
    + subsection("楊伯馴's Family",
        couple_row("楊伯馴 (Albert Young)", "羅慧嘉 (Barbara Young)")
        + arr("↓ Gen 4 child")
        + couple_row("楊祖能 (Jonas Young)", "伍惠娟 (Sharon Young)")
        + gen_label("Gen 5")
        + gen_row(["楊靖婷 (Laura Stella Young)"])
    )

    # 楊玉影
    + subsection("楊玉影's Family",
        couple_row("楊玉影", "李志剛")
        + arr("↓ Gen 4 children")
        + gen_row(["李道恩", "李道真", "李道賢"],
                  {"李道恩": "× 鄧佩雯 → 李國義 (2019)",
                   "李道真": "× 陸靜儀 → 李謙羭 (2001), 李謙翔 (2003)",
                   "李道賢": "× 甘振揚 → 甘來恩 (2014), 甘來希 (2017)"})
    )
)

# ── 楊專三 ───────────────────────────────────────────────────────────────────
body += section("楊專三's Family — Five Siblings",
    couple_row("楊專三", "陳幗卿")
    + arr("↓ Generation 3 children")
    + gen_row(["楊伯鵬", "楊琇珍", "楊琇娟", "楊琇瑛", "楊伯倫"],
              {"楊伯鵬": "× 李紅梅 · see below", "楊琇珍": "× 李清慰",
               "楊琇娟": "× 劉裕宣 · see below", "楊琇瑛": "× 林正基 · see below",
               "楊伯倫": "× 林幼梅 · see below"})

    # 楊伯鵬
    + subsection("楊伯鵬's Family (1913–2009)",
        couple_row("楊伯鵬", "李紅梅")
        + arr("↓ Gen 4 children")
        + gen_row(["楊碧文", "楊祖志", "楊碧心", "楊祖成", "楊祖浩"],
                  {"楊碧文": "× 周士光 → 周詠詞, 周詠詳",
                   "楊祖志": "× 朱麗萍 → 楊忻忻, 楊永匡",
                   "楊碧心": "× 顏耀璋 → 顏芳瑜 (× 吳敏華)",
                   "楊祖成": "× 鍾麗霞 → 楊忻玪 (× 黃頴生)"})
    )

    # 楊琇娟
    + subsection("楊琇娟's Family (1923–2014)",
        couple_row("楊琇娟", "劉裕宣")
        + arr("↓ Gen 4 child")
        + couple_row("劉芳之", "謝明")
        + arr("↓ Gen 5 children")
        + gen_row(["謝沛琳", "謝沛婷"],
                  {"謝沛婷": "× 李芳杰 → 李式明 (2024), 李式浩 (2026)"})
    )

    # 楊琇瑛
    + subsection("楊琇瑛's Family",
        couple_row("楊琇瑛", "林正基")
        + arr("↓ Gen 4 children")
        + gen_row(["林澤崑", "林澤堅"],
                  {"林澤崑": "× 孫䁱滌 → 林恩瀚",
                   "林澤堅": "× 李淑賢 → 林綽渝 (2003), 林子浩 (2008)"})
    )

    # 楊伯倫
    + subsection("楊伯倫's Family · Hong Kong",
        couple_row("楊伯倫", "林幼梅")
        + arr("↓ Gen 4 children")
        + gen_row(["楊碧惠", "楊碧樺", "楊祖權"],
                  {"楊碧惠": "× 詹兆輝", "楊祖權": "× 何佳穎"})
        + gen_label("楊碧惠 × 詹兆輝 → Gen 5")
        + gen_row(["詹弘信", "詹詠心"])
        + gen_label("楊祖權 × 何佳穎 → Gen 5")
        + gen_row(["楊澤凱", "楊澤安"])
    )
)

# ── Assemble full HTML ────────────────────────────────────────────────────────
html = f"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>楊氏家族樹 · Yeung Family Tree</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: Georgia, 'Times New Roman', serif; background: #f7f5f0; color: #222; padding: 24px 16px; }}
h1 {{ text-align: center; font-size: 22px; font-weight: 400; color: #2a2520; margin-bottom: 4px; letter-spacing: 0.02em; }}
.subtitle {{ text-align: center; font-size: 13px; color: #999; margin-bottom: 10px; font-style: italic; }}
.datestamp-wrap {{ text-align: center; margin-bottom: 20px; }}
.datestamp {{ display: inline-block; font-size: 12px; color: #aaa; background: #fff; padding: 5px 14px; border-radius: 20px; border: 0.5px solid #e0ddd5; letter-spacing: 0.02em; }}
.legend {{ display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; margin-bottom: 24px; }}
.legend-item {{ display: flex; align-items: center; gap: 6px; font-size: 11px; color: #777; }}
.legend-dot {{ width: 10px; height: 10px; border-radius: 2px; flex-shrink: 0; }}
.section {{ background: #fff; border-radius: 12px; border: 0.5px solid #e0ddd5; padding: 20px 16px; margin-bottom: 18px; }}
.section-title {{ font-size: 11px; font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase; color: #aaa; margin-bottom: 14px; padding-bottom: 8px; border-bottom: 0.5px solid #ece9e2; }}
.subsection {{ margin-top: 16px; padding-top: 14px; border-top: 0.5px dashed #e5e2db; }}
.subsection-title {{ font-size: 10px; font-weight: 500; letter-spacing: 0.06em; text-transform: uppercase; color: #bbb; margin-bottom: 10px; }}
.gen-row {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 9px; margin-bottom: 8px; }}
.gen-label {{ font-size: 10px; color: #ccc; text-align: center; letter-spacing: 0.04em; margin: 4px 0 8px; }}
.card {{ width: 118px; background: #fff; border: 0.5px solid #ccc; border-radius: 8px; padding: 7px 8px 8px; text-align: center; flex-shrink: 0; }}
.card.yang {{ border-top: 2.5px solid #4A7FBB; }}
.card.in-law {{ border-top: 2.5px solid #bbb; }}
.card.deceased {{ opacity: 0.62; }}
.card-name {{ font-size: 11.5px; font-weight: 500; color: #1a1a1a; line-height: 1.3; }}
.card-year {{ font-size: 10px; color: #aaa; margin-top: 2px; line-height: 1.3; }}
.card-note {{ font-size: 9.5px; color: #999; margin-top: 2px; font-style: italic; line-height: 1.25; }}
.card-alias {{ font-size: 9.5px; color: #bbb; margin-top: 2px; line-height: 1.3; }}
.couple {{ display: flex; align-items: flex-start; gap: 4px; }}
.sx {{ font-size: 11px; color: #ccc; padding-top: 14px; flex-shrink: 0; }}
.arr {{ text-align: center; font-size: 11px; color: #ccc; margin: 3px 0 4px; }}
.footer {{ font-size: 10px; color: #ccc; text-align: center; margin-top: 6px; line-height: 1.9; font-style: italic; }}
</style>
</head>
<body>
<h1>楊氏家族樹 · Yeung Family Tree</h1>
<div class="subtitle">Six generations · Seattle · Hong Kong · Antwerp · San Diego · New Jersey · Northern California</div>
<div class="datestamp-wrap"><span class="datestamp">Data last updated: {csv_date}</span></div>
<div class="legend">
  <div class="legend-item"><div class="legend-dot" style="background:#4A7FBB;"></div>楊氏 bloodline</div>
  <div class="legend-item"><div class="legend-dot" style="background:#bbb;"></div>Married in</div>
  <div class="legend-item" style="opacity:0.6;"><div class="legend-dot" style="background:#888;"></div>Deceased (faded)</div>
</div>
{body}
<div class="footer">Generated {date.today().strftime('%B %-d, %Y')} · Source: {esc(csv_filename)} · 楊氏家族樹</div>
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
