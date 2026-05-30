import re
with open('/Users/yamlam/.gemini/antigravity/brain/8a7f3986-0c12-4aa5-8fad-089835d0b66f/task.md', 'r') as f:
    content = f.read()
content = content.replace('- [ ] **2. H5 预览展示层 (React)**', '- [x] **2. H5 预览展示层 (React)**')
content = content.replace('- [ ] **3. PPTX 生成器层 (Node.js)**', '- [x] **3. PPTX 生成器层 (Node.js)**')
content = content.replace('- [ ] 在 `SlideFactory.jsx`', '- [x] 在 `SlideFactory.jsx`')
content = content.replace('- [ ] 完善 `Layout_Code.jsx`', '- [x] 完善 `Layout_Code.jsx`')
content = content.replace('- [ ] 编写 `MermaidRenderer.jsx`', '- [x] 编写 `MermaidRenderer.jsx`')
content = content.replace('- [ ] 拓展 `AssetPlaceholder.jsx`', '- [x] 拓展 `AssetPlaceholder.jsx`')
content = content.replace('- [ ] 增加 `.h5-layout-code`', '- [x] 增加 `.h5-layout-code`')
content = content.replace('- [ ] 修改 `generate_course_ppt.js`', '- [x] 修改 `generate_course_ppt.js`')
content = content.replace('- [ ] 修改 `ppt_layouts.js`', '- [x] 修改 `ppt_layouts.js`')
with open('/Users/yamlam/.gemini/antigravity/brain/8a7f3986-0c12-4aa5-8fad-089835d0b66f/task.md', 'w') as f:
    f.write(content)
