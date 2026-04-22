from pathlib import Path

from fetcher import fetch_articles
from renderer import generate_html

if __name__ == "__main__":
    print("Fetching articles...")
    articles = fetch_articles()
    print(f"Fetched {len(articles)} articles")

    Path("docs").mkdir(exist_ok=True)
    html = generate_html(articles)
    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated docs/index.html")
