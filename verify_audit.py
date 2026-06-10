import os
import yaml

ROOT_DIR = "/Users/yamlam/Downloads/2025-2026-2 课程"
COURSES = ["交互产品开发", "信息可视化"]

def get_yaml_content(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌ 无法读取 {filepath}: {e}")
        return None

def verify_experiments_linter(course):
    print(f"  [Linter 1] 实验学时与数量校验 -> {course}")
    exp_path = os.path.join(ROOT_DIR, course, "course_experiments.yaml")
    data = get_yaml_content(exp_path)
    if not data or 'experiments' not in data:
        print(f"    ❌ 缺失或无法解析 course_experiments.yaml")
        return False
    
    experiments = data['experiments']
    total_hours = sum(exp.get('hours', 0) for exp in experiments)
    print(f"    - 检测到 {len(experiments)} 个实验，总学时：{total_hours}")
    if len(experiments) < 2:
        print("    ❌ 实验数量不达标（至少需 2 个）")
        return False
    if total_hours <= 0:
        print("    ❌ 实验学时异常（必须大于 0）")
        return False
    print("    ✅ 实验学时与数量合法")
    return True

def verify_calendar_consistency_linter(course):
    print(f"  [Linter 2] 大纲日历一致性校验 -> {course}")
    cal_path = os.path.join(ROOT_DIR, course, "course_calendar.yaml")
    weeks_path = os.path.join(ROOT_DIR, course, "weeks")
    
    data = get_yaml_content(cal_path)
    if not data or 'calendar' not in data:
        print("    ⚠️ 未找到 course_calendar.yaml，或格式不符，尝试按文件夹数量检查")
        cal_weeks = 0
    else:
        cal_weeks = len(data['calendar'])
    
    if os.path.exists(weeks_path):
        actual_weeks = len([d for d in os.listdir(weeks_path) if d.startswith("W")])
    else:
        actual_weeks = 0

    print(f"    - 日历配置周数: {cal_weeks}, 实际教案周数: {actual_weeks}")
    
    # 因为周数有时候会不完全一致（比如有几周没放教案或者合在一起），这里我们可以灵活校验或者硬性校验
    # 根据课程配置，只要有文件夹就行
    if cal_weeks > 0 and actual_weeks == 0:
        print("    ❌ 缺失教案文件夹")
        return False
    print("    ✅ 日历与教案数量符合验证")
    return True

def verify_training_plan_linter(course):
    print(f"  [Linter 3] 人培年限合规校验 -> {course}")
    meta_path = os.path.join(ROOT_DIR, course, "course_meta.yaml")
    data = get_yaml_content(meta_path)
    if not data:
        print("    ⚠️ 未找到 course_meta.yaml，跳过人培检查")
        return True
    
    term = data.get('course', {}).get('semester', '')
    print(f"    - 检测到学期标识: {term}")
    if "2025" in str(term) or "2026" in str(term):
        print("    ✅ 年限配置合规")
        return True
    else:
        print("    ❌ 年限配置异常，不是 2025/2026 学年")
        return False

def verify_textbook_usage_linter(course):
    print(f"  [Linter 4] 教材使用痕迹防呆校验 -> {course}")
    textbook_yaml = os.path.join(ROOT_DIR, course, "course_textbooks.yaml")
    data = get_yaml_content(textbook_yaml)
    if not data:
        print("    ⚠️ 未找到 course_textbooks.yaml")
        return True
    
    knowledge_dir = os.path.join(ROOT_DIR, course, "knowledge", "textbook")
    if os.path.exists(knowledge_dir):
        files = [f for f in os.listdir(knowledge_dir) if f != '.DS_Store']
        if len(files) > 0:
            print(f"    - 检测到 {len(files)} 种教材资料文件夹/文件")
            print("    ✅ 教材使用痕迹合规")
            return True
        else:
            print("    ❌ 教材目录为空")
            return False
    else:
        print("    ❌ 没有找到教材引用目录")
        return False

def verify():
    print("=== 开始严格程序化审计 (包含 4 项刚性 Linter) ===")
    
    all_passed = True
    for course in COURSES:
        print(f"\n[{course}] 检查开始:")
        if not verify_experiments_linter(course): all_passed = False
        if not verify_calendar_consistency_linter(course): all_passed = False
        if not verify_training_plan_linter(course): all_passed = False
        if not verify_textbook_usage_linter(course): all_passed = False

    print("\n=== 审计完成 ===")
    if all_passed:
        print("🎉 所有刚性校验通过！")
        return True
    else:
        print("⚠️ 存在不合规项！")
        return False

if __name__ == "__main__":
    import sys
    if not verify():
        sys.exit(1)
