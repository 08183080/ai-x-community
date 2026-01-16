#!/usr/bin/env python3
"""
AI+X Website Local Server
简单的本地HTTP服务器，用于运行AI+X社区网站
"""

import http.server
import socketserver
import webbrowser
import os
import sys
import json
import urllib.parse
import urllib.request
import mimetypes

PORT = 8000

def scan_directory(path, base_path=''):
    """递归扫描目录，返回文件列表"""
    result = []
    try:
        items = sorted(os.listdir(path))
        for item in items:
            item_path = os.path.join(path, item)
            rel_path = os.path.join(base_path, item).replace('\\', '/')
            
            if os.path.isdir(item_path):
                children = scan_directory(item_path, rel_path)
                result.append({
                    'type': 'folder',
                    'name': item,
                    'path': rel_path,
                    'children': children
                })
            else:
                ext = os.path.splitext(item)[1][1:].lower() if '.' in item else ''
                result.append({
                    'type': 'file',
                    'name': item,
                    'path': rel_path,
                    'ext': ext
                })
    except PermissionError:
        pass
    return result

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path_only = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        def send_json(code, obj):
            self.send_response(code)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(obj, ensure_ascii=False).encode('utf-8'))

        # API端点：扫描文件目录（历史数据）
        if path_only == '/api/files':
            data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'AI+X_history_data')
            if os.path.exists(data_dir):
                files = scan_directory(data_dir, 'AI+X_history_data')
                send_json(200, files)
            else:
                send_json(404, {'error': 'Directory not found'})
            return

        # API端点：代理读取文件（对齐 Vercel 的 /api/file）
        if path_only == '/api/file':
            raw_path = query.get('path', [''])[0]
            if not raw_path:
                return send_json(400, {'error': 'Missing path parameter'})
            decoded = urllib.parse.unquote(raw_path)
            if decoded.startswith('/'):
                decoded = decoded[1:]

            base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'AI+X_history_data')
            if not os.path.exists(base_dir):
                return send_json(404, {'error': 'Data directory not found'})

            rel = decoded.replace('AI+X_history_data/', '')
            full_path = os.path.join(base_dir, rel)
            resolved = os.path.realpath(full_path)
            allowed = os.path.realpath(base_dir)
            if not resolved.startswith(allowed):
                return send_json(403, {'error': 'Access denied'})
            if not os.path.exists(full_path) or not os.path.isfile(full_path):
                return send_json(404, {'error': 'File not found', 'path': decoded})

            ctype, _ = mimetypes.guess_type(full_path)
            if not ctype:
                ext = os.path.splitext(full_path)[1].lower()
                ctype = 'application/octet-stream' if ext else 'application/octet-stream'
            self.send_response(200)
            self.send_header('Content-Type', ctype)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            with open(full_path, 'rb') as f:
                self.wfile.write(f.read())
            return

        # API端点：扫描城市图片（对齐 Vercel 的 /api/city-photos）
        if path_only == '/api/city-photos':
            base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'AI+X_history_data', '地图')
            if not os.path.exists(base_dir):
                return send_json(404, {'error': 'Directory not found', 'tried': [base_dir]})
            out = {}
            for city in sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]):
                city_dir = os.path.join(base_dir, city)
                photos = []
                for fn in sorted(os.listdir(city_dir)):
                    low = fn.lower()
                    if low.endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):
                        rel = f"AI+X_history_data/地图/{city}/{fn}"
                        photos.append({'src': f"/api/file?path={urllib.parse.quote(rel)}", 'title': os.path.splitext(fn)[0]})
                if photos:
                    out[city] = {'title': city, 'note': '', 'photos': photos}
            return send_json(200, out)

        # API端点：地图 GeoJSON 代理（对齐 Vercel 的 /api/geo）
        if path_only == '/api/geo':
            adcode = ''.join([c for c in query.get('adcode', ['100000'])[0] if c.isdigit()]) or '100000'
            url = f"https://geo.datav.aliyun.com/areas_v3/bound/{adcode}_full.json"
            try:
                with urllib.request.urlopen(url, timeout=10) as resp:
                    data = resp.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Cache-Control', 'no-store')
                self.end_headers()
                self.wfile.write(data)
            except Exception as e:
                return send_json(502, {'error': 'fetch_failed', 'url': url, 'message': str(e)})
            return
        
        # 默认文件服务
        super().do_GET()
    
    def end_headers(self):
        # 添加CORS头，允许本地加载JSON文件
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

def start_server():
    # 切换到脚本所在目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # 尝试绑定端口，如果被占用则自动尝试下一个
    port = PORT
    while True:
        try:
            httpd = socketserver.TCPServer(("127.0.0.1", port), MyHTTPRequestHandler)
            break
        except OSError:
            if port == PORT:
                print(f"Port {port} is in use, trying next port...")
            port += 1
            if port > PORT + 100:
                print(f"[ERROR] Failed to find available port after {PORT}-{port-1}")
                sys.exit(1)
    
    with httpd:
        print("=" * 60)
        print("     AI+X Community - Local Server")
        print("=" * 60)
        print(f"\n✓ Server started successfully!")
        print(f"✓ Running at: http://localhost:{port}")
        print(f"✓ Press Ctrl+C to stop the server\n")
        print("=" * 60)
        print("\nAvailable pages:")
        print(f"  • Main site:  http://localhost:{port}/index.html")
        print("\n" + "=" * 60 + "\n")

        # 自动打开浏览器
        try:
            webbrowser.open(f'http://localhost:{port}/index.html')
        except:
            pass

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✓ Server stopped.")
            sys.exit(0)

if __name__ == "__main__":
    start_server()
