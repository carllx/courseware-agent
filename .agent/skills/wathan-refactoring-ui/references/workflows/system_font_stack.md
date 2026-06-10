# 工作流：使用系统字体栈 (System Font Stack)

## Prerequisites & Context (前提与背景)
- **WHY (为什么需要此工作流)**：加载自定义 Web 字体会导致额外的网络请求、延迟（FOIT 或 FOUT 现象）和潜在的渲染性能问题。而在许多现代操作系统中，内置的系统字体已经拥有极高的排版质量。
- **WHEN (何时使用)**：追求极致加载性能、构建基础工具/控制台面板，或不希望界面具有过于强烈定制品牌色彩的项目。

## Comprehensive Guide & Best Practices (全面指南与最佳实践)
1. **什么是系统字体栈**
   - 系统字体栈是指通过一段特定的 CSS `font-family` 声明，让浏览器直接使用用户当前操作系统原生的最佳字体。
   - 例如：macOS 上的 San Francisco，Windows 上的 Segoe UI，Android 上的 Roboto，Ubuntu 上的 Ubuntu 等。
2. **标准的 System Font Stack 代码片段**
   - 建议在 CSS 基础设置中使用如下配置：
     ```css
     font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
     ```
3. **系统字体带来的隐形优势**
   - **零加载时间**：立即可见，无字体闪烁。
   - **极佳的用户熟悉感**：字体与用户所在的操作系统风格高度契合，使得 Web 应用具有“原生 App”的质感。
   - **卓越的国际化与回退支持**：操作系统本身已经完美解决了多语言和表情符号的字符映射。

## If/Then Troubleshooting Logic (故障排除逻辑)
- **IF** 你的 Web 应用首屏加载时总是出现文本闪烁，或在弱网环境下文字不可见：
  - **THEN** 考虑移除庞大的自定义 Web 字体（或仅在营销落地页使用），而在应用主界面切换回 System Font Stack。
- **IF** 跨平台测试时发现排版在不同系统上的高度/宽度略有不一致：
  - **THEN** 接受这种原生差异。这正是系统字体栈的特性。通过更弹性的布局（如 Flexbox/Grid 且不写死高度）来适应字体渲染的微小变化，而不是强行对齐像素。

## Verification Checklists (验证清单)
- [ ] 是否在不需要强品牌字体的场景中，默认采用了系统字体栈？
- [ ] 字体栈的 CSS 声明是否涵盖了主流操作系统（macOS, iOS, Windows, Android）的最佳默认字体？
- [ ] 针对使用系统字体的界面，是否对容器高度进行了灵活处理，以兼容不同字体度量的差异？