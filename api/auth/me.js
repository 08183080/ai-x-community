const { kv } = require('@vercel/kv');
const jwt = require('jsonwebtoken');

const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-change-in-production';

// 验证 JWT token 的辅助函数
function verifyToken(token) {
  try {
    return jwt.verify(token, JWT_SECRET);
  } catch (error) {
    return null;
  }
}

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  res.setHeader('Access-Control-Allow-Credentials', 'true');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // 从请求头获取 token
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({ error: '未提供认证令牌' });
    }

    const token = authHeader.substring(7);
    const decoded = verifyToken(token);

    if (!decoded) {
      return res.status(401).json({ error: '无效或过期的令牌' });
    }

    // 获取用户信息
    const user = await kv.get(`user:${decoded.userId}`);
    if (!user) {
      return res.status(404).json({ error: '用户不存在' });
    }

    // 返回用户信息（不包含密码）
    return res.json({
      id: user.id,
      username: user.username,
      email: user.email,
      createdAt: user.createdAt,
      lastLoginAt: user.lastLoginAt
    });
  } catch (error) {
    console.error('Get user info error:', error);
    return res.status(500).json({ error: '获取用户信息失败' });
  }
};
