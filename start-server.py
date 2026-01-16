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
import hashlib
import secrets
import time
import threading
import sqlite3

PORT = 8000
JWT_SECRET = 'local-dev-secret-key-change-in-production'

# 简单的用户数据库（使用 SQLite）
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'local_users.db')

def init_db():
    """初始化用户数据库"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE,
            password TEXT NOT NULL,
            created_at TEXT NOT NULL,
            last_login_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    """简单的密码哈希（用于本地开发测试）"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_jwt(user_id, username):
    """生成简单的 JWT token（用于本地开发测试）"""
    header = json.dumps({'alg': 'HS256', 'typ': 'JWT'})
    payload = json.dumps({'userId': user_id, 'username': username, 'exp': int(time.time()) + 7 * 24 * 3600})
    header_b64 = base64_url_encode(header.encode())
    payload_b64 = base64_url_encode(payload.encode())
    signature = hashlib.sha256(f"{header_b64}.{payload_b64}.{JWT_SECRET}".encode()).hexdigest()
    return f"{header_b64}.{payload_b64}.{signature}"

def base64_url_encode(data):
    """Base64 URL 编码"""
    import base64
    return base64.b64encode(data).decode().replace('+', '-').replace('/', '_').rstrip('=')

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
    def do_OPTIONS(self):
        """处理 CORS 预检请求"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

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

        # API端点：获取论坛帖子列表
        if path_only == '/api/forum-posts':
            # 本地开发环境返回空列表（因为没有持久化存储）
            return send_json(200, [])

        # 默认文件服务
        super().do_GET()

    def do_POST(self):
        """处理 POST 请求"""
        parsed = urllib.parse.urlparse(self.path)
        path_only = parsed.path

        # 认证 API 端点
        if path_only in ['/api/auth/register', '/api/auth/login', '/api/auth/logout', '/api/auth/me']:
            return handle_auth_request(self, path_only)

        # 论坛发帖 API 端点
        if path_only == '/api/forum-posts':
            return handle_forum_post(self)

        # 论坛点赞 API 端点
        if path_only == '/api/forum-vote':
            return handle_forum_vote(self)

        # 不支持的端点
        send_json(404, {'error': 'Not found'})
        return

    def end_headers(self):
        # 添加CORS头，允许本地加载JSON文件
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

def handle_auth_request(handler, path):
    """处理认证相关请求"""
    def send_json(code, obj):
        handler.send_response(code)
        handler.send_header('Content-Type', 'application/json; charset=utf-8')
        handler.send_header('Access-Control-Allow-Origin', '*')
        handler.send_header('Access-Control-Allow-Credentials', 'true')
        handler.end_headers()
        handler.wfile.write(json.dumps(obj, ensure_ascii=False).encode('utf-8'))

    # 获取请求体
    content_length = int(handler.headers.get('Content-Length', 0))
    body = handler.rfile.read(content_length).decode('utf-8')

    try:
        data = json.loads(body) if body else {}
    except json.JSONDecodeError:
        data = {}

    # 打印调试信息
    import sys
    print(f"[AUTH] {path} request data: {data}", file=sys.stderr)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    try:
        if path == '/api/auth/register':
            # 用户注册
            username = data.get('username', '').strip()
            password = data.get('password', '')
            email = data.get('email', '').strip()

            # 验证输入
            if not username or not password:
                return send_json(400, {'error': '用户名和密码不能为空'})
            if len(username) < 3 or len(username) > 20:
                return send_json(400, {'error': '用户名长度必须在 3-20 个字符之间'})
            if len(password) < 6:
                return send_json(400, {'error': '密码长度必须至少 6 个字符'})

            # 检查用户名是否已存在
            c.execute('SELECT id FROM users WHERE username = ?', (username,))
            if c.fetchone():
                return send_json(400, {'error': '用户名已存在'})

            # 检查邮箱是否已存在
            if email:
                c.execute('SELECT id FROM users WHERE email = ?', (email,))
                if c.fetchone():
                    return send_json(400, {'error': '邮箱已被注册'})

            # 创建用户
            user_id = f"user_{int(time.time() * 1000)}_{secrets.token_hex(4)}"
            hashed_password = hash_password(password)
            # 使用 datetime 而不是 time.strftime（Windows 不支持 %f）
            from datetime import datetime
            created_at = datetime.utcnow().isoformat() + 'Z'

            c.execute('''
                INSERT INTO users (id, username, email, password, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, username, email if email else None, hashed_password, created_at))
            conn.commit()

            # 生成 token
            token = generate_jwt(user_id, username)

            return send_json(201, {
                'message': '注册成功',
                'token': token,
                'user': {
                    'id': user_id,
                    'username': username,
                    'email': email,
                    'createdAt': created_at
                }
            })

        elif path == '/api/auth/login':
            # 用户登录
            username = data.get('username', '').strip()
            password = data.get('password', '')

            if not username or not password:
                return send_json(400, {'error': '用户名和密码不能为空'})

            # 查找用户
            c.execute('SELECT id, username, email, password, created_at FROM users WHERE username = ?', (username,))
            user = c.fetchone()

            if not user or user[3] != hash_password(password):
                return send_json(401, {'error': '用户名或密码错误'})

            user_id, username, email, _, created_at = user

            # 更新最后登录时间
            from datetime import datetime
            last_login_at = datetime.utcnow().isoformat() + 'Z'
            c.execute('UPDATE users SET last_login_at = ? WHERE id = ?', (last_login_at, user_id))
            conn.commit()

            # 生成 token
            token = generate_jwt(user_id, username)

            return send_json(200, {
                'message': '登录成功',
                'token': token,
                'user': {
                    'id': user_id,
                    'username': username,
                    'email': email,
                    'createdAt': created_at,
                    'lastLoginAt': last_login_at
                }
            })

        elif path == '/api/auth/logout':
            # 用户登出
            auth_header = handler.headers.get('Authorization', '')
            if not auth_header.startswith('Bearer '):
                return send_json(401, {'error': '未提供认证令牌'})

            # JWT 是无状态的，登出只需客户端删除 token
            return send_json(200, {'message': '登出成功'})

        elif path == '/api/auth/me':
            # 获取当前用户信息
            auth_header = handler.headers.get('Authorization', '')
            if not auth_header.startswith('Bearer '):
                return send_json(401, {'error': '未提供认证令牌'})

            token = auth_header[7:]
            # 简单验证 token（解析 payload）
            try:
                parts = token.split('.')
                if len(parts) != 3:
                    raise ValueError('Invalid token')

                import base64
                payload = json.loads(base64.b64decode(parts[1] + '=='))
                user_id = payload.get('userId')

                if not user_id:
                    raise ValueError('Invalid token')

                # 查询用户信息
                c.execute('SELECT id, username, email, created_at, last_login_at FROM users WHERE id = ?', (user_id,))
                user = c.fetchone()

                if not user:
                    return send_json(404, {'error': '用户不存在'})

                return send_json(200, {
                    'id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'createdAt': user[3],
                    'lastLoginAt': user[4]
                })
            except Exception as e:
                return send_json(401, {'error': '无效或过期的令牌'})

    except Exception as e:
        print(f"Auth error: {e}")
        return send_json(500, {'error': '服务器错误'})
    finally:
        conn.close()

def handle_forum_post(handler):
    """处理论坛发帖请求（简化版本）"""
    def send_json(code, obj):
        handler.send_response(code)
        handler.send_header('Content-Type', 'application/json; charset=utf-8')
        handler.send_header('Access-Control-Allow-Origin', '*')
        handler.end_headers()
        handler.wfile.write(json.dumps(obj, ensure_ascii=False).encode('utf-8'))

    content_length = int(handler.headers.get('Content-Length', 0))
    body = handler.rfile.read(content_length).decode('utf-8')

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return send_json(400, {'error': 'Invalid JSON'})

    nickname = data.get('nickname', '').strip()
    content = data.get('content', '').strip()
    tag = data.get('tag', '其他')

    if not nickname or not content:
        return send_json(400, {'error': 'Missing nickname or content'})

    # 生成帖子 ID
    post_id = f"post_{int(time.time() * 1000)}_{secrets.token_hex(4)}"

    # 使用 datetime（Windows 不支持 %f）
    from datetime import datetime
    post = {
        'id': post_id,
        'nickname': nickname,
        'content': content,
        'tag': tag,
        'createdAt': datetime.utcnow().isoformat() + 'Z',
        'upvotes': 0
    }

    # 注意：本地开发环境不持久化帖子数据
    return send_json(200, post)

def handle_forum_vote(handler):
    """处理论坛点赞请求（简化版本）"""
    def send_json(code, obj):
        handler.send_response(code)
        handler.send_header('Content-Type', 'application/json; charset=utf-8')
        handler.send_header('Access-Control-Allow-Origin', '*')
        handler.end_headers()
        handler.wfile.write(json.dumps(obj, ensure_ascii=False).encode('utf-8'))

    content_length = int(handler.headers.get('Content-Length', 0))
    body = handler.rfile.read(content_length).decode('utf-8')

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return send_json(400, {'error': 'Invalid JSON'})

    # 简化版本：返回固定数值
    return send_json(200, {'upvotes': 1})

def start_server():
    # 切换到脚本所在目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # 初始化用户数据库
    init_db()

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
        print(f"\n[OK] Server started successfully!")
        print(f"[OK] Running at: http://localhost:{port}")
        print(f"[OK] Press Ctrl+C to stop the server\n")
        print("=" * 60)
        print("\nAvailable pages:")
        print(f"  - Main site:  http://localhost:{port}/index.html")
        print("  - Auth page:  http://localhost:{port}/auth.html")
        print("  - Forum page: http://localhost:{port}/forum.html")
        print("\n" + "=" * 60 + "\n")

        # 自动打开浏览器
        try:
            webbrowser.open(f'http://localhost:{port}/auth.html')
        except:
            pass

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n[OK] Server stopped.")
            sys.exit(0)

if __name__ == "__main__":
    start_server()
