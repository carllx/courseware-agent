---
name: d3
description: This skill should be used when working with d3 to understand features, APIs, workflows, and find concrete examples.
---

# D3 Skill

This skill provides references and workflows for D3.js.

## Quick start

```javascript
// Minimal D3 working example
import * as d3 from "d3";

const data = [10, 20, 30];
d3.select("body")
  .selectAll("div")
  .data(data)
  .join("div")
  .style("width", d => `${d * 10}px`)
  .text(d => d);
```

## Workflows

Follow these steps when using the D3 skill:

- [ ] **1. Foundational Concepts**: Review `references/getting_started.md` (and `tutorials` if available).
- [ ] **2. Concrete Examples**: Consult `references/examples.md` to find matching code snippets for the required visualization.
- [ ] **3. Detailed API Context**: Use the `view_file` tool to read the specific reference files (e.g., `references/d3-shape.md`, `references/d3-scale.md`) for deep API context.
- [ ] **4. Security Validation**: Apply the Security Guidelines below before finalizing any DOM manipulation.

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **api.md** - API 核心索引路由表
- **examples.md** - 综合代码案例与使用模式
- **d3-*.md** - 包含所有正交解耦的独立模块参考文档 (涵盖 Visualization, Animation, Interaction, Data 四大类)

Use the `view_file` tool to read specific reference files when detailed information is needed.

## Notes

- This skill was automatically generated from official documentation.
- Reference files preserve the structure and examples from source docs.
- Code examples include language detection for better syntax highlighting.
- Quick reference entries are filtered to avoid low-signal placeholders and inline tokens.

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration.
2. The skill will be rebuilt with the latest information.

## Security Guidelines

When using D3 to manipulate the DOM or load data, you MUST adhere to the following security guidelines to prevent vulnerabilities:

1. **DOM & SVG XSS Prevention**: 
   - Never use `selection.html()` with unvalidated or unsanitized user data. Prefer `selection.text()`.
   - When constructing SVGs, strictly validate inputs to `<foreignObject>` to prevent external HTML injection.
   - Ensure URLs passed to attributes like `href` or `xlink:href` (e.g., in `<image>` or `<a>` tags) are validated and DO NOT contain `javascript:` payloads.
2. **Prototype Pollution**: Be cautious when dynamically parsing deep, nested, or untrusted JSON data using `d3.json()`. Ensure input is sanitized to avoid prototype pollution.
3. **Subresource Integrity (SRI)**: ALWAYS use `integrity` and `crossorigin="anonymous"` when including D3 via CDN.
4. **Safe Data Fetching**: When using `d3.json()` or `d3.csv()` with external URLs, validate endpoints to prevent Server-Side Request Forgery (SSRF) and confirm proper CORS setup.
