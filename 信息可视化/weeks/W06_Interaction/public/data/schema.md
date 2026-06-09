# W06 数据资产 Schema 摘要

这份 Schema 摘要旨在为 Vibe Coding 阶段的 LLM 提供准确的数据上下文。在向 LLM 发送指令前，请截取相关数据结构喂给大模型，防止产生 D3 数据映射幻觉。

## M01: Stacked Normalized Horizontal Bar
**数据文件**: `us-population-state-age.csv`
**结构类型**: 宽表 (Wide format CSV)
**字段说明**:
- `name`: 字符串 (String) - 美国各州缩写，例如 `AL`, `AK`, `AZ`
- `<10`, `10-19`, `20-29`, `30-39`, `40-49`, `50-59`, `60-69`, `70-79`, `≥80`: 整数 (Integer) - 表示各年龄段在该州的人口绝对数量。

**样本数据**:
```csv
name,<10,10-19,20-29,30-39,40-49,50-59,60-69,70-79,≥80
AL,598478,638789,661666,603013,625599,673864,548376,316598,174781
AK,106741,99926,120674,102008,91539,104569,70473,28422,12503
```

---

## M02: Force-Directed Graph
**数据文件**: `miserables.json`
**结构类型**: 节点-链路树状 JSON (Node-Link JSON)
**字段说明**:
- 根对象包含两个数组：`nodes` 和 `links`
- `nodes` 数组元素:
  - `id`: 字符串 (String) - 角色名称（唯一标识）
  - `group`: 整数 (Integer) - 聚类分组 ID
- `links` 数组元素:
  - `source`: 字符串 (String) - 连线起点 ID
  - `target`: 字符串 (String) - 连线终点 ID
  - `value`: 整数 (Integer) - 关联强度权重

**样本数据**:
```json
{
  "nodes": [
    {"id": "Myriel", "group": 1},
    {"id": "Napoleon", "group": 1}
  ],
  "links": [
    {"source": "Napoleon", "target": "Myriel", "value": 1}
  ]
}
```

---

## M03: Electric Usage 2019 Heatmap
**数据文件**: `electric-usage.csv`
**结构类型**: 长表 (Long format CSV)
**字段说明**:
- `date`: 日期字符串 (String) - 格式为 `YYYY-MM-DD`
- `value`: 浮点数/整数 (Number) - 每日用电量或温度等数值指标

**样本数据**:
```csv
date,value
2019-01-01,24.5
2019-01-02,23.1
```

---

## M04: Bar Chart Race
**数据文件**: `category-brands.csv`
**结构类型**: 时序追踪长表 (Long format time-series CSV)
**字段说明**:
- `date`: 日期字符串 (String) - 格式为 `YYYY-MM-DD`
- `name`: 字符串 (String) - 品牌名称
- `category`: 字符串 (String) - 行业分类（用于色彩映射）
- `value`: 整数/浮点数 (Number) - 品牌价值或指标数值

**样本数据**:
```csv
date,name,category,value
2000-01-01,Coca-Cola,Beverages,72537
2000-01-01,Microsoft,Technology,70196
```
