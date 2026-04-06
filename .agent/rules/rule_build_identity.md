---
trigger: glob
description: 当修改 course.yaml 中的 id/name 字段或新增课程目录时，必须校验 id 与物理目录名一致，防止 SSG 路径寻址分歧导致资产丢失。
globs:
  - "**/course.yaml"
---

# 规则：构建身份一致性 (Build Identity Consistency)

> **核心原则**：`course.yaml` 中的 `id` 字段必须与物理目录名完全一致。这是 SSG 构建管线进行路径寻址的唯一可靠锚点。

## §1 强制约束

1. 每个 `course.yaml` 必须显式声明 `course.id` 字段
2. `course.id` 的值必须与该 `course.yaml` 所在目录的**物理目录名**完全一致
3. `course.name`（展示名）可以与 `id` 不同，但不可用于路径寻址

## §2 验证方法

Agent 在编辑 `course.yaml` 后，执行以下检查：

```bash
# 对比 id 字段与目录名
for f in */course.yaml; do
  dir=$(dirname "$f")
  id=$(grep '^\s*id:' "$f" | head -1 | sed 's/.*id:\s*["'\'']*\([^"'\'']*\)["'\'']*\s*#\?.*/\1/' | xargs)
  if [ -n "$id" ] && [ "$id" != "$dir" ]; then
    echo "❌ ${f}: id='${id}' ≠ dir='${dir}'"
  fi
done
```

## §3 背景（复盘教训）

此规则源自 2026-04-06 的 TTS 同步血案：

- `data.course`（展示名"信息可视化设计"）被误用于路径拼接
- 物理目录是 `信息可视化/`，导致 4096 段音频静默跳过
- 根本原因：**展示层数据与工程键值未分离**

## §4 禁止行为

- ❌ 缺省 `id` 字段（虽然有 fallback 到 `dir_name`，但隐式行为易被未来的显式声明覆盖）
- ❌ 使用英文别名作为 `id`（如 `info-vis`）而物理目录是中文
- ❌ 在构建脚本中使用 `data.course`（展示名）进行路径拼接
