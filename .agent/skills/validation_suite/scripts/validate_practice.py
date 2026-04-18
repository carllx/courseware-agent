#!/usr/bin/env python3
"""
实践活动 YAML 验证器 (Practice Validator)

基于 practice_schema.md v3.1 (ADR 043 + 超星集成) 执行以下校验：
  - YAML 语法合法性
  - SSOT 越界检查（禁止 weight/scoring_rubric）
  - experiment_link 类型校验（list[int]）
  - theory_link 结构化格式 + concept_id 引用完整性
  - total_minutes = sum(phases[].minutes) 一致性
  - theory_link 条件必填（workshop/practice/critique 类型）
  - concept_registry.yaml 格式校验（ID 唯一、snake_case）
  - quiz 导出文件存在性校验（chaoxing_export）
  - Schema 版本同步检查

用法:
    python validate_practice.py --course "交互产品开发"
    python validate_practice.py --course "信息可视化" --week 6
    python validate_practice.py --all      # 跨课程全量
"""

import argparse
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("❌ 缺少 PyYAML：pip install pyyaml")
    sys.exit(1)


# ── 配置 ──────────────────────────────────────────────────

# 禁止出现在 practice.yaml 中的字段（SSOT 在 course.yaml）
SSOT_BANNED_FIELDS = {"weight", "scoring_rubric"}

# 要求提供 theory_link 的 phase 类型
THEORY_LINK_REQUIRED_TYPES = {"workshop", "practice", "critique"}

# concept_id 命名约定
CONCEPT_ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")

# Schema 版本 SSOT
SCHEMA_VERSION_SSOT = "3.1"

# 排除的目录（build 产物、dist 等）
EXCLUDED_DIRS = {"build", "dist", "node_modules", ".build", "engines"}


# ── 数据类 ────────────────────────────────────────────────

class Issue:
    """单条校验问题。"""

    def __init__(self, file: str, code: str, severity: str, message: str, line: int = None):
        self.file = file
        self.code = code          # 如 SSOT_VIOLATION, CA_REF_BROKEN
        self.severity = severity  # 🔴 / 🟡 / 🟢
        self.message = message
        self.line = line

    def __str__(self):
        loc = f"L{self.line}" if self.line else ""
        return f"  {self.severity} [{self.code}] {self.file}{(':' + loc) if loc else ''}: {self.message}"


# ── 核心校验函数 ──────────────────────────────────────────

