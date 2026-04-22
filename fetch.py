import feedparser
import re
import html as html_module
from datetime import datetime, timezone, timedelta
from pathlib import Path

FEEDS = [
    # 総合
    {"name": "Zenn",           "url": "https://zenn.dev/feed",                              "topic": None},
    {"name": "Qiita",          "url": "https://qiita.com/popular-items/feed",               "topic": None},
    {"name": "はてなブックマーク",  "url": "https://b.hatena.ne.jp/hotentry/it.rss",            "topic": None},
    {"name": "gihyo.jp",       "url": "https://gihyo.jp/feed/rss2",                         "topic": None},
    {"name": "ITmedia",        "url": "https://rss.itmedia.co.jp/rss/2.0/news_bursts.xml",  "topic": None},
    # インフラ
    {"name": "Zenn",  "url": "https://zenn.dev/topics/infrastructure/feed", "topic": "インフラ"},
    {"name": "Zenn",  "url": "https://zenn.dev/topics/kubernetes/feed",     "topic": "インフラ"},
    {"name": "Qiita", "url": "https://qiita.com/tags/infrastructure/feed",  "topic": "インフラ"},
    {"name": "Qiita", "url": "https://qiita.com/tags/docker/feed",          "topic": "インフラ"},
    # モバイル
    {"name": "Zenn",  "url": "https://zenn.dev/topics/ios/feed",      "topic": "モバイル"},
    {"name": "Zenn",  "url": "https://zenn.dev/topics/android/feed",  "topic": "モバイル"},
    {"name": "Qiita", "url": "https://qiita.com/tags/ios/feed",       "topic": "モバイル"},
    {"name": "Qiita", "url": "https://qiita.com/tags/android/feed",   "topic": "モバイル"},
    # フロントエンド
    {"name": "Zenn",  "url": "https://zenn.dev/topics/frontend/feed",  "topic": "フロントエンド"},
    {"name": "Zenn",  "url": "https://zenn.dev/topics/react/feed",     "topic": "フロントエンド"},
    {"name": "Qiita", "url": "https://qiita.com/tags/frontend/feed",   "topic": "フロントエンド"},
    {"name": "Qiita", "url": "https://qiita.com/tags/typescript/feed", "topic": "フロントエンド"},
    # AI/ML
    {"name": "Zenn",  "url": "https://zenn.dev/topics/ai/feed",              "topic": "AI/ML"},
    {"name": "Zenn",  "url": "https://zenn.dev/topics/machinelearning/feed", "topic": "AI/ML"},
    {"name": "Qiita", "url": "https://qiita.com/tags/machinelearning/feed",  "topic": "AI/ML"},
    {"name": "Qiita", "url": "https://qiita.com/tags/ai/feed",               "topic": "AI/ML"},
    # セキュリティ
    {"name": "Zenn",  "url": "https://zenn.dev/topics/security/feed", "topic": "セキュリティ"},
    {"name": "Qiita", "url": "https://qiita.com/tags/security/feed",  "topic": "セキュリティ"},
]

ARTICLES_PER_FEED = 20

SOURCE_COLORS = {
    "Zenn":         {"bg": "#e8f5e9", "text": "#2e7d32"},
    "Qiita":        {"bg": "#e8f5e9", "text": "#55c500"},
    "はてなブックマーク": {"bg": "#fff3e0", "text": "#e65100"},
    "gihyo.jp":     {"bg": "#e3f2fd", "text": "#1565c0"},
    "ITmedia":      {"bg": "#fce4ec", "text": "#c62828"},
}

TOPIC_COLORS = {
    "インフラ":        {"bg": "#e3f2fd", "text": "#1565c0"},
    "モバイル":        {"bg": "#f3e5f5", "text": "#6a1b9a"},
    "フロントエンド":   {"bg": "#fff8e1", "text": "#f57f17"},
    "AI/ML":         {"bg": "#e0f7fa", "text": "#00695c"},
    "セキュリティ":    {"bg": "#fce4ec", "text": "#b71c1c"},
}

TOPIC_SUPPORTED_SOURCES = {"Zenn", "Qiita"}


def strip_tags(text):
    return re.sub(r"<[^>]+>", "", text or "").strip()


