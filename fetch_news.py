#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI News Auto-Fetcher
自动从多个RSS源采集AI新闻并更新news.json
"""

import feedparser
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# 设置输出编码为 UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# RSS新闻源配置
RSS_SOURCES = [
    {
        'name': 'OpenAI Blog',
        'url': 'https://openai.com/blog/rss.xml',
        'category': '模型发布'
    },
    {
        'name': 'Google AI Blog',
        'url': 'https://blog.google/technology/ai/rss/',
        'category': '科学研究'
    },
    {
        'name': 'DeepMind',
        'url': 'https://deepmind.google/discover/blog/rss/',
        'category': '科学研究'
    },
    {
        'name': 'Meta AI',
        'url': 'https://ai.meta.com/blog/rss/',
        'category': '开源社区'
    },
    {
        'name': 'Anthropic',
        'url': 'https://www.anthropic.com/index/rss',
        'category': 'AI安全'
    },
    {
        'name': 'MIT Technology Review AI',
        'url': 'https://www.technologyreview.com/feed/',
        'category': '行业动态'
    },
    {
        'name': 'VentureBeat AI',
        'url': 'https://venturebeat.com/ai/feed/',
        'category': '应用落地'
    },
]

# 关键词过滤（确保新闻与AI相关）
AI_KEYWORDS = [
    'AI', 'artificial intelligence', 'machine learning', 'deep learning',
    'neural network', 'GPT', 'LLM', 'language model', 'transformer',
    'computer vision', 'NLP', 'robotics', 'automation', 'chatbot',
    'Claude', 'OpenAI', 'Gemini', 'Llama', 'Diffusion', 'Stable Diffusion'
]

def is_ai_related(title, summary):
    """检查文章是否与AI相关"""
    text = f"{title} {summary}".lower()
    return any(keyword.lower() in text for keyword in AI_KEYWORDS)

def fetch_news_from_source(source, days_back=7, max_articles=3):
    """从单个RSS源获取新闻"""
    print(f"正在获取 {source['name']}...")

    try:
        feed = feedparser.parse(source['url'])
        articles = []
        cutoff_date = datetime.now() - timedelta(days=days_back)

        for entry in feed.entries[:max_articles * 2]:  # 获取更多以便筛选
            try:
                # 解析发布日期
                published = entry.get('published_parsed')
                if published:
                    pub_date = datetime(*published[:6])
                else:
                    pub_date = datetime.now()

                # 只获取最近的文章
                if pub_date < cutoff_date:
                    continue

                title = entry.get('title', '无标题')
                summary = entry.get('summary', entry.get('description', ''))

                # 清理HTML标签
                import re
                summary = re.sub('<[^<]+?>', '', summary)
                summary = summary[:200] + '...' if len(summary) > 200 else summary

                # 检查是否与AI相关
                if not is_ai_related(title, summary):
                    continue

                article = {
                    'title': title,
                    'summary': summary.strip(),
                    'source': source['name'],
                    'date': pub_date.strftime('%Y-%m-%d'),
                    'category': source['category'],
                    'url': entry.get('link', '#')
                }

                articles.append(article)

            except Exception as e:
                print(f"  解析文章时出错: {e}")
                continue

        print(f"  找到 {len(articles)} 篇相关文章")
        return articles[:max_articles]

    except Exception as e:
        print(f"  获取失败: {e}")
        return []

def remove_duplicates(articles):
    """移除重复文章（基于标题相似度）"""
    seen_titles = set()
    unique_articles = []

    for article in articles:
        title = article['title'].lower().strip()
        # 简单的去重逻辑
        if title not in seen_titles:
            seen_titles.add(title)
            unique_articles.append(article)

    return unique_articles

def sort_by_date(articles):
    """按日期排序（最新的在前）"""
    return sorted(articles, key=lambda x: x['date'], reverse=True)

def update_news_json(articles):
    """更新news.json文件"""
    script_dir = Path(__file__).parent
    news_file = script_dir / 'news.json'

    # 读取现有新闻
    existing_news = []
    if news_file.exists():
        with open(news_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            existing_news = data.get('news', [])

    # 合并新旧新闻，去重
    all_news = existing_news + articles
    unique_news = remove_duplicates(all_news)

    # 按日期排序并只保留最近30条
    sorted_news = sort_by_date(unique_news)
    latest_news = sorted_news[:30]

    # 生成新的news.json
    new_data = {
        'lastUpdated': datetime.now().strftime('%Y-%m-%d'),
        'news': latest_news
    }

    # 写入文件
    with open(news_file, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)

    print(f"\n✓ 已更新 news.json")
    print(f"  总文章数: {len(latest_news)}")
    print(f"  新增文章: {len(articles)}")
    print(f"  最新日期: {latest_news[0]['date'] if latest_news else 'N/A'}")

    return len(articles) > 0

def main():
    """主函数"""
    print("=" * 60)
    print("AI 新闻自动采集器")
    print("=" * 60)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"RSS源数量: {len(RSS_SOURCES)}")
    print()

    # 从所有源获取新闻
    all_articles = []
    for source in RSS_SOURCES:
        articles = fetch_news_from_source(source, days_back=7, max_articles=3)
        all_articles.extend(articles)

    print(f"\n总共获取 {len(all_articles)} 篇文章")

    # 更新news.json
    if all_articles:
        updated = update_news_json(all_articles)
        if updated:
            print("\n✓ 新闻更新成功！")
        else:
            print("\n- 没有新文章")
    else:
        print("\n✗ 未获取到任何新闻")

    print(f"\n结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

if __name__ == '__main__':
    main()