def load_concept_registry(course_dir: Path) -> tuple[dict, list[Issue]]:
    """加载并校验 concept_registry.yaml，返回 (id→name 映射, 问题列表)。"""
    issues = []
    registry = {}
    registry_file = course_dir / "concept_registry.yaml"

    if not registry_file.exists():
        issues.append(Issue(
            str(registry_file), "REGISTRY_MISSING", "🟡",
            "概念注册表文件不存在——无法进行 theory_link 引用完整性校验"
        ))
        return registry, issues

    try:
        data = yaml.safe_load(registry_file.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        issues.append(Issue(
            str(registry_file), "REGISTRY_YAML_ERROR", "🔴",
            f"YAML 解析失败: {e}"
        ))
        return registry, issues

    if not data or "concepts" not in data:
        issues.append(Issue(
            str(registry_file), "REGISTRY_EMPTY", "🟡",
            "concept_registry.yaml 为空或缺少 concepts 键"
        ))
        return registry, issues

    seen_ids = set()
    for i, concept in enumerate(data["concepts"]):
        if not isinstance(concept, dict):
            issues.append(Issue(
                str(registry_file), "REGISTRY_FORMAT", "🔴",
                f"concepts[{i}] 不是对象格式"
            ))
            continue

        cid = concept.get("id")
        name = concept.get("name")

        if not cid:
            issues.append(Issue(
                str(registry_file), "REGISTRY_NO_ID", "🔴",
                f"concepts[{i}] 缺少 id 字段"
            ))
            continue

        # snake_case 校验
        if not CONCEPT_ID_PATTERN.match(cid):
            issues.append(Issue(
                str(registry_file), "REGISTRY_ID_FORMAT", "🟡",
                f"概念 ID '{cid}' 不符合 snake_case 命名约定"
            ))

        # 唯一性校验
        if cid in seen_ids:
            issues.append(Issue(
                str(registry_file), "REGISTRY_DUPLICATE_ID", "🔴",
                f"概念 ID '{cid}' 重复定义"
            ))
        seen_ids.add(cid)

        # 必填字段
        if not name:
            issues.append(Issue(
                str(registry_file), "REGISTRY_NO_NAME", "🟡",
                f"概念 '{cid}' 缺少 name 字段"
            ))

        if "first_introduced" not in concept:
            issues.append(Issue(
                str(registry_file), "REGISTRY_NO_WEEK", "🟡",
                f"概念 '{cid}' 缺少 first_introduced 字段"
            ))

        registry[cid] = name or cid

    return registry, issues


def load_stale_terms(course_dir: Path) -> tuple[list, list[Issue]]:
    """加载课程级别的过时术语配置（可选）。

    读取 <课程>/stale_terms.yaml，返回 ([编译后的正则, 术语名, 原因], 问题列表)。
    文件不存在时静默跳过，返回空列表。
    """
    issues = []
    patterns = []
    stale_file = course_dir / "stale_terms.yaml"

    if not stale_file.exists():
        return patterns, issues

    try:
        data = yaml.safe_load(stale_file.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        issues.append(Issue(
            str(stale_file), "STALE_TERMS_YAML_ERROR", "🟡",
            f"stale_terms.yaml 解析失败: {e}"
        ))
        return patterns, issues

    if not data or "terms" not in data:
        return patterns, issues

    for item in data["terms"]:
        if not isinstance(item, dict):
            continue
        regex = item.get("regex", "")
        term = item.get("term", regex)
        reason = item.get("reason", "该术语已被标记为过时")
        try:
            patterns.append((re.compile(regex), term, reason))
        except re.error as e:
            issues.append(Issue(
                str(stale_file), "STALE_TERMS_REGEX_ERROR", "🟡",
                f"术语 '{term}' 的正则表达式无效: {e}"
            ))

    return patterns, issues


def validate_practice_file(filepath: Path, concept_registry: dict,
                           workspace: Path = None,
                           stale_terms: list = None) -> list[Issue]:
    """对单个 practice.yaml 执行全部校验，返回问题列表。"""
    issues = []
    # 使用相对路径显示
    rel_path = str(filepath.relative_to(workspace)) if workspace else str(filepath)

    # ── R0: YAML 语法 ──
    try:
        data = yaml.safe_load(filepath.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        issues.append(Issue(rel_path, "YAML_SYNTAX", "🔴", f"YAML 解析失败: {e}"))
        return issues

    if not data or not isinstance(data, dict):
        issues.append(Issue(rel_path, "YAML_EMPTY", "🔴", "文件为空或非字典格式"))
        return issues

    # ── R1: 顶层必填字段 ──
    for field in ("week", "title", "total_minutes", "phases"):
        if field not in data:
            issues.append(Issue(rel_path, "MISSING_FIELD", "🔴", f"缺少顶层必填字段: {field}"))

    # ── R2: experiment_link 类型校验 (Schema 规则 4) ──
    exp_link = data.get("experiment_link")
    if exp_link is not None:
        if not isinstance(exp_link, list):
            issues.append(Issue(
                rel_path, "EXP_LINK_LEGACY", "🔴",
                f"experiment_link 应为 list[int]，实际为 {type(exp_link).__name__}: {exp_link}"
            ))
        elif exp_link:
            for item in exp_link:
                if not isinstance(item, int):
                    issues.append(Issue(
                        rel_path, "EXP_LINK_TYPE", "🔴",
                        f"experiment_link 元素应为 int，实际为 {type(item).__name__}: {item}"
                    ))

    # ── R3: total_minutes 一致性 (Schema 规则 1) ──
    phases = data.get("phases", [])
    if isinstance(phases, list) and "total_minutes" in data:
        phase_sum = sum(p.get("minutes", 0) for p in phases if isinstance(p, dict))
        total = data["total_minutes"]
        if isinstance(total, (int, float)) and phase_sum != total:
            issues.append(Issue(
                rel_path, "MINUTES_MISMATCH", "🔴",
                f"sum(phases[].minutes)={phase_sum} ≠ total_minutes={total}"
            ))

    # ── R4-R6: Phase 级别校验 ──
    if isinstance(phases, list):
        seen_phase_ids = set()
        for i, phase in enumerate(phases):
            if not isinstance(phase, dict):
                issues.append(Issue(rel_path, "PHASE_FORMAT", "🔴", f"phases[{i}] 不是对象格式"))
                continue

            pid = phase.get("id", f"P{i+1}")

            # Phase ID 唯一性
            if pid in seen_phase_ids:
                issues.append(Issue(rel_path, "PHASE_ID_DUPLICATE", "🟡", f"Phase ID '{pid}' 重复"))
            seen_phase_ids.add(pid)

            # 必填字段
            for field in ("name", "minutes", "type"):
                if field not in phase:
                    issues.append(Issue(
                        rel_path, "PHASE_MISSING_FIELD", "🔴",
                        f"phases[{i}] ({pid}) 缺少必填字段: {field}"
                    ))

            # R4: SSOT 越界检查 (Schema 规则 10)
            for banned in SSOT_BANNED_FIELDS:
                if banned in phase:
                    issues.append(Issue(
                        rel_path, "SSOT_VIOLATION", "🔴",
                        f"phases[{i}] ({pid}) 含被禁字段 '{banned}'——"
                        f"SSOT 在 course.yaml.assessment_methods (ADR 043)"
                    ))

            # R5: theory_link 条件必填 (Schema 规则 7)
            ptype = phase.get("type", "")
            theory_link = phase.get("theory_link")
            if ptype in THEORY_LINK_REQUIRED_TYPES and not theory_link:
                issues.append(Issue(
                    rel_path, "CA_MISSING_LINK", "🟡",
                    f"phases[{i}] ({pid}) type='{ptype}' 要求提供 theory_link（构建性对齐）"
                ))

            # R6: theory_link 格式与引用完整性 (Schema 规则 8)
            if theory_link:
                if isinstance(theory_link, str):
                    issues.append(Issue(
                        rel_path, "CA_LEGACY_FORMAT", "🔴",
                        f"phases[{i}] ({pid}) theory_link 为纯字符串（已废弃），"
                        f"须改为结构化对象 {{concept_id, description}} 或对象数组"
                    ))
                elif isinstance(theory_link, dict):
                    theory_links = [theory_link]
                elif isinstance(theory_link, list):
                    theory_links = theory_link
                else:
                    issues.append(Issue(
                        rel_path, "CA_INVALID_TYPE", "🔴",
                        f"phases[{i}] ({pid}) theory_link 类型无效: {type(theory_link).__name__}"
                    ))
                    theory_links = []

                for tl_idx, link_obj in enumerate(theory_links):
                    if not isinstance(link_obj, dict):
                        issues.append(Issue(
                            rel_path, "CA_INVALID_TYPE", "🔴",
                            f"phases[{i}] ({pid}) theory_link[{tl_idx}] 不是对象"
                        ))
                        continue
                    
                    cid = link_obj.get("concept_id")
                    if not cid:
                        issues.append(Issue(
                            rel_path, "CA_NO_CONCEPT_ID", "🔴",
                            f"phases[{i}] ({pid}) theory_link[{tl_idx}] 缺少 concept_id"
                        ))
                    elif concept_registry and cid not in concept_registry:
                        issues.append(Issue(
                            rel_path, "CA_REF_BROKEN", "🔴",
                            f"phases[{i}] ({pid}) concept_id='{cid}' "
                            f"不存在于 concept_registry.yaml"
                        ))

            # deliverables 必填
            if not phase.get("deliverables"):
                issues.append(Issue(
                    rel_path, "PHASE_NO_DELIVERABLES", "🟡",
                    f"phases[{i}] ({pid}) 缺少 deliverables 提交物清单"
                ))

    # ── R7: Homework 级别校验 ──
    homework = data.get("homework")
    if homework and isinstance(homework, dict):
        # SSOT 越界
        for banned in SSOT_BANNED_FIELDS:
            if banned in homework:
                issues.append(Issue(
                    rel_path, "SSOT_VIOLATION", "🔴",
                    f"homework 含被禁字段 '{banned}'——SSOT 在 course.yaml (ADR 043)"
                ))

        # 必填字段
        if not homework.get("title"):
            issues.append(Issue(rel_path, "HW_NO_TITLE", "🟡", "homework 缺少 title"))
        if not homework.get("deliverables"):
            issues.append(Issue(rel_path, "HW_NO_DELIVERABLES", "🟡", "homework 缺少 deliverables"))

    # ── R8: quiz 导出文件存在性 (Schema 规则 11) ──
    # ── R8b: quiz 知识点覆盖率语义校验 ──
    if isinstance(phases, list):
        for i, phase in enumerate(phases):
            if not isinstance(phase, dict):
                continue
            pid = phase.get("id", f"P{i+1}")
            materials = phase.get("materials", [])
            if isinstance(materials, list):
                for mi, mat in enumerate(materials):
                    if not isinstance(mat, dict):
                        continue
                    if mat.get("type") == "quiz" and mat.get("chaoxing_export"):
                        export_path = mat["chaoxing_export"]
                        # 相对于课程根目录解析
                        if workspace:
                            # 从 practice.yaml 路径推算课程目录
                            course_dir = filepath.parent
                            # 向上查找 course.yaml 所在目录
                            while course_dir != workspace and not (course_dir / "course.yaml").exists():
                                course_dir = course_dir.parent
                            abs_export = course_dir / export_path
                        else:
                            abs_export = filepath.parent / export_path
                        if not abs_export.exists():
                            issues.append(Issue(
                                rel_path, "QUIZ_EXPORT_MISSING", "🟡",
                                f"phases[{i}] ({pid}) materials[{mi}] chaoxing_export "
                                f"指向的文件不存在: {export_path}"
                            ))
                        else:
                            # R8b: 语义层校验 — 题库知识点 vs theory_prerequisites 覆盖率
                            prereqs = data.get("theory_prerequisites", [])
                            if isinstance(prereqs, list) and prereqs:
                                try:
                                    quiz_text = abs_export.read_text(encoding="utf-8")
                                    # 提取题库文件中所有 "知识点：xxx" 标签
                                    quiz_tags = set()
                                    for line in quiz_text.splitlines():
                                        stripped = line.strip()
                                        if stripped.startswith("知识点：") or stripped.startswith("知识点:"):
                                            tag = stripped.split("：", 1)[-1].split(":", 1)[-1].strip()
                                            if tag:
                                                quiz_tags.add(tag)

                                    if quiz_tags:
                                        # 交叉比对：每个 prerequisite 是否被至少 1 道题覆盖
                                        for prereq in prereqs:
                                            if isinstance(prereq, str) and prereq not in quiz_tags:
                                                issues.append(Issue(
                                                    rel_path, "QUIZ_PREREQ_UNCOVERED", "🟡",
                                                    f"theory_prerequisites 中的 '{prereq}' "
                                                    f"未被题库 ({export_path}) 中的任何题目覆盖——"
                                                    f"学生无法通过快测激活该知识点"
                                                ))
                                    else:
                                        issues.append(Issue(
                                            rel_path, "QUIZ_NO_TAGS", "🟡",
                                            f"题库文件 ({export_path}) 中未发现任何 '知识点：' 标签——"
                                            f"无法校验知识点覆盖率"
                                        ))

                                    # R8c: 题量一致性校验
                                    declared_q = mat.get("questions")
                                    if declared_q is not None:
                                        # 统计题库中的实际题数（匹配 "N.【" 模式）
                                        actual_q = len(re.findall(
                                            r"^\d+\.\s*【", quiz_text, re.MULTILINE
                                        ))
                                        if actual_q and actual_q != declared_q:
                                            issues.append(Issue(
                                                rel_path, "QUIZ_COUNT_MISMATCH", "🟡",
                                                f"YAML 声明 questions={declared_q}，"
                                                f"但题库文件实际含 {actual_q} 题——需同步回填"
                                            ))

                                except Exception as e:
                                    issues.append(Issue(
                                        rel_path, "QUIZ_READ_ERROR", "🟡",
                                        f"读取题库文件失败 ({export_path}): {e}"
                                    ))

    # ── R9: practice_guide.md 下游衍生文档校验 ──
    guide_path = filepath.parent / "practice_guide.md"
    guide_rel = str(guide_path.relative_to(workspace)) if workspace else str(guide_path)

    if not guide_path.exists():
        issues.append(Issue(
            rel_path, "GUIDE_MISSING", "🟡",
            "同目录下缺少 practice_guide.md——学生无可操作的实践指南"
        ))
    else:
        try:
            guide_text = guide_path.read_text(encoding="utf-8")
        except Exception:
            guide_text = ""

        if guide_text:
            # R9a: 过时术语巡检（数据源为课程级 stale_terms.yaml，无硬编码）
            if stale_terms:
                for pattern, term, reason in stale_terms:
                    matches = pattern.findall(guide_text)
                    if matches:
                        issues.append(Issue(
                            guide_rel, "GUIDE_STALE_TERM", "🟡",
                            f"practice_guide.md 中出现过时术语 '{term}'——{reason}"
                        ))

            # R9b: theory_prerequisites 一致性检查
            prereqs = data.get("theory_prerequisites", [])
            if isinstance(prereqs, list):
                for prereq in prereqs:
                    if isinstance(prereq, str) and prereq not in guide_text:
                        issues.append(Issue(
                            guide_rel, "GUIDE_PREREQ_DRIFT", "🟡",
                            f"practice.yaml 的 theory_prerequisites 含 '{prereq}'，"
                            f"但 practice_guide.md 中未提及——学生指南与 YAML 脱节"
                        ))

            # R9c: concept_registry 术语正向验证
            if concept_registry:
                for cid, cname in concept_registry.items():
                    # 仅检查当前周次关联的 concept（通过 theory_link 关联）
                    linked_concepts = set()
                    for phase in (data.get("phases") or []):
                        if isinstance(phase, dict):
                            tl = phase.get("theory_link")
                            tl_list = tl if isinstance(tl, list) else ([tl] if isinstance(tl, dict) else [])
                            for link_obj in tl_list:
                                if isinstance(link_obj, dict) and link_obj.get("concept_id"):
                                    linked_concepts.add(link_obj["concept_id"])
                    if cid in linked_concepts and cname not in guide_text:
                        issues.append(Issue(
                            guide_rel, "GUIDE_CONCEPT_MISSING", "🟢",
                            f"practice.yaml 通过 theory_link 引用了概念 '{cname}' ({cid})，"
                            f"但 practice_guide.md 中未提及——建议在指南中强化该术语"
                        ))

    return issues


def check_schema_version_sync(workspace: Path) -> list[Issue]:
    """检查各课程本地 _schema.md 是否引用了正确的全局 Schema 版本。"""
    issues = []
    global_schema = workspace / ".agent" / "templates" / "practice_schema.md"

    if not global_schema.exists():
        return issues

    # 提取全局版本号
    content = global_schema.read_text(encoding="utf-8")
    match = re.search(r"Schema Version:\s*([\d.]+)", content)
    if not match:
        return issues
    global_ver = match.group(1)

    # 扫描各课程本地 _schema.md
    for local_schema in workspace.glob("**/practices/_schema.md"):
        # 排除 build/dist
        if any(part in EXCLUDED_DIRS for part in local_schema.parts):
            continue
        local_content = local_schema.read_text(encoding="utf-8")
        local_match = re.search(r"\*\*v([\d.]+)\*\*", local_content)
        if local_match:
            local_ver = local_match.group(1)
            if local_ver != global_ver:
                issues.append(Issue(
                    str(local_schema), "SCHEMA_VERSION_DRIFT", "🟡",
                    f"本地 Schema 引用 v{local_ver} ≠ 全局 SSOT v{global_ver}"
                ))

    return issues


# ── 文件发现 ──────────────────────────────────────────────

def discover_practice_files(workspace: Path, course: str = None, week: int = None) -> list[Path]:
    """发现所有 practice.yaml 文件（排除 build/dist 等产物目录）。"""
    files = []

    if course:
        search_roots = [workspace / course]
    else:
        # 全量扫描：跳过 .agent 和通用目录
        search_roots = [
            d for d in workspace.iterdir()
            if d.is_dir() and d.name not in EXCLUDED_DIRS
            and not d.name.startswith(".")
        ]

    for root in search_roots:
        for f in root.rglob("practice.yaml"):
            # 排除 build/dist 中的副本
            if any(part in EXCLUDED_DIRS for part in f.parts):
                continue
            # 排除 materials 下误放的（如 W01_Visual_Perception/materials/practice.yaml）
            if "materials" in f.parts:
                continue
            # 按周次过滤
            if week is not None:
                week_match = re.search(r"W(\d+)", str(f))
                if week_match and int(week_match.group(1)) != week:
                    continue
            files.append(f)

    return sorted(files)


def discover_courses(workspace: Path) -> list[str]:
    """发现所有含 course.yaml 的课程目录名。"""
    courses = []
    for f in workspace.glob("*/course.yaml"):
        if any(part in EXCLUDED_DIRS for part in f.parts):
            continue
        courses.append(f.parent.name)
    return sorted(courses)


# ── 主函数 ────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="实践活动 YAML 验证器 (ADR 043 / Schema v3.0)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--course", help="课程目录名")
    group.add_argument("--all", action="store_true", help="跨课程全量校验")
    parser.add_argument("--week", type=int, default=None, help="仅验证指定周次")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式报告")
    args = parser.parse_args()

    # 推算工作区根目录
    script_dir = Path(__file__).resolve().parent
    workspace = script_dir.parents[3]  # .agent/skills/validation_suite/scripts → workspace

    print("🛡️  Practice Validator (Schema v3.1 / ADR 043 + 超星集成)")
    print("=" * 60)

    all_issues: list[Issue] = []
    files_checked = 0

    # 确定校验范围
    if args.all:
        courses = discover_courses(workspace)
        print(f"  模式: 跨课程全量")
        print(f"  发现课程: {', '.join(courses) or '无'}")
    else:
        courses = [args.course]
        print(f"  课程: {args.course}")
        if args.week:
            print(f"  周次: W{args.week:02d}")

    print("=" * 60)

    for course in courses:
        course_dir = workspace / course

        if not course_dir.exists():
            all_issues.append(Issue(course, "COURSE_NOT_FOUND", "🔴", f"课程目录不存在: {course_dir}"))
            continue

        # 1. 加载并校验 concept_registry
        print(f"\n📂 课程: {course}")
        registry, reg_issues = load_concept_registry(course_dir)
        all_issues.extend(reg_issues)
        if registry:
            print(f"   概念注册表: {len(registry)} 个概念已加载")
        else:
            print(f"   概念注册表: ⚠️ 未加载（将跳过引用完整性校验）")

        # 1b. 加载课程级过时术语配置（可选）
        stale_terms, stale_issues = load_stale_terms(course_dir)
        all_issues.extend(stale_issues)
        if stale_terms:
            print(f"   过时术语表: {len(stale_terms)} 条已加载")
        else:
            print(f"   过时术语表: 未配置（跳过 R9a 检查）")

        # 2. 发现并校验 practice.yaml 文件
        practice_files = discover_practice_files(workspace, course, args.week)
        if not practice_files:
            print(f"   practice.yaml: 未发现（范围内无文件）")
            continue

        for pf in practice_files:
            rel = pf.relative_to(workspace)
            print(f"   📄 {rel}")
            file_issues = validate_practice_file(pf, registry, workspace, stale_terms)
            all_issues.extend(file_issues)
            files_checked += 1

            # 实时输出每个文件的问题
            if file_issues:
                for issue in file_issues:
                    print(f"   {issue}")
            else:
                print(f"      ✅ 全部通过")

    # 3. Schema 版本同步检查
    print(f"\n🔄 Schema 版本同步检查")
    version_issues = check_schema_version_sync(workspace)
    all_issues.extend(version_issues)
    if version_issues:
        for issue in version_issues:
            print(f"   {issue}")
    else:
        print(f"   ✅ 所有本地 _schema.md 与全局 SSOT 版本一致")

    # ── 汇总 ──
    print(f"\n{'=' * 60}")
    print("📊 校验汇总")
    print(f"{'=' * 60}")
    print(f"  检查文件数: {files_checked}")

    critical = [i for i in all_issues if i.severity == "🔴"]
    warnings = [i for i in all_issues if i.severity == "🟡"]
    info = [i for i in all_issues if i.severity == "🟢"]

    print(f"  🔴 致命: {len(critical)}")
    print(f"  🟡 警告: {len(warnings)}")
    print(f"  🟢 信息: {len(info)}")

    if critical:
        print(f"\n❌ 存在 {len(critical)} 个致命问题，需修复后方可通过：")
        for i in critical:
            print(f"   {i}")
        sys.exit(1)
    elif warnings:
        print(f"\n⚠️ 存在 {len(warnings)} 个警告，建议修复：")
        for i in warnings:
            print(f"   {i}")
        print(f"\n✅ 无致命问题，校验通过（含警告）")
        sys.exit(0)
    else:
        print(f"\n✨ 全部检查已通过！")
        sys.exit(0)


if __name__ == "__main__":
    main()
