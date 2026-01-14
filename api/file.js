const fs = require('fs');
const path = require('path');

const mimeTypes = {
  'png': 'image/png',
  'jpg': 'image/jpeg',
  'jpeg': 'image/jpeg',
  'gif': 'image/gif',
  'webp': 'image/webp',
  'html': 'text/html',
  'htm': 'text/html',
  'pdf': 'application/pdf'
};

module.exports = async (req, res) => {
  try {
    const filePath = req.query.path;
    if (!filePath) {
      return res.status(400).json({ error: 'Missing path parameter' });
    }

    // 解码路径
    let decodedPath = decodeURIComponent(filePath);
    if (decodedPath.startsWith('/')) {
      decodedPath = decodedPath.slice(1);
    }

    // 查找数据目录
    const possibleDataDirs = [
      path.join(process.cwd(), 'AI+X_history_data'),
      path.join(__dirname, '..', 'AI+X_history_data'),
      path.join(process.cwd(), 'public', 'AI+X_history_data')
    ];

    let dataDir = null;
    for (const dirPath of possibleDataDirs) {
      if (fs.existsSync(dirPath)) {
        dataDir = dirPath;
        break;
      }
    }

    if (!dataDir) {
      return res.status(404).json({ error: 'Data directory not found' });
    }

    // 构建完整文件路径
    const fullPath = path.join(dataDir, decodedPath.replace(/^AI\+X_history_data\//, ''));
    const resolvedPath = path.resolve(fullPath);
    const resolvedDataDir = path.resolve(dataDir);

    // 安全检查：确保文件在允许的目录内
    if (!resolvedPath.startsWith(resolvedDataDir)) {
      return res.status(403).json({ error: 'Access denied' });
    }

    if (!fs.existsSync(fullPath)) {
      return res.status(404).json({ error: 'File not found', path: decodedPath });
    }

    // 检查是否为文件
    const stat = fs.statSync(fullPath);
    if (!stat.isFile()) {
      return res.status(400).json({ error: 'Path is not a file' });
    }

    // 获取文件扩展名并设置 Content-Type
    const ext = path.extname(fullPath).slice(1).toLowerCase();
    const contentType = mimeTypes[ext] || 'application/octet-stream';

    // 读取并返回文件
    const fileContent = fs.readFileSync(fullPath);
    res.setHeader('Content-Type', contentType);
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Cache-Control', 'public, max-age=31536000');
    res.send(fileContent);
  } catch (error) {
    res.status(500).json({ 
      error: error.message,
      stack: process.env.NODE_ENV === 'development' ? error.stack : undefined
    });
  }
};
