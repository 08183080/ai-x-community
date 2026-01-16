const jwt = require('jsonwebtoken');

const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-change-in-production';

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  res.setHeader('Access-Control-Allow-Credentials', 'true');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // 从请求头获取 token
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({ error: '未提供认证令牌' });
    }

    // JWT 是无状态的，客户端删除 token 即可完成登出
    // 这里我们只是验证 token 的有效性
    const token = authHeader.substring(7);
    try {
      jwt.verify(token, JWT_SECRET);
    } catch (error) {
      return res.status(401).json({ error: '无效或过期的令牌' });
    }

    return res.json({ message: '登出成功' });
  } catch (error) {
    console.error('Logout error:', error);
    return res.status(500).json({ error: '登出失败' });
  }
};
