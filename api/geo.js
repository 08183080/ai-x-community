module.exports = async (req, res) => {
  const adcode = String(req.query?.adcode || '100000').replace(/\D/g, '') || '100000';
  const url = `https://geo.datav.aliyun.com/areas_v3/bound/${adcode}_full.json`;
  try {
    const r = await fetch(url);
    if (!r.ok) return res.status(r.status).json({ error: `upstream ${r.status}`, url });
    const json = await r.json();
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.setHeader('Cache-Control', 'public, s-maxage=86400, max-age=3600');
    return res.status(200).json(json);
  } catch (e) {
    return res.status(502).json({ error: 'fetch_failed', url, message: String(e?.message || e) });
  }
};

