# AI+X 社区网站 - 使用说明

## 功能特性

- **01代码雨背景** - 经典的《黑客帝国》风格动画效果，采用优化的性能实现
- **现代深色科技风格** - 深色渐变背景配合绿色主题色，营造科技感氛围
- **玻璃态设计** - 使用毛玻璃效果（glassmorphism）增强视觉层次感
- **流畅动画效果** - 平滑的过渡动画和微交互，提升用户体验
- **响应式布局** - 完美适配移动端、平板和桌面端
- **谢苹果故事** - 点击右上角苹果图标查看社区创始人的传奇故事

## 设计亮点

### 视觉设计
- **渐变色彩方案**：从纯绿色调整为渐变绿色系（`#00ff88` → `#00d4ff`）
- **玻璃态元素**：使用 `backdrop-filter: blur()` 实现半透明毛玻璃效果
- **动态交互**：卡片悬停效果、按钮涟漪动画、滚动淡入动画
- **发光效果**：文字和边框的柔和发光，增强科技感

### 技术实现
- **CSS变量系统**：统一管理颜色、尺寸和过渡效果
- **模块化JavaScript**：代码雨、模态框、滚动动画独立模块
- **性能优化**：使用 `requestAnimationFrame` 优化动画性能
- **可访问性**：支持键盘导航、ARIA标签、减少动画偏好

## 文件说明

- `index.html` - 主网站页面（包含所有样式和脚本）
- `start-server.py` - 本地开发服务器
- `start.bat` - Windows快速启动脚本
- `vercel.json` - Vercel部署配置
- `README.md` - 本说明文件

## ⚠️ 重要提示：本地运行

由于浏览器的CORS安全策略，**不能直接双击打开HTML文件**。你需要通过本地服务器运行。

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

安装"Live Server"插件，右键点击 `index.html` 选择"Open with Live Server"

### 方法四：使用Windows批处理文件

双击 `start.bat` 文件（如果存在）

### 方法五：使用其他本地服务器

任何可以提供静态文件服务的Web服务器都可以（Apache、Nginx等）

## 自定义配置

### 修改主题颜色

在 `index.html` 的 `<style>` 标签中，修改 CSS 变量：

```css
:root {
    --primary-color: #00ff88;      /* 主色调 */
    --accent-color: #00d4ff;       /* 强调色 */
    --bg-gradient-start: #0a0a0a;  /* 背景渐变起始 */
    --bg-gradient-end: #1a1a2e;    /* 背景渐变结束 */
}
```

### 修改代码雨速度

在 JavaScript 的代码雨模块中，修改配置对象：

```javascript
const config = {
    speed: 33,  // 毫秒，数值越小速度越快
    fontSize: 14,  // 字体大小
    resetProbability: 0.975  // 重置概率
};
```

### 调整玻璃态效果

修改 CSS 变量中的玻璃态相关值：

```css
:root {
    --glass-bg: rgba(255, 255, 255, 0.05);  /* 背景透明度 */
    --glass-border: rgba(0, 255, 136, 0.2); /* 边框透明度 */
}
```

## 浏览器兼容性

- ✅ Chrome/Edge (推荐) - 完全支持
- ✅ Firefox - 完全支持
- ✅ Safari - 完全支持（需要 Safari 9+）
- ⚠️ 需要支持 ES6+ 语法和 CSS3 特性
- ⚠️ `backdrop-filter` 需要现代浏览器支持

### 特性支持
- CSS变量（Custom Properties）
- `backdrop-filter`（毛玻璃效果）
- `requestAnimationFrame`（动画优化）
- Intersection Observer API（滚动动画）

## 响应式断点

- **移动端**：`< 768px` - 单列布局，优化触摸交互
- **平板**：`768px - 1024px` - 自适应网格布局
- **桌面**：`> 1024px` - 完整多列布局

## 故障排除

**问题：代码雨不显示**
- 确保JavaScript已启用
- 检查浏览器控制台是否有错误
- 确认Canvas API支持

**问题：玻璃态效果不显示**
- 检查浏览器是否支持 `backdrop-filter`
- Chrome/Edge/Safari 需要较新版本
- Firefox 需要启用 `layout.css.backdrop-filter.enabled`（实验性功能）

**问题：动画不流畅**
- 检查设备性能
- 尝试在浏览器中禁用硬件加速
- 检查是否有其他扩展影响性能

**问题：移动端显示异常**
- 确保 `viewport` meta 标签正确设置
- 检查CSS媒体查询是否正确
- 清除浏览器缓存

## 部署到线上

可以直接部署到任何静态网站托管服务：

- **GitHub Pages** - 免费，适合开源项目
- **Netlify** - 免费，自动部署
- **Vercel** - 免费，快速部署（已包含配置文件）
- **Cloudflare Pages** - 免费，全球CDN

只需要将所有文件上传即可正常工作。无需后端服务器。

## 技术栈

- **HTML5** - 语义化标签，可访问性支持
- **CSS3** - 变量系统、玻璃态效果、动画
- **Vanilla JavaScript** - 无依赖，模块化代码
- **Canvas API** - 代码雨动画
- **Intersection Observer API** - 滚动动画

## 性能优化

- 使用 `requestAnimationFrame` 优化动画性能
- 减少DOM操作，使用CSS动画替代JavaScript动画
- 使用CSS变量减少重复代码
- 模块化JavaScript代码，按需加载
- 响应式图片和媒体查询优化

## 可访问性

- 语义化HTML标签（`<main>`, `<section>`, `<article>`, `<footer>`）
- ARIA标签支持（`role`, `aria-label`, `aria-modal`）
- 键盘导航支持（ESC键关闭模态框）
- 减少动画偏好支持（`prefers-reduced-motion`）
- 足够的颜色对比度

## 许可证

MIT License

---

**AI+X Community** - Where Innovation Meets Intelligence
