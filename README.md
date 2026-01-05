# AI+X 社区网站 - 使用说明

## 功能特性

- **01代码雨背景** - 经典的《黑客帝国》风格动画效果
- **极简设计** - 纯黑背景配合绿色主题色
- **AI每日新闻** - 动态加载和展示AI行业新闻
- **响应式布局** - 完美适配移动端和桌面端
- **新闻编辑器** - 方便管理和更新新闻内容

## 文件说明

- `index.html` - 主网站页面
- `news.json` - 新闻数据存储文件
- `news-editor.html` - 新闻管理编辑器
- `README.md` - 本说明文件

## ⚠️ 重要提示：本地运行

由于浏览器的CORS安全策略，**不能直接双击打开HTML文件**来查看新闻功能。你需要通过本地服务器运行。

### 方法一：使用Python（推荐）

如果你安装了Python，打开命令行，进入网站目录，运行：

**Python 3.x:**
```bash
python -m http.server 8000
```

**Python 2.x:**
```bash
python -m SimpleHTTPServer 8000
```

然后在浏览器中访问：`http://localhost:8000`

### 方法二：使用Node.js

```bash
npx http-server -p 8000
```

### 方法三：使用VS Code

安装"Live Server"插件，右键点击index.html选择"Open with Live Server"

### 方法四：使用其他本地服务器

任何可以提供静态文件服务的Web服务器都可以（Apache、Nginx等）

## 新闻管理

### 添加新闻

1. 打开 `news-editor.html`（通过本地服务器）
2. 填写新闻表单：
   - 标题：新闻标题
   - 摘要：新闻内容摘要
   - 来源：新闻来源
   - 分类：选择合适的分类
   - URL：可选的新闻链接
3. 点击"ADD ARTICLE"添加
4. 下载生成的news.json文件并替换原文件

### 编辑/删除新闻

1. 在编辑器页面查看现有文章列表
2. 点击"EDIT"编辑文章
3. 点击"DELETE"删除文章
4. 更新后会自动下载新的news.json文件

## 新闻数据格式

`news.json` 文件格式示例：

```json
{
  "lastUpdated": "2025-01-05",
  "news": [
    {
      "id": 1,
      "title": "新闻标题",
      "summary": "新闻摘要...",
      "source": "来源",
      "date": "2025-01-05",
      "category": "模型发布",
      "url": "https://..."
    }
  ]
}
```

## 自定义配置

### 修改主题颜色

在 `index.html` 中，将 `#00ff00` 替换为你想要的颜色值

### 修改代码雨速度

在 `index.html` 的JavaScript部分，修改 `setInterval(draw, 33)` 中的数字（毫秒）

### 添加新的新闻分类

在 `news-editor.html` 的分类选择框中添加新选项

## 浏览器兼容性

- Chrome/Edge (推荐)
- Firefox
- Safari
- 需要支持ES6+语法

## 故障排除

**问题：新闻显示"Loading..."或不显示**
- 确保通过本地服务器运行，而不是直接打开文件
- 检查news.json文件是否与index.html在同一目录
- 打开浏览器开发者工具（F12）查看错误信息

**问题：代码雨不显示**
- 确保JavaScript已启用
- 检查浏览器控制台是否有错误

**问题：编辑器无法保存**
- 由于浏览器安全限制，需要手动下载并替换news.json文件
- 或者使用支持本地文件写入的后端服务

## 部署到线上

可以直接部署到任何静态网站托管服务：
- GitHub Pages
- Netlify
- Vercel
- Cloudflare Pages

只需要将所有文件上传即可正常工作。

## 技术栈

- HTML5
- CSS3
- Vanilla JavaScript (无依赖)
- Canvas API

## 许可证

MIT License

---

**AI+X Community** - Where Innovation Meets Intelligence
