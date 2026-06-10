#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成实验文档双轨 Markdown (实验指导书 + 实验报告空模板)

读取数据源：
  1. exp_X.yaml — 全量事实源 (SSOT, 包含元数据与增量步骤)

遵守 rule_document_boundaries.md 规范。
"""

import os
import sys
import yaml
import argparse
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="生成课程大实验的《实验指导书》和《实验报告》模板（基于全量单一事实源 exp_X.yaml）"
    )
    parser.add_argument("--course_dir", required=True, help="课程根目录")
    parser.add_argument("--exp", required=True, help="实验编号，如 '1'")
    return parser.parse_args()


def load_yaml(file_path):
    """加载 YAML 文件，失败时退出。"""
    if not os.path.exists(file_path):
        print(f"Error: 找不到文件 {file_path}")
        sys.exit(1)
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"Error: YAML 解析失败: {e}")
            sys.exit(1)





def generate_guide_md(course_exp, increment):
    """生成实验指导书（5 个环节）。"""
    exp_id = course_exp.get("id", "?")
    name = course_exp.get("name", "未命名实验")
    exp_type = course_exp.get("type", "未知")
    hours = course_exp.get("hours", 0)

    md = []
    md.append(f"# 实验{exp_id}：{name} — 实验指导书\n")
    md.append(f"**实验类型**：{exp_type}")
    md.append(f"**实验学时**：{hours} 学时")
    md.append(f"**每组人数**：{course_exp.get('group_size', 1)} 人")
    md.append(f"**开出要求**：{course_exp.get('requirement', '必做')}\n")
    md.append("---\n")

    # 一、实验目的
    md.append("## 一、实验目的\n")
    md.append(course_exp.get("objectives", "（待补充）").strip())
    md.append("\n")

    # 二、实验设备与环境
    md.append("## 二、实验设备与环境\n")
    md.append(course_exp.get("equipment", "（待补充）").strip())
    md.append("\n")

    # 三、实验要求
    md.append("## 三、实验要求\n")
    md.append(course_exp.get("requirements", "（待补充）").strip())
    md.append("\n")

    # 四、实验步骤与要点 (来自 exp_X.yaml 增量数据)
    md.append("## 四、实验步骤与要点\n")
    steps = increment.get("steps", [])
    for step in steps:
        md.append(f"### 步骤 {step.get('id', '')}: {step.get('name', '')}\n")
        for text in step.get("guide_text", []):
            md.append(f"- {text}")
        md.append("\n")

    # 五、实验结论
    md.append("## 五、实验结论\n")
    md.append(course_exp.get("conclusions", "（待补充）").strip())
    md.append("\n")

    return "\n".join(md)


def generate_report_md(course_exp, increment):
    """生成实验报告模板（6 个环节）。"""
    exp_id = course_exp.get("id", "?")
    name = course_exp.get("name", "未命名实验")

    md = []
    md.append(f"# 实验{exp_id}：{name} — 实验报告\n")

    # 学生信息
    md.append("> **姓名**：[请填写姓名]")
    md.append("> **学号**：[请填写学号]")
    md.append("> **班级**：[请填写班级]")
    md.append("> **日期**：[请填写实验完成日期]\n")
    md.append("---\n")

    # 一、实验目的 (预填)
    md.append("## 一、实验目的\n")
    md.append(course_exp.get("objectives", "（待补充）").strip())
    md.append("\n")

    # 二、实验设备与环境 (预填)
    md.append("## 二、实验设备与环境\n")
    md.append(course_exp.get("equipment", "（待补充）").strip())
    md.append("\n")

    # 三、实验要求 (预填)
    md.append("## 三、实验要求\n")
    md.append(course_exp.get("requirements", "（待补充）").strip())
    md.append("\n")

    # 四、实验内容（步骤）— 学生填写，图文穿插
    md.append("## 四、实验内容（步骤）\n")
    md.append("> ⚠️ **重要提示**：本部分要求**图文穿插**。请按照每个步骤下方的引导框填写操作记录与对应截图。**严禁连续粘贴纯图片而不写任何文字说明**。\n")

    steps = increment.get("steps", [])
    for step in steps:
        md.append(f"### 步骤 {step.get('id', '')}: {step.get('name', '')}\n")
        for item in step.get("report_prompt", []):
            # 支持新格式 (dict with type/prompt) 和旧格式 (plain string)
            if isinstance(item, dict):
                item_type = item.get("type", "text")
                prompt_text = item.get("prompt", "")
                if item_type == "image":
                    md.append(f"![{prompt_text}]()\n")
                else:
                    md.append(f"**[{prompt_text}]**\n")
            else:
                md.append(f"**{item}**\n")
            md.append("")  # 空行留白
        md.append("")

    # 五、实验分析 — 学生填写
    md.append("## 五、实验分析\n")
    md.append("> 请结合上述实验步骤的操作结果，对本次实验进行总结与反思。\n")
    for prompt in increment.get("analysis_prompts", []):
        md.append(f"**{prompt}**\n")
        md.append("")
    md.append("")

    # 六、成绩评定 — 教师填写
    md.append("## 六、成绩评定\n")
    md.append("> *本部分由教师填写*\n")

    rubrics = increment.get("grading_rubric", [])
    total_points = sum(item.get("points", 0) for item in rubrics)

    md.append("| 考核维度 | 满分 | 教师评分 | 评分标准说明 |")
    md.append("|---|---|---|---|")
    for item in rubrics:
        dim = item.get("dimension", "")
        pts = item.get("points", 0)
        std = item.get("standard", "")
        md.append(f"| {dim} | {pts} | | {std} |")
    md.append(f"| **总分** | **{total_points}** | | |")
    md.append("")

    md.append("**教师评语**：\n\n[教师在此处填写评语]\n")
    md.append("**签名**：________________")
    md.append("**日期**：________________\n")

    return "\n".join(md)


def main():
    args = parse_args()
    course_dir = Path(args.course_dir).resolve()
    exp_num = int(args.exp)

    # 读取全量单一事实源 exp_X.yaml
    increment_path = course_dir / "practices" / "experiments" / f"exp_{exp_num}.yaml"
    print(f"[*] 读取单一事实源配置: {increment_path}")
    increment = load_yaml(increment_path)
    
    # 统一变量引用，增量与元数据合并在同一文件中
    course_exp = increment

    # 校验外键一致性
    if increment.get("exp_id") != exp_num and increment.get("id") != exp_num:
        print(f"Warning: exp_{exp_num}.yaml 中的 exp_id={increment.get('exp_id', increment.get('id'))} 与参数 {exp_num} 不匹配")

    # 4. 生成双轨文档
    name_safe = str(course_exp.get("name", "experiment")).replace(" ", "_").replace("/", "_")
    output_dir = course_dir / "practices" / "experiments" / "Output"
    output_dir.mkdir(parents=True, exist_ok=True)

    guide_path = output_dir / f"Exp_{exp_num}_{name_safe}_实验指导书.md"
    report_path = output_dir / f"Exp_{exp_num}_{name_safe}_实验报告_学生模板.md"

    guide_content = generate_guide_md(course_exp, increment)
    report_content = generate_report_md(course_exp, increment)

    with open(guide_path, "w", encoding="utf-8") as f:
        f.write(guide_content)
    print(f"[+] 成功生成实验指导书: {guide_path}")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"[+] 成功生成实验报告模板: {report_path}")

    print(f"\n✅ 双轨实验文档生成完毕（基于单一事实源 exp_{exp_num}.yaml）。")


if __name__ == "__main__":
    main()
