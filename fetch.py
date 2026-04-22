import feedparser
import re
import html as html_module
from datetime import datetime, timezone
from pathlib import Path

FEEDS = [
    {"name": "Zenn", "url": "https://zenn.dev/feed"},
    {"name": "Qiita", "url": "https://qiita.com/popular-items/feed"},
    {"name": "はてなブックマーク", "url": "https://b.hatena.ne.jp/hotentry/it.rss"},
    {"name": "gihyo.jp", "url": "https://gihyo.jp/feed/rss2"},
    {"name": "ITmedia", "url": "https://rss.itmedia.co.jp/rss/2.0/news_bursts.xml"},
]

ARTICLES_PER_FEED = 20

SOURCE_COLORS = {
    "Zenn":         {"bg": "#e8f5e9", "text": "#2e7d32"},
    "Qiita":        {"bg": "#e8f5e9", "text": "#55c500"},
    "はてなブックマーク": {"bg": "#fff3e0", "text": "#e65100"},
    "gihyo.jp":     {"bg": "#e3f2fd", "text": "#1565c0"},
    "ITmedia":      {"bg": "#fce4ec", "text": "#c62828"},
}


def strip_tags(text):
    return re.sub(r"<[^>]+>", "", text or "").strip()


def fetch_articles():
    articles = []
    for feed_info in FEEDS:
        try:
            feed = feedparser.parse(feed_info["url"])
            for entry in feed.entries[:ARTICLES_PER_FEED]:
                published = entry.get("published_parsed") or entry.get("updated_parsed")
                if published:
                    dt = datetime(*published[:6], tzinfo=timezone.utc)
                    date_str = dt.strftime("%Y年%-m月%-d日")
                    timestamp = dt.timestamp()
                else:
                    date_str = ""
                    timestamp = 0

                summary = strip_tags(entry.get("summary", ""))[:120]

                articles.append({
                    "title": html_module.escape(strip_tags(entry.get("title", "タイトルなし"))),
                    "url": html_module.escape(entry.get("link", "")),
                    "source": feed_info["name"],
                    "date": date_str,
                    "timestamp": timestamp,
                    "summary": html_module.escape(summary),
                })
        except Exception as e:
            print(f"Error fetching {feed_info['name']}: {e}")

    articles.sort(key=lambda x: x["timestamp"], reverse=True)
    return articles


def generate_html(articles):
    jst_offset = 9 * 3600
    updated_at = datetime.fromtimestamp(
        datetime.now(timezone.utc).timestamp() + jst_offset
    ).strftime("%Y年%-m月%-d日 %H:%M")
    sources = sorted(set(a["source"] for a in articles))

    article_html = ""
    for a in articles:
        color = SOURCE_COLORS.get(a["source"], {"bg": "#f0f0f0", "text": "#333"})
        summary_html = f'<p class="summary">{a["summary"]}</p>' if a["summary"] else ""
        article_html += f"""
    <article data-source="{a['source']}">
      <div class="meta">
        <span class="source-tag" style="background:{color['bg']};color:{color['text']}">{a['source']}</span>
        <span class="date">{a['date']}</span>
      </div>
      <h2><a href="{a['url']}" target="_blank" rel="noopener noreferrer">{a['title']}</a></h2>
      {summary_html}
    </article>"""

    filter_buttons = '<button class="filter-btn active" data-source="all">すべて</button>'
    for src in sources:
        color = SOURCE_COLORS.get(src, {"bg": "#f0f0f0", "text": "#333"})
        bg, text = color["bg"], color["text"]
        filter_buttons += f'<button class="filter-btn" data-source="{src}" style="--active-bg:{bg};--active-text:{text}">{src}</button>'

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Tech Report</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Hiragino Sans', 'Hiragino Kaku Gothic ProN', 'Noto Sans JP', sans-serif; background: #f5f5f5; color: #333; }}

  header {{ background: #fff; border-bottom: 2px solid #55c500; padding: 0 24px; height: 56px; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 0; z-index: 10; box-shadow: 0 1px 4px rgba(0,0,0,.06); }}
  .logo {{ font-size: 1.3rem; font-weight: 700; color: #55c500; letter-spacing: -0.5px; }}
  .updated {{ font-size: 0.72rem; color: #aaa; }}

  .filters {{ display: flex; flex-wrap: wrap; gap: 8px; padding: 14px 24px; background: #fff; border-bottom: 1px solid #e8e8e8; }}
  .filter-btn {{ background: #f5f5f5; border: 1px solid #ddd; color: #555; padding: 5px 14px; border-radius: 20px; cursor: pointer; font-size: 0.8rem; transition: all .15s; }}
  .filter-btn:hover {{ border-color: #55c500; color: #55c500; }}
  .filter-btn.active {{ background: #55c500; border-color: #55c500; color: #fff; }}

  main {{ max-width: 800px; margin: 24px auto; padding: 0 16px; display: flex; flex-direction: column; gap: 12px; }}

  article {{ background: #fff; border-radius: 8px; padding: 18px 20px; border: 1px solid #e8e8e8; transition: box-shadow .15s; }}
  article:hover {{ box-shadow: 0 2px 12px rgba(0,0,0,.08); }}

  .meta {{ display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }}
  .source-tag {{ font-size: 0.72rem; font-weight: 600; padding: 2px 10px; border-radius: 20px; }}
  .date {{ font-size: 0.75rem; color: #aaa; }}

  h2 {{ font-size: 1rem; font-weight: 700; line-height: 1.6; }}
  h2 a {{ color: #222; text-decoration: none; }}
  h2 a:hover {{ color: #55c500; }}

  .summary {{ font-size: 0.82rem; color: #777; margin-top: 6px; line-height: 1.65; }}

  @media (max-width: 600px) {{
    header {{ padding: 0 16px; }}
    .filters {{ padding: 10px 16px; }}
    main {{ margin: 16px auto; padding: 0 12px; }}
  }}
</style>
</head>
<body>
<header>
  <span class="logo">Tech Report</span>
  <span class="updated">更新: {updated_at} JST</span>
</header>
<div class="filters">{filter_buttons}</div>
<main id="articles">{article_html}</main>
<script>
  document.querySelectorAll('.filter-btn').forEach(btn => {{
    btn.addEventListener('click', () => {{
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const src = btn.dataset.source;
      document.querySelectorAll('article').forEach(a => {{
        a.style.display = (src === 'all' || a.dataset.source === src) ? '' : 'none';
      }});
    }});
  }});
</script>
</body>
</html>"""
    return html


if __name__ == "__main__":
    print("Fetching articles...")
    articles = fetch_articles()
    print(f"Fetched {len(articles)} articles")

    Path("docs").mkdir(exist_ok=True)
    html = generate_html(articles)
    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated docs/index.html")
