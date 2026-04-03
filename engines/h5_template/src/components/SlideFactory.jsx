import Layout_Split from './layouts/Layout_Split'
import Layout_List from './layouts/Layout_List'
import Layout_Diagram from './layouts/Layout_Diagram'
import Layout_Grid from './layouts/Layout_Grid'
import Layout_Image from './layouts/Layout_Image'
import Layout_Comparison from './layouts/Layout_Comparison'
import Layout_Title from './layouts/Layout_Title'

/**
 * 规范布局 → 组件映射（全小写 key）
 * 与 PPT ppt_layouts.js LAYOUT_MAP 完全对齐
 */
const CANONICAL_MAP = {
  // Title 系列
  'title':      Layout_Title,
  'section':    Layout_Title,
  'stat':       Layout_Title,
  // Split 系列
  'split':      Layout_Split,
  'code':       Layout_Split,
  // List 系列
  'list':       Layout_List,
  'agenda':     Layout_List,
  'icons':      Layout_List,
  'table':      Layout_List,
  'workshop':   Layout_List,
  // Grid 系列
  'grid':       Layout_Grid,
  'dashboard':  Layout_Grid,
  // Image 系列
  'image':      Layout_Image,
  'full':       Layout_Image,
  'screenshot': Layout_Image,
  'poll':       Layout_Image,
  // Diagram 系列
  'diagram':    Layout_Diagram,
  'timeline':   Layout_Diagram,
  // Comparison
  'comparison': Layout_Comparison,
  // Quote / CTA → Title fallback
  'quote':      Layout_Title,
  'cta':        Layout_Title,
}

/**
 * 弃用别名 → 规范名
 */
const DEPRECATED_ALIASES = {
  'card': 'grid', 'cards': 'grid',
  'full screen': 'full', 'codeblock': 'code',
  'three-column': 'grid', 'triple-column': 'grid',
  'quadrant': 'grid', 'flow': 'timeline',
  'canvas': 'grid', 'chat-bubble': 'split',
  'template-card': 'grid', 'spectrum': 'diagram',
  'text': 'list', 'chart': 'image',
  'video': 'full', 'scene': 'image',
  'checklist': 'list', 'process': 'timeline',
}

/**
 * SlideFactory — 幻灯片布局路由器
 *
 * 接受 courseId 用于构建正确的图片 URL 前缀。
 * 将 slide.image 的相对路径映射为 /courses/{courseId}/... 的绝对 URL。
 */
export default function SlideFactory({ slide, courseId }) {
  if (!slide) return null

  // 大小写不敏感 + 弃用别名解析
  let key = (slide.layout || 'Image').toLowerCase().trim()
  if (DEPRECATED_ALIASES[key]) key = DEPRECATED_ALIASES[key]
  const LayoutComponent = CANONICAL_MAP[key] || Layout_Image

  // 构造带 courseId 前缀的 slide 副本
  const resolvedSlide = {
    ...slide,
    // 将 visuals/W01_xxx/W01_S01.png → /courses/courseId/visuals/W01_xxx/W01_S01.png
    resolvedImage: slide.image
      ? (courseId ? `/courses/${courseId}/${slide.image}` : `/${slide.image}`)
      : null,
  }

  return (
    <div className="slide-frame">
      <LayoutComponent slide={resolvedSlide} />
    </div>
  )
}
