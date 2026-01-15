const { kv } = require('@vercel/kv');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, x-admin-token');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const adminToken = req.headers['x-admin-token'];
    const expectedToken = process.env.FORUM_ADMIN_TOKEN;

    if (!expectedToken || adminToken !== expectedToken) {
      return res.status(403).json({ error: 'Unauthorized' });
    }

    const { id, featured } = req.body;

    if (!id || typeof featured !== 'boolean') {
      return res.status(400).json({ error: 'Missing id or featured flag' });
    }

    const post = await kv.get(`forum:post:${id}`);
    if (!post) {
      return res.status(404).json({ error: 'Post not found' });
    }

    if (featured) {
      await kv.sadd('forum:posts:featured', id);
    } else {
      await kv.srem('forum:posts:featured', id);
    }

    return res.json({ success: true, featured });
  } catch (error) {
    console.error('Forum feature error:', error);
    return res.status(500).json({ error: error.message });
  }
};
