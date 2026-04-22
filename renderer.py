from datetime import datetime, timezone, timedelta
from pathlib import Path

from config import SOURCE_COLORS, TOPIC_COLORS

TOPICS = ["インフラ", "モバイル", "フロントエンド", "AI/ML", "セキュリティ"]
TEMPLATE_PATH = Path(__file__).parent / "templates" / "index.html"


def _build_articles(articles):
    parts = []
    for a in articles:
        sc = SOURCE_COLORS.get(a["source"], {"bg": "#f0f0f0", "text": "#333"})
        topic_badge = ""
        if a["topic"]:
            tc = TOPIC_COLORS.get(a["topic"], {"bg": "#f0f0f0", "text": "#333"})
            topic_badge = (
                f'<span class="topic-tag" style="background:{tc["bg"]};color:{tc["text"]}">'
                f'{a["topic"]}</span>'
            )
        summary_html = f'<p class="summary">{a["summary"]}</p>' if a["summary"] else ""
        topic_val = a["topic"] or ""
        parts.append(
            f'  <article data-source="{a["source"]}" data-topic="{topic_val}">\n'
            f'    <div class="meta">\n'
            f'      <span class="source-tag" style="background:{sc["bg"]};color:{sc["text"]}">{a["source"]}</span>\n'
            f'      {topic_badge}\n'
            f'      <span class="date">{a["date"]}</span>\n'
            f'    </div>\n'
            f'    <h2><a href="{a["url"]}" target="_blank" rel="noopener noreferrer">{a["title"]}</a></h2>\n'
            f'    {summary_html}\n'
            f'  </article>'
        )
    return "\n".join(parts)


def _build_source_buttons(sources):
    btns = ['<button class="filter-btn active" data-filter="source" data-value="all">すべて</button>']
    for src in sorted(sources):
        btns.append(f'<button class="filter-btn" data-filter="source" data-value="{src}">{src}</button>')
    return "".join(btns)


def _build_topic_buttons():
    btns = ['<button class="filter-btn active" data-filter="topic" data-value="all">すべて</button>']
    for t in TOPICS:
        tc = TOPIC_COLORS[t]
        btns.append(
            f'<button class="filter-btn" data-filter="topic" data-value="{t}"'
            f' data-bg="{tc["bg"]}" data-text="{tc["text"]}">{t}</button>'
        )
    return "".join(btns)


def generate_html(articles):
    JST = timezone(timedelta(hours=9))
    updated_at = datetime.now(JST).strftime("%Y年%-m月%-d日 %H:%M")

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    return (
        template
        .replace("%%UPDATED_AT%%",  updated_at)
        .replace("%%ARTICLES%%",    _build_articles(articles))
        .replace("%%SOURCE_BTNS%%", _build_source_buttons({a["source"] for a in articles}))
        .replace("%%TOPIC_BTNS%%",  _build_topic_buttons())
    )
