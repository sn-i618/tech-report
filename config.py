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
    "インフラ":       {"bg": "#e3f2fd", "text": "#1565c0"},
    "モバイル":       {"bg": "#f3e5f5", "text": "#6a1b9a"},
    "フロントエンド":  {"bg": "#fff8e1", "text": "#f57f17"},
    "AI/ML":        {"bg": "#e0f7fa", "text": "#00695c"},
    "セキュリティ":   {"bg": "#fce4ec", "text": "#b71c1c"},
}

TOPIC_SUPPORTED_SOURCES = {"Zenn", "Qiita"}
