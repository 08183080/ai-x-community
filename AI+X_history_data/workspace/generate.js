const pptxgen = require('pptxgenjs');
const html2pptx = require('C:/Users/31875/.claude/plugins/cache/anthropic-agent-skills/document-skills/69c0b1a06741/skills/pptx/scripts/html2pptx.js');

async function createPresentation() {
    const pptx = new pptxgen();
    pptx.layout = 'LAYOUT_16x9';
    pptx.author = 'AI+X 社区';
    pptx.title = 'AI+X 社群聊天记录分析 (2025年5月)';

    // Slide 1: Title
    await html2pptx('D:/AI+X web/AI+X_history_data/workspace/slide1.html', pptx);

    // Slide 2: Community Overview
    await html2pptx('D:/AI+X web/AI+X_history_data/workspace/slide2.html', pptx);

    // Slide 3: May Activities
    await html2pptx('D:/AI+X web/AI+X_history_data/workspace/slide3.html', pptx);

    // Slide 4: Tools Sharing
    await html2pptx('D:/AI+X web/AI+X_history_data/workspace/slide4.html', pptx);

    // Slide 5: Future Plans
    await html2pptx('D:/AI+X web/AI+X_history_data/workspace/slide5.html', pptx);

    // Slide 6: Vision Quote
    await html2pptx('D:/AI+X web/AI+X_history_data/workspace/slide6.html', pptx);

    await pptx.writeFile({ fileName: 'D:/AI+X web/AI+X_history_data/AI+X_社群分析_2025年5月.pptx' });
    console.log('Presentation created successfully!');
}

createPresentation().catch(console.error);
