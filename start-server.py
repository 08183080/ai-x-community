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

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 添加CORS头，允许本地加载JSON文件
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

def start_server():
    # 切换到脚本所在目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # 创建服务器
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print("=" * 60)
        print("     AI+X Community - Local Server")
        print("=" * 60)
        print(f"\n✓ Server started successfully!")
        print(f"✓ Running at: http://localhost:{PORT}")
        print(f"✓ Press Ctrl+C to stop the server\n")
        print("=" * 60)
        print("\nAvailable pages:")
        print(f"  • Main site:  http://localhost:{PORT}/index.html")
        print(f"  • News editor: http://localhost:{PORT}/news-editor.html")
        print("\n" + "=" * 60 + "\n")

        # 自动打开浏览器
        try:
            webbrowser.open(f'http://localhost:{PORT}/index.html')
        except:
            pass

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✓ Server stopped.")
            sys.exit(0)

if __name__ == "__main__":
    start_server()
