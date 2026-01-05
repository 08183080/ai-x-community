# AI 新闻自动更新系统

## 系统概述

这个系统每天自动从多个权威 AI 新闻源采集最新资讯，自动更新到你的网站。

**工作流程：**
1. **GitHub Actions** 每天自动运行（北京时间 09:00）
2. **fetch_news.py** 从 RSS 源采集最新新闻
3. 自动更新 `news.json` 文件
4. 提交更新到 GitHub 仓库
5. **Vercel** 检测到更新后自动重新部署

## 已配置的新闻源

- ✅ OpenAI Blog
- ✅ Google AI Blog
- ✅ DeepMind
- ✅ Meta AI
- ✅ Anthropic
- ✅ MIT Technology Review
- ✅ VentureBeat AI

## 使用方法

### 方法一：自动运行（推荐）

**完全自动，无需任何操作！**

系统会在每天北京时间 09:00 自动运行，采集最新新闻并更新网站。

### 方法二：手动触发更新

1. 访问 GitHub 仓库：https://github.com/08183080/ai-x-community
2. 点击 **"Actions"** 标签
3. 选择 **"Auto Fetch AI News"** 工作流
4. 点击 **"Run workflow"** 按钮
5. 确认运行

### 方法三：本地手动运行

```bash
# 安装依赖
pip install feedparser

# 运行脚本
python fetch_news.py
```

## 自定义配置

### 修改更新时间

编辑 `.github/workflows/fetch-news.yml`:

```yaml
schedule:
  # 每天 UTC 时间 01:00 (北京时间 09:00)
  - cron: '0 1 * * *'
```

Cron 格式说明：
- `0 1 * * *` = 每天 01:00 UTC = 北京时间 09:00
- `0 */6 * * *` = 每 6 小时一次
- `0 2 * * 1-5` = 工作日凌晨 2 点

### 添加新的新闻源

编辑 `fetch_news.py` 中的 `RSS_SOURCES` 列表：

```python
RSS_SOURCES = [
    {
        'name': '新闻源名称',
        'url': 'https://example.com/rss',
        'category': '分类'
    },
    # 添加更多源...
]
```

### 调整关键词过滤

编辑 `fetch_news.py` 中的 `AI_KEYWORDS` 列表，添加或删除关键词。

### 修改新闻数量限制

在 `fetch_news.py` 中调整：

```python
fetch_news_from_source(source, days_back=7, max_articles=3)
#                                       ↑          ↑
#                                    获取天数   每源文章数
```

## 监控和调试

### 查看运行日志

1. 访问 GitHub 仓库
2. 点击 **"Actions"** 标签
3. 点击最近的工作流运行记录
4. 查看详细日志

### 常见问题

**Q: 为什么没有新新闻？**
- 可能是新闻源没有更新
- RSS 订阅可能失效
- 关键词过滤太严格

**Q: 如何手动测试？**
```bash
# 本地运行
python fetch_news.py

# 或在 GitHub 手动触发工作流
```

**Q: Vercel 没有自动更新？**
- 检查 Vercel 是否连接到 GitHub
- 确认 Vercel 的 Git 集成已启用
- 查看 Vercel 部署日志

## 技术细节

### 文件结构

```
.
├── fetch_news.py              # 新闻采集脚本
├── news.json                  # 新闻数据（自动更新）
├── .github/
│   └── workflows/
│       └── fetch-news.yml     # GitHub Actions 配置
├── index.html                 # 主页（读取 news.json）
└── NEWS-AUTOMATION-GUIDE.md   # 本文件
```

### 数据格式

`news.json` 格式：

```json
{
  "lastUpdated": "2025-01-05",
  "news": [
    {
      "title": "文章标题",
      "summary": "文章摘要...",
      "source": "新闻源",
      "date": "2025-01-05",
      "category": "分类",
      "url": "https://..."
    }
  ]
}
```

## 进阶功能

### 发送通知（可选）

可以在 GitHub Actions 中添加通知步骤，例如：
- 发送邮件
- 推送 Telegram 消息
- 发送 Slack 通知

### 多语言支持

修改脚本以采集多语言新闻：
- 中文：36kr、虎嗅等
- 日语：日本 AI 博客
- 其他语言

### 内容过滤增强

添加更智能的内容过滤：
- 按重要性评分
- 过滤广告内容
- 去重算法优化

## 维护建议

1. **定期检查新闻源**：每季度检查 RSS 源是否有效
2. **优化关键词**：根据采集结果调整过滤规则
3. **监控运行状态**：每周查看 Actions 日志
4. **备份数据**：定期备份 `news.json`

## 支持与反馈

如有问题或建议，请：
1. 查看 GitHub Issues
2. 检查 Actions 日志
3. 联系维护者

---

**Enjoy automated AI news! 🤖**
