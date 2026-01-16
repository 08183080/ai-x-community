const fs = require('fs');
const path = require('path');

const IMG_EXT = new Set(['.png', '.jpg', '.jpeg', '.webp', '.gif']);
const toApiFile = (relPath) => `/api/file?path=${encodeURIComponent(String(relPath).replace(/\\/g, '/'))}`;

module.exports = async (req, res) => {
  try {
    const tried = [
      path.join(process.cwd(), 'AI+X_history_data', '地图'),
      path.join(__dirname, '..', 'AI+X_history_data', '地图'),
      path.join(process.cwd(), 'public', 'AI+X_history_data', '地图')
    ];

    const baseDir = tried.find(p => fs.existsSync(p));
    if (!baseDir) return res.status(404).json({ error: 'Directory not found', tried });

    const out = {};
    const cities = fs.readdirSync(baseDir, { withFileTypes: true }).filter(d => d.isDirectory()).map(d => d.name).sort();
    for (const city of cities) {
      const cityDir = path.join(baseDir, city);
      let meta = null;
      const metaPath = path.join(cityDir, 'meta.json');
      if (fs.existsSync(metaPath)) {
        try { meta = JSON.parse(fs.readFileSync(metaPath, 'utf-8')); } catch (e) {}
      }

      const files = fs.readdirSync(cityDir, { withFileTypes: true })
        .filter(d => d.isFile() && IMG_EXT.has(path.extname(d.name).toLowerCase()))
        .map(d => d.name).sort();

      const photos = Array.isArray(meta?.photos) && meta.photos.length
        ? meta.photos.map(p => ({ src: toApiFile(path.join('AI+X_history_data', '地图', city, p.file)), title: p.title || '' }))
        : files.map(f => ({ src: toApiFile(path.join('AI+X_history_data', '地图', city, f)), title: path.basename(f, path.extname(f)) }));

      if (photos.length) out[city] = { title: meta?.title || city, note: meta?.note || '', photos };
    }

    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.setHeader('Cache-Control', 'public, s-maxage=3600, max-age=600');
    return res.status(200).json(out);
  } catch (e) {
    return res.status(500).json({ error: String(e?.message || e) });
  }
};

