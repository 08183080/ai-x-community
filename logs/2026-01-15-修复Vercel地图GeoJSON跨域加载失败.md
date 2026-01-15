# 2026-01-15 修复Vercel地图GeoJSON跨域加载失败

## 现象
- 在 Vercel 上打开 `jianghu.html` 提示“地图数据加载失败”。

## 原因判断
- 浏览器直连第三方 GeoJSON（`geo.datav.aliyun.com`）可能被 CORS/网络策略拦截。

## 修复
- 新增同域代理接口：`/api/geo?adcode=xxxxxx`
  - 服务端抓取阿里 datav 的 GeoJSON，并返回给前端（避免浏览器跨域限制）。
- `jianghu.html` 优先从 `/api/geo` 拉取地图数据；外网直连作为兜底。
- 失败时在页面右上角输出更具体的错误信息（含 HTTP 状态码/URL）。

## 自检方法
- 部署后访问：`/api/geo?adcode=100000` 应返回中国 GeoJSON。

