const { kv } = require('@vercel/kv');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { id } = req.body;

    if (!id) {
      return res.status(400).json({ error: 'Missing post id' });
    }

    const post = await kv.get(`forum:post:${id}`);
    if (!post) {
      return res.status(404).json({ error: 'Post not found' });
    }

    post.upvotes = (post.upvotes || 0) + 1;
    await kv.set(`forum:post:${id}`, post);

    const createdAt = new Date(post.createdAt).getTime();
    const hotScore = post.upvotes * 1e13 + createdAt;
    await kv.zadd('forum:posts:hot', hotScore, id);

    return res.json({ upvotes: post.upvotes });
  } catch (error) {
    console.error('Forum vote error:', error);
    return res.status(500).json({ error: error.message });
  }
};
