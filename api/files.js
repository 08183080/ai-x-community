const fs = require('fs');
const path = require('path');

function scanDirectory(dirPath, basePath = '') {
  const result = [];
  try {
    const items = fs.readdirSync(dirPath).sort();
    for (const item of items) {
      const itemPath = path.join(dirPath, item);
      const relPath = path.join(basePath, item).replace(/\\/g, '/');
      
      try {
        const stat = fs.statSync(itemPath);
        if (stat.isDirectory()) {
          const children = scanDirectory(itemPath, relPath);
          result.push({
            type: 'folder',
            name: item,
            path: relPath,
            children: children
          });
        } else {
          const ext = path.extname(item).slice(1).toLowerCase();
          result.push({
            type: 'file',
            name: item,
            path: relPath,
            ext: ext
          });
        }
      } catch (err) {
        // 跳过无法访问的文件
      }
    }
  } catch (err) {
    // 目录不存在或无法访问
  }
  return result;
}

module.exports = async (req, res) => {
  try {
    // Vercel 上文件在项目根目录
    const dataDir = path.join(process.cwd(), 'AI+X_history_data');
    
    if (!fs.existsSync(dataDir)) {
      return res.status(404).json({ error: 'Directory not found' });
    }
    
    const files = scanDirectory(dataDir, 'AI+X_history_data');
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.json(files);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};
