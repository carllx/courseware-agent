import '../styles/slide-area.css'
import '../styles/h5-layouts.css'
import Layout_Split from './layouts/Layout_Split'
import Layout_List from './layouts/Layout_List'
import Layout_Diagram from './layouts/Layout_Diagram'
import Layout_Grid from './layouts/Layout_Grid'
import Layout_Image from './layouts/Layout_Image'
import Layout_Comparison from './layouts/Layout_Comparison'
import Layout_Title from './layouts/Layout_Title'
import BrokenImageOverlay from './BrokenImageOverlay'
import { parseListString, parseComparisonData } from '../utils/slide_parser'

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
  // Diagram 系列
  'diagram':    Layout_Diagram,
  'timeline':   Layout_Diagram,
  // Comparison
  'comparison': Layout_Comparison,
  // Poll
  'poll':       Layout_List,
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
  'center': 'title',
}

/**
 * SlideFactory — 幻灯片布局路由器 & 数据代理层
 */
export default function SlideFactory({ slide, courseId }) {
  if (!slide) return null

  // 大小写不敏感 + 弃用别名解析
  let key = (slide.layout || 'Image').toLowerCase().trim()
  if (DEPRECATED_ALIASES[key]) key = DEPRECATED_ALIASES[key]
  const LayoutComponent = CANONICAL_MAP[key] || Layout_Image

  // 数据解析：兼容 SSG 环境下的静态根路径
  const getImageUrl = (imgPath) => {
    if (!imgPath) return null
    if (imgPath.startsWith('/') || imgPath.startsWith('http')) return imgPath
    return courseId ? `/courses/${courseId}/${imgPath}` : `/${imgPath}`
  }
  const resolvedImage = getImageUrl(slide.image)
  // V-04 fix: images 数组也要经过环境感知的路径解析，防止 SSG 绝对路径被二次拼接前缀
  const resolvedImages = (slide.images || []).map(getImageUrl)

  // 数据代理层 (Data Proxy): 统一拆解 Markdown 字符串列为规整数据结构，使子组件保持纯净
  const parsedList = parseListString(slide.list)
  const comparisonData = parseComparisonData(slide.list)

  const resolvedSlide = {
    ...slide,
    resolvedImage,
    resolvedImages,
    parsedList,
    comparisonData,
  }

  // 检测断链状态
  const isBroken = resolvedSlide.assetExpected && !resolvedSlide.image

  return (
    <div className={`slide-frame${isBroken ? ' slide-frame--broken' : ''}`}>
      <LayoutComponent slide={resolvedSlide} />
      {isBroken && <BrokenImageOverlay expected={resolvedSlide.assetExpected} />}
    </div>
  )
}
