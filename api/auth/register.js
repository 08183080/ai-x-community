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
    const { username, password, email } = req.body;

    // 验证输入
    if (!username || !password) {
      return res.status(400).json({ error: '用户名和密码不能为空' });
    }

    if (username.length < 3 || username.length > 20) {
      return res.status(400).json({ error: '用户名长度必须在 3-20 个字符之间' });
    }

    if (password.length < 6) {
      return res.status(400).json({ error: '密码长度必须至少 6 个字符' });
    }

    // 检查用户名是否已存在
    const existingUser = await kv.get(`user:username:${username}`);
    if (existingUser) {
      return res.status(400).json({ error: '用户名已存在' });
    }

    // 检查邮箱是否已存在（如果提供了邮箱）
    if (email) {
      const existingEmail = await kv.get(`user:email:${email}`);
      if (existingEmail) {
        return res.status(400).json({ error: '邮箱已被注册' });
      }
    }

    // 哈希密码
    const hashedPassword = await bcrypt.hash(password, 10);

    // 创建用户
    const userId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    const user = {
      id: userId,
      username: username.trim(),
      email: email ? email.trim().toLowerCase() : null,
      password: hashedPassword,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };

    // 存储用户信息
    await kv.set(`user:${userId}`, user);
    await kv.set(`user:username:${username}`, userId);
    if (email) {
      await kv.set(`user:email:${email}`, userId);
    }

    // 生成 JWT token
    const token = jwt.sign(
      { userId: user.id, username: user.username },
      JWT_SECRET,
      { expiresIn: '7d' }
    );

    return res.status(201).json({
      message: '注册成功',
      token,
      user: {
        id: user.id,
        username: user.username,
        email: user.email,
        createdAt: user.createdAt
      }
    });
  } catch (error) {
    console.error('Registration error:', error);
    return res.status(500).json({ error: '注册失败，请稍后重试' });
  }
};
