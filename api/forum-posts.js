const { kv } = require('@vercel/kv');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  try {
    if (req.method === 'GET') {
      const sort = req.query.sort || 'new';
      const limit = parseInt(req.query.limit || '50', 10);

      if (sort === 'featured') {
        const featuredIds = await kv.smembers('forum:posts:featured');
        if (featuredIds.length === 0) {
          return res.json([]);
        }
        const posts = [];
        for (const id of featuredIds.slice(0, limit)) {
          const post = await kv.get(`forum:post:${id}`);
          if (post) posts.push(post);
        }
        return res.json(posts.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt)));
      }

      const key = sort === 'hot' ? 'forum:posts:hot' : 'forum:posts:new';
      const ids = await kv.zrange(key, 0, limit - 1, { rev: true });
      if (ids.length === 0) {
        return res.json([]);
      }

      const posts = [];
      for (const id of ids) {
        const post = await kv.get(`forum:post:${id}`);
        if (post) posts.push(post);
      }
      return res.json(posts);
    }

    if (req.method === 'POST') {
      const { nickname, content, tag } = req.body;

      if (!nickname || !content) {
        return res.status(400).json({ error: 'Missing nickname or content' });
      }

      if (nickname.length > 50 || content.length > 2000) {
        return res.status(400).json({ error: 'Nickname or content too long' });
      }

      const id = `post_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      const createdAt = Date.now();
      const post = {
        id,
        nickname: nickname.trim(),
        content: content.trim(),
        tag: tag || '其他',
        createdAt: new Date(createdAt).toISOString(),
        upvotes: 0
      };

      await kv.set(`forum:post:${id}`, post);
      await kv.zadd('forum:posts:new', createdAt, id);
      await kv.zadd('forum:posts:hot', createdAt, id);

      return res.json(post);
    }

    return res.status(405).json({ error: 'Method not allowed' });
  } catch (error) {
    console.error('Forum posts error:', error);
    return res.status(500).json({ error: error.message });
  }
};
