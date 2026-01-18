// Vercel serverless function for auth endpoints
const { kv } = require('@vercel/kv');

module.exports = async (req, res) => {
  const { slug } = req.query;

  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // Handle /api/auth/me
  if (slug === 'me') {
    const authHeader = req.headers.authorization;
    const token = authHeader && authHeader.split(' ')[1];

    if (!token) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    // Verify token with KV storage
    try {
      const userId = await kv.get(`auth:token:${token}`);
      if (!userId) {
        return res.status(401).json({ error: 'Invalid token' });
      }

      const user = await kv.get(`user:${userId}`);
      return res.status(200).json(user);
    } catch (error) {
      console.error('Auth error:', error);
      return res.status(500).json({ error: error.message });
    }
  }

  // Handle /api/auth/logout
  if (slug === 'logout' && req.method === 'POST') {
    const authHeader = req.headers.authorization;
    const token = authHeader && authHeader.split(' ')[1];

    if (token) {
      try {
        await kv.del(`auth:token:${token}`);
      } catch (error) {
        console.error('Logout error:', error);
      }
    }

    return res.status(200).json({ message: 'Logged out successfully' });
  }

  res.status(404).json({ error: 'Not found' });
};