def fetch_articles():
    seen_urls = {}

    # トピックフィードを先に処理して優先させる
    ordered = sorted(FEEDS, key=lambda f: (f["topic"] is None))

    for feed_info in ordered:
        try:
            feed = feedparser.parse(feed_info["url"])
            for entry in feed.entries[:ARTICLES_PER_FEED]:
                url = entry.get("link", "")
                if not url:
                    continue

                published = entry.get("published_parsed") or entry.get("updated_parsed")
                if published:
                    dt = datetime(*published[:6], tzinfo=timezone.utc)
                    date_str = dt.strftime("%Y年%-m月%-d日")
                    timestamp = dt.timestamp()
                else:
                    date_str = ""
                    timestamp = 0

                if url not in seen_urls:
                    title   = strip_tags(entry.get("title", "タイトルなし"))
                    summary = strip_tags(entry.get("summary", ""))[:120]
                    seen_urls[url] = {
                        "title":     html_module.escape(title),
                        "url":       html_module.escape(url),
                        "source":    feed_info["name"],
                        "topic":     feed_info["topic"],
                        "date":      date_str,
                        "timestamp": timestamp,
                        "summary":   html_module.escape(summary),
                    }
        except Exception as e:
            print(f"Error fetching {feed_info['name']} ({feed_info['topic']}): {e}")

    articles = sorted(seen_urls.values(), key=lambda x: x["timestamp"], reverse=True)
    return articles


