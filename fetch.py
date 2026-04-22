import feedparser
import json
import os
from datetime import datetime, timezone
from pathlib import Path

FEEDS = [
    {"name": "Hacker News", "url": "https://news.ycombinator.com/rss"},
    {"name": "Zenn", "url": "https://zenn.dev/feed"},
    {"name": "Qiita", "url": "https://qiita.com/popular-items/feed"},
    {"name": "dev.to", "url": "https://dev.to/feed"},
    {"name": "The Verge Tech", "url": "https://www.theverge.com/tech/rss/index.xml"},
]

ARTICLES_PER_FEED = 20


def fetch_articles():
    articles = []
    for feed_info in FEEDS:
        try:
            feed = feedparser.parse(feed_info["url"])
            for entry in feed.entries[:ARTICLES_PER_FEED]:
                published = entry.get("published_parsed") or entry.get("updated_parsed")
                if published:
                    dt = datetime(*published[:6], tzinfo=timezone.utc)
                    date_str = dt.strftime("%Y-%m-%d %H:%M")
                    timestamp = dt.timestamp()
                else:
                    date_str = ""
                    timestamp = 0

                articles.append({
                    "title": entry.get("title", "No title"),
                    "url": entry.get("link", ""),
                    "source": feed_info["name"],
                    "date": date_str,
                    "timestamp": timestamp,
                    "summary": entry.get("summary", "")[:200],
                })
        except Exception as e:
            print(f"Error fetching {feed_info['name']}: {e}")

    articles.sort(key=lambda x: x["timestamp"], reverse=True)
    return articles


def generate_html(articles):
    updated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    sources = sorted(set(a["source"] for a in articles))

    article_html = ""
    for a in articles:
        summary = f'<p class="summary">{a["summary"]}</p>' if a["summary"] else ""
        article_html += f"""
        <article data-source="{a['source']}">
            <div class="meta">
                <span class="source">{a['source']}</span>
                <span class="date">{a['date']}</span>
            </div>
            <h2><a href="{a['url']}" target="_blank" rel="noopener">{a['title']}</a></h2>
            {summary}
        </article>"""

    filter_buttons = '<button class="filter-btn active" data-source="all">All</button>'
    for src in sources:
        filter_buttons += f'<button class="filter-btn" data-source="{src}">{src}</button>'

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Tech Report</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0f0f0f; color: #e0e0e0; }}
  header {{ background: #1a1a1a; border-bottom: 1px solid #333; padding: 16px 24px; position: sticky; top: 0; z-index: 10; }}
  header h1 {{ font-size: 1.4rem; color: #fff; margin-bottom: 8px; }}
  .updated {{ font-size: 0.75rem; color: #888; }}
  .filters {{ display: flex; flex-wrap: wrap; gap: 8px; padding: 16px 24px; background: #141414; border-bottom: 1px solid #2a2a2a; }}
  .filter-btn {{ background: #2a2a2a; border: 1px solid #444; color: #ccc; padding: 4px 12px; border-radius: 16px; cursor: pointer; font-size: 0.8rem; }}
  .filter-btn:hover, .filter-btn.active {{ background: #3b82f6; border-color: #3b82f6; color: #fff; }}
  main {{ max-width: 860px; margin: 0 auto; padding: 16px 24px; }}
  article {{ border-bottom: 1px solid #222; padding: 16px 0; }}
  article:last-child {{ border-bottom: none; }}
  .meta {{ display: flex; gap: 12px; margin-bottom: 6px; }}
  .source {{ font-size: 0.75rem; background: #1e3a5f; color: #60a5fa; padding: 2px 8px; border-radius: 4px; }}
  .date {{ font-size: 0.75rem; color: #666; }}
  h2 {{ font-size: 1rem; font-weight: 500; line-height: 1.5; }}
  h2 a {{ color: #e0e0e0; text-decoration: none; }}
  h2 a:hover {{ color: #60a5fa; }}
  .summary {{ font-size: 0.82rem; color: #888; margin-top: 6px; line-height: 1.5; }}
</style>
</head>
<body>
<header>
  <h1>Tech Report</h1>
  <div class="updated">Last updated: {updated_at}</div>
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
