import feedparser
import re
import html as html_module
from datetime import datetime, timezone

from config import FEEDS, ARTICLES_PER_FEED


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

    return sorted(seen_urls.values(), key=lambda x: x["timestamp"], reverse=True)
