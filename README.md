# AI+X社区

## 部署配置

### Vercel KV 配置

论坛功能需要 Vercel KV（Redis）存储。在 Vercel 项目中配置以下环境变量：

1. **KV_REST_API_URL** - Vercel KV 的 REST API URL
2. **KV_REST_API_TOKEN** - Vercel KV 的 REST API Token
3. **FORUM_ADMIN_TOKEN** - 管理员令牌（用于设置精华帖子）

### 配置步骤

1. 在 Vercel 项目设置中开通 KV
2. 复制 KV 的 REST API URL 和 Token
3. 在环境变量中添加上述三个变量
4. 重新部署项目

### 管理员功能

使用管理员令牌调用 `/api/forum-feature` API 设置精华帖子：

```bash
curl -X POST https://your-domain.com/api/forum-feature \
  -H "Content-Type: application/json" \
  -H "x-admin-token: YOUR_ADMIN_TOKEN" \
  -d '{"id": "post_id", "featured": true}'
```

# 日志
- [x] 2026年1月，用cc进行AI+X 1.0社区的构造，纯网页。
- [x] 2026年1-15日，用cursor沉淀AI+X 1.0的历史数据。
- [x] 1-15，沉淀之前的知识库到网站中。
- [x] 1-15，增加【我是昭阳】。
- [x] 1-15，凌晨6点，复活【AI信息流】，在实验室服务器。
- [x] 1-15，增加网站的最下面的AI资源链接。
- [x] 1-15，优化界面设计和跳转相应逻辑。ps：等后续写完论文，提交后可以一周的时间做个前后端的论坛出来。
- [x] 1-15，增加AI论坛的功能。
- [x] 1-15，添加英文版的支持。想起michael说的这句话。AI和出海，是这个时代的两大杠杆。
- [x] 2026-01-15，论坛升级：从 localStorage 升级为 Vercel KV 存储，支持多人共享、最新/最热/精华排序、点赞功能。
- [x] 1-16，让claude code（cc）给我的网页写个chatbot，调用智谱的免费的api。
- [x] 1-16，namesilio买了个1年的域名: xpg.one。感觉AI和出海似乎是未来的大趋势呀。https://www.aixpg.one/
- [x] 1-19，发现我的cc免费7天，到1月21日过期，因此多用起来它
- [x] 1-29，现在我用飞书写博客，挂载在网站。同时，手机端的ima。也复活了。
- [x] 1-30，开始复活使用我的苹果电脑。