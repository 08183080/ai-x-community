const { kv } = require('@vercel/kv');
const bcrypt = require('bcryptjs');
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
    const { username, password } = req.body;

    // 验证输入
    if (!username || !password) {
      return res.status(400).json({ error: '用户名和密码不能为空' });
    }

    // 查找用户
    const userId = await kv.get(`user:username:${username}`);
    if (!userId) {
      return res.status(401).json({ error: '用户名或密码错误' });
    }

    const user = await kv.get(`user:${userId}`);
    if (!user) {
      return res.status(401).json({ error: '用户不存在' });
    }

    // 验证密码
    const isValidPassword = await bcrypt.compare(password, user.password);
    if (!isValidPassword) {
      return res.status(401).json({ error: '用户名或密码错误' });
    }

    // 更新最后登录时间
    user.lastLoginAt = new Date().toISOString();
    user.updatedAt = new Date().toISOString();
    await kv.set(`user:${userId}`, user);

    // 生成 JWT token
    const token = jwt.sign(
      { userId: user.id, username: user.username },
      JWT_SECRET,
      { expiresIn: '7d' }
    );

    return res.json({
      message: '登录成功',
      token,
      user: {
        id: user.id,
        username: user.username,
        email: user.email,
        createdAt: user.createdAt,
        lastLoginAt: user.lastLoginAt
      }
    });
  } catch (error) {
    console.error('Login error:', error);
    return res.status(500).json({ error: '登录失败，请稍后重试' });
  }
};
