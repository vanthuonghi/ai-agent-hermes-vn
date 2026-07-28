# -*- coding: utf-8 -*-
"""
Daily AI Brief — Research AI & AI Agent trends, synthesize, output HTML.
File name: YYYY-MM-DD.html in ~/Desktop/Nơi Rộng Hiểu Biết AI/
Runs at 7:30am via cron. Uses hermes web_search + web_extract.
"""
import os, datetime, html

DESKTOP = "/Users/vanhi/Desktop"
FOLDER = os.path.join(DESKTOP, "Nới Rộng Hiểu Biết AI")
os.makedirs(FOLDER, exist_ok=True)

TODAY = datetime.date.today()
DATE_STR = TODAY.strftime("%Y-%m-%d")
DATE_HUMAN = TODAY.strftime("%d/%m/%Y")

# This script is run by the agent's terminal toolset with web access.
# But since no_agent cron runs plain python WITHOUT web tools, we instead
# produce the research by calling external fetch. To keep it self-contained
# and runnable via no_agent, we embed a fallback: the cron prompt will do the
# real research via hermes web_search, then write the HTML. This script is the
# HTML generator given a content dict.

def render_html(items, date_str, date_human):
    """items: list of dict {title, summary, source, url, tags}"""
    cards = ""
    for it in items:
        cards += f'''
<div class="item">
  <h3><a href="{it.get('url','#')}" target="_blank" rel="noopener">{html.escape(it.get('title',''))}</a></h3>
  <p class="sum">{html.escape(it.get('summary',''))}</p>
  <p class="meta">📌 {html.escape(it.get('source',''))} · 🏷️ {html.escape(', '.join(it.get('tags',[])))}</p>
</div>'''
    doc = f'''<!DOCTYPE html>
<html lang="vi"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Brief {date_str} — Nới Rộng Hiểu Biết AI</title>
<style>
:root{{--bg:#0a0e1a;--surface:#121829;--ink:#e8ecf5;--muted:#8b95ad;--accent:#f59e0b}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--ink);line-height:1.7;padding:32px 20px}}
.wrap{{max-width:820px;margin:0 auto}}
h1{{font-size:30px;color:var(--accent);margin-bottom:6px}}
.date{{color:var(--muted);margin-bottom:24px}}
.intro{{background:var(--surface);border-left:3px solid var(--accent);padding:14px 18px;border-radius:0 10px 10px 0;margin-bottom:28px;color:var(--muted)}}
.item{{background:var(--surface);border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:20px;margin:16px 0}}
.item h3{{font-size:19px;margin-bottom:8px}}
.item h3 a{{color:var(--ink);text-decoration:none}}
.item h3 a:hover{{color:var(--accent)}}
.sum{{color:var(--muted);font-size:15.5px;margin:8px 0}}
.meta{{color:#5a647e;font-size:13px}}
footer{{margin-top:40px;padding-top:20px;border-top:1px solid rgba(255,255,255,.08);color:#5a647e;font-size:13px;text-align:center}}
</style></head>
<body><div class="wrap">
<h1>🤖 AI Brief — {date_str}</h1>
<p class="date">Nới Rộng Hiểu Biết AI · {date_human}</p>
<div class="intro">Tổng hợp mỗi sáng từ Hermes: những thông tin, công nghệ, xu hướng mới về AI & AI Agent để mình và anh cùng học. Nguồn: tìm kiếm web tổng hợp.</div>
{cards}
<footer>Được tạo tự động bởi Hermes Agent · 7h30 sáng mỗi ngày</footer>
</div></body></html>'''
    return doc

if __name__ == "__main__":
    # When run directly (no_agent), generate from a placeholder if no content passed.
    # The cron prompt does real research then calls render with items.
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo = [
            {"title":"Demo: Chạy cron thật sẽ có tin thật","summary":"Đây là file mẫu. Khi cron 7h30 chạy, Hermes sẽ research và điền tin thật vào đây.","source":"Hermes","url":"#","tags":["demo"]}
        ]
        out = os.path.join(FOLDER, f"{DATE_STR}.html")
        open(out,"w",encoding="utf-8").write(render_html(demo, DATE_STR, DATE_HUMAN))
        print("✅ demo written:", out)
