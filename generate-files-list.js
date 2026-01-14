// 构建时生成文件列表的脚本
// 运行: node generate-files-list.js

const fs = require('fs');
const path = require('path');

function scanDirectory(dirPath, basePath = '') {
  const result = [];
  try {
    const items = fs.readdirSync(dirPath).sort();
    for (const item of items) {
      const itemPath = path.join(dirPath, item);
      let relPath = path.join(basePath, item).replace(/\\/g, '/');
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
        console.warn(`跳过文件: ${itemPath}`, err.message);
      }
    }
  } catch (err) {
    console.error(`扫描目录失败: ${dirPath}`, err.message);
  }
  return result;
}

const dataDir = path.join(__dirname, 'AI+X_history_data');
if (fs.existsSync(dataDir)) {
  const files = scanDirectory(dataDir, 'AI+X_history_data');
  const outputPath = path.join(__dirname, 'public', 'files-list.json');
  
  // 确保 public 目录存在
  const publicDir = path.join(__dirname, 'public');
  if (!fs.existsSync(publicDir)) {
    fs.mkdirSync(publicDir, { recursive: true });
  }
  
  fs.writeFileSync(outputPath, JSON.stringify(files, null, 2), 'utf-8');
  console.log(`✓ 文件列表已生成: ${outputPath}`);
  console.log(`✓ 共 ${files.length} 个项目`);
} else {
  console.error(`✗ 目录不存在: ${dataDir}`);
  process.exit(1);
}
