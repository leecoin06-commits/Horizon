#!/usr/bin/env python3
"""Turn Horizon's latest English Markdown into an Arabic RTL report."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from html import escape
import os, re, json, urllib.request

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "arabic"

def chunks(data, size=5500):
    return [data[i:i+size] for i in range(0, len(data), size)]

def translate(data):
    key = os.environ["OPENAI_API_KEY"]
    output = []
    for chunk in chunks(data):
        body = {"model": os.getenv("TRANSLATE_MODEL", "gpt-4o-mini"),
                "messages": [
                    {"role": "system", "content": "Translate this financial news report into accurate Modern Standard Arabic Markdown. Retain URLs, references, exact dates, numbers, ticker symbols BTC, IBIT, NVDA, TSLA, USD. Do not invent facts. Keep quantum risks properly qualified."},
                    {"role": "user", "content": chunk}
                ], "temperature": 0.2}
        req = urllib.request.Request("https://api.openai.com/v1/chat/completions",
              data=json.dumps(body).encode(), method="POST",
              headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=120) as response:
            output.append(json.load(response)["choices"][0]["message"]["content"])
    return "\n\n".join(output)

def render_line(line):
    # Escape all untrusted news content before introducing safe links.
    pieces, start = [], 0
    for m in re.finditer(r"\[([^\]]+)\]\((https?://[^\s)]+)\)", line):
        pieces.append(escape(line[start:m.start()]))
        pieces.append('<a target="_blank" rel="noopener noreferrer" href="' + escape(m.group(2), quote=True) + '">' + escape(m.group(1)) + '</a>')
        start = m.end()
    return "".join(pieces) + escape(line[start:])

def html_body(markdown):
    result = []
    for line in markdown.splitlines():
        if not line.strip(): continue
        heading = re.match(r"^(#{1,5})\s+(.*)$", line)
        if heading:
            level = len(heading.group(1))
            result.append(f"<h{level}>{render_line(heading.group(2))}</h{level}>")
        elif line.startswith(("- ", "* ")):
            result.append("<p>• " + render_line(line[2:]) + "</p>")
        else:
            result.append("<p>" + render_line(line) + "</p>")
    return "\n".join(result)

def main():
    candidates = list((ROOT / "data" / "summaries").glob("*-en.md"))
    if not candidates:
        raise RuntimeError("No English Markdown report under data/summaries")
    source = max(candidates, key=lambda p: p.stat().st_mtime)
    data = source.read_text(encoding="utf-8")
    if len(data.strip()) < 80:
        raise RuntimeError("Horizon generated an unexpectedly short summary")
    arabic = translate(data)
    today = datetime.now(ZoneInfo("Asia/Riyadh")).strftime("%Y-%m-%d")
    archive = OUTPUT / "archive"
    archive.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "latest.md").write_text(arabic + "\n", encoding="utf-8")
    (archive / f"{today}.md").write_text(arabic + "\n", encoding="utf-8")
    dates = sorted(archive.glob("*.md"), reverse=True)[:35]
    links = "\n".join(f'<li><a href="archive/{p.name}">{p.stem}</a></li>' for p in dates)
    html = f"""<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>رادار البيتكوين والأسواق</title>
<style>body{{font-family:Tahoma,"Noto Sans Arabic",Arial,sans-serif;line-height:1.9;background:#f5f7fa;color:#13253a;margin:auto;max-width:950px;padding:22px;direction:rtl}}main{{background:white;border-radius:14px;padding:28px}}h1,h2,h3{{color:#005b84}}p{{unicode-bidi:plaintext}}a{{color:#1264a3;overflow-wrap:anywhere}}@media(max-width:650px){{body{{padding:8px}}main{{padding:14px}}}}</style></head>
<body><header><h1>رادار البيتكوين والأسواق</h1><p>تقرير آلي بتاريخ {today} بتوقيت الرياض — ليس توصية استثمارية</p></header><main>{html_body(arabic)}</main><footer><h2>الأرشيف</h2><ul>{links}</ul><a href="latest.md">تنزيل التقرير العربي</a></footer></body></html>"""
    (OUTPUT / "index.html").write_text(html, encoding="utf-8")
    print("Built Arabic report from", source)

if __name__ == "__main__":
    main()
