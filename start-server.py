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
        # API端点：扫描文件目录
        if self.path == '/api/files':
            data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'AI+X_history_data')
            if os.path.exists(data_dir):
                files = scan_directory(data_dir, 'AI+X_history_data')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(files, ensure_ascii=False).encode('utf-8'))
            else:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Directory not found'}).encode('utf-8'))
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