def generate_html(articles):
    JST = timezone(timedelta(hours=9))
    updated_at = datetime.now(JST).strftime("%Y年%-m月%-d日 %H:%M")

    sources = sorted(set(a["source"] for a in articles))
    topics = ["インフラ", "モバイル", "フロントエンド", "AI/ML", "セキュリティ"]

    article_html = ""
    for a in articles:
        sc = SOURCE_COLORS.get(a["source"], {"bg": "#f0f0f0", "text": "#333"})
        topic_badge = ""
        if a["topic"]:
            tc = TOPIC_COLORS.get(a["topic"], {"bg": "#f0f0f0", "text": "#333"})
            topic_badge = f'<span class="topic-tag" style="background:{tc["bg"]};color:{tc["text"]}">{a["topic"]}</span>'
        summary_html = f'<p class="summary">{a["summary"]}</p>' if a["summary"] else ""
        sbg, stext = sc["bg"], sc["text"]
        topic_val = a["topic"] or ""
        article_html += f"""
    <article data-source="{a['source']}" data-topic="{topic_val}">
      <div class="meta">
        <span class="source-tag" style="background:{sbg};color:{stext}">{a['source']}</span>
        {topic_badge}
        <span class="date">{a['date']}</span>
      </div>
      <h2><a href="{a['url']}" target="_blank" rel="noopener noreferrer">{a['title']}</a></h2>
      {summary_html}
    </article>"""

    source_btns = '<button class="filter-btn active" data-filter="source" data-value="all">すべて</button>'
    for src in sources:
        source_btns += f'<button class="filter-btn" data-filter="source" data-value="{src}">{src}</button>'

    topic_btns = '<button class="filter-btn active" data-filter="topic" data-value="all">すべて</button>'
    for t in topics:
        tc = TOPIC_COLORS[t]
        topic_btns += f'<button class="filter-btn" data-filter="topic" data-value="{t}" data-bg="{tc["bg"]}" data-text="{tc["text"]}">{t}</button>'

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Tech Report</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Hiragino Sans', 'Noto Sans JP', sans-serif; background: #f5f5f5; color: #333; }}

  header {{ background: #fff; border-bottom: 2px solid #55c500; padding: 0 24px; height: 56px; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 0; z-index: 10; box-shadow: 0 1px 4px rgba(0,0,0,.06); }}
  .logo {{ font-size: 1.3rem; font-weight: 700; color: #55c500; }}
  .updated {{ font-size: 0.72rem; color: #aaa; }}

  .filter-section {{ background: #fff; border-bottom: 1px solid #e8e8e8; padding: 10px 24px; display: flex; flex-direction: column; gap: 8px; }}
  .filter-label {{ font-size: 0.7rem; color: #aaa; font-weight: 600; }}
  .filter-row {{ display: flex; flex-wrap: wrap; gap: 6px; }}
  .filter-btn {{ background: #f5f5f5; border: 1px solid #ddd; color: #555; padding: 4px 12px; border-radius: 20px; cursor: pointer; font-size: 0.78rem; transition: all .15s; }}
  .filter-btn:hover {{ border-color: #55c500; color: #55c500; }}
  .filter-btn.active {{ background: #55c500; border-color: #55c500; color: #fff; }}
  .filter-btn[data-filter="topic"].active {{ background: var(--tc-bg, #55c500); border-color: var(--tc-bg, #55c500); color: var(--tc-text, #fff); filter: brightness(0.92); }}
  #topic-filters.disabled {{ opacity: 0.35; pointer-events: none; }}
  .filter-label.disabled {{ opacity: 0.35; }}

  main {{ max-width: 800px; margin: 20px auto; padding: 0 16px; display: flex; flex-direction: column; gap: 10px; }}

  article {{ background: #fff; border-radius: 8px; padding: 16px 20px; border: 1px solid #e8e8e8; transition: box-shadow .15s; }}
  article:hover {{ box-shadow: 0 2px 12px rgba(0,0,0,.08); }}

  .meta {{ display: flex; align-items: center; flex-wrap: wrap; gap: 6px; margin-bottom: 8px; }}
  .source-tag, .topic-tag {{ font-size: 0.7rem; font-weight: 600; padding: 2px 8px; border-radius: 20px; }}
  .date {{ font-size: 0.73rem; color: #aaa; margin-left: auto; }}

  h2 {{ font-size: 0.98rem; font-weight: 700; line-height: 1.6; }}
  h2 a {{ color: #222; text-decoration: none; }}
  h2 a:hover {{ color: #55c500; }}

  .summary {{ font-size: 0.81rem; color: #777; margin-top: 6px; line-height: 1.65; }}
  .no-result {{ text-align: center; color: #aaa; padding: 48px 0; font-size: 0.9rem; }}

  @media (max-width: 600px) {{
    header {{ padding: 0 16px; }}
    .filter-section {{ padding: 10px 16px; }}
    main {{ margin: 12px auto; padding: 0 10px; }}
  }}
</style>
</head>
<body>
<header>
  <span class="logo">Tech Report</span>
  <span class="updated">更新: {updated_at} JST</span>
</header>
<div class="filter-section">
  <div>
    <div class="filter-label">ソース</div>
    <div class="filter-row" id="source-filters">{source_btns}</div>
  </div>
  <div>
    <div class="filter-label" id="topic-label">トピック（Zenn・Qiita のみ対応）</div>
    <div class="filter-row" id="topic-filters">{topic_btns}</div>
  </div>
</div>
<main id="articles">{article_html}</main>
<p class="no-result" id="no-result" style="display:none">該当する記事がありません</p>
<script>
  const LS_SOURCE = 'tr_source';
  const LS_TOPIC  = 'tr_topic';
  const TOPIC_SOURCES = new Set(['all', 'Zenn', 'Qiita']);

  let selectedSource = localStorage.getItem(LS_SOURCE) || 'all';
  let selectedTopic  = localStorage.getItem(LS_TOPIC)  || 'all';

  function applyFilters() {{
    const articles = document.querySelectorAll('article');
    let visible = 0;
    articles.forEach(a => {{
      const srcMatch   = selectedSource === 'all' || a.dataset.source === selectedSource;
      const topicMatch = selectedTopic  === 'all' || a.dataset.topic  === selectedTopic;
      const show = srcMatch && topicMatch;
      a.style.display = show ? '' : 'none';
      if (show) visible++;
    }});
    document.getElementById('no-result').style.display = visible === 0 ? '' : 'none';
  }}

  function setActive(group, value) {{
    document.querySelectorAll(`#${{group}}-filters .filter-btn`).forEach(b => {{
      const isActive = b.dataset.value === value;
      b.classList.toggle('active', isActive);
      if (group === 'topic' && isActive && b.dataset.bg) {{
        b.style.setProperty('--tc-bg',   b.dataset.bg);
        b.style.setProperty('--tc-text', b.dataset.text);
      }}
    }});
  }}

  function updateTopicAvailability() {{
    const topicSupported = TOPIC_SOURCES.has(selectedSource);
    const topicRow   = document.getElementById('topic-filters');
    const topicLabel = document.getElementById('topic-label');
    topicRow.classList.toggle('disabled', !topicSupported);
    topicLabel.classList.toggle('disabled', !topicSupported);
    if (!topicSupported && selectedTopic !== 'all') {{
      selectedTopic = 'all';
      localStorage.setItem(LS_TOPIC, 'all');
      setActive('topic', 'all');
    }}
  }}

  setActive('source', selectedSource);
  setActive('topic',  selectedTopic);
  updateTopicAvailability();
  applyFilters();

  document.getElementById('source-filters').addEventListener('click', e => {{
    const btn = e.target.closest('.filter-btn');
    if (!btn) return;
    selectedSource = btn.dataset.value;
    localStorage.setItem(LS_SOURCE, selectedSource);
    setActive('source', selectedSource);
    updateTopicAvailability();
    applyFilters();
  }});

  document.getElementById('topic-filters').addEventListener('click', e => {{
    const btn = e.target.closest('.filter-btn');
    if (!btn) return;
    selectedTopic = btn.dataset.value;
    localStorage.setItem(LS_TOPIC, selectedTopic);
    setActive('topic', selectedTopic);
    applyFilters();
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
