const fs = require('fs');
const path = require('path');

function scanDirectory(dirPath, basePath = '') {
  const result = [];
  try {
    const items = fs.readdirSync(dirPath).sort();
    for (const item of items) {
      const itemPath = path.join(dirPath, item);
      let relPath = path.join(basePath, item).replace(/\\/g, '/');
      // 确保路径以 / 开头
      if (!relPath.startsWith('/')) {
        relPath = '/' + relPath;
      }
      
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
    // 方法1: 尝试从静态文件读取（如果存在）
    const staticListPath = path.join(process.cwd(), 'public', 'files-list.json');
    if (fs.existsSync(staticListPath)) {
      const files = JSON.parse(fs.readFileSync(staticListPath, 'utf-8'));
      res.setHeader('Content-Type', 'application/json; charset=utf-8');
      res.setHeader('Access-Control-Allow-Origin', '*');
      return res.json(files);
    }
    
    // 方法2: 动态扫描目录
    const possiblePaths = [
      path.join(process.cwd(), 'AI+X_history_data'),
      path.join(__dirname, '..', 'AI+X_history_data'),
      path.join(process.cwd(), 'public', 'AI+X_history_data')
    ];
    
    let dataDir = null;
    for (const dirPath of possiblePaths) {
      if (fs.existsSync(dirPath)) {
        dataDir = dirPath;
        break;
      }
    }
    
    if (!dataDir) {
      return res.status(404).json({ 
        error: 'Directory not found',
        message: '请运行 node generate-files-list.js 生成文件列表，或确保 AI+X_history_data 目录存在',
        tried: possiblePaths
      });
    }
    
    const files = scanDirectory(dataDir, 'AI+X_history_data');
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.json(files);
  } catch (error) {
    res.status(500).json({ 
      error: error.message,
      stack: process.env.NODE_ENV === 'development' ? error.stack : undefined
    });
  }
};
