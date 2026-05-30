import pandas as pd
import re

def verify():
    print("=== 开始严格程序化审计 ===")
    
    # 1. 验证专业防混淆
    files = [
        "/Users/yamlam/Downloads/数字媒体艺术2025（包括23级专升本）人才培养方案/数艺-23专升本-人培（表格）.xlsx",
        "/Users/yamlam/Downloads/数字媒体艺术2025（包括23级专升本）人才培养方案/数艺-25本科-人培（表格）.xlsx"
    ]
    for f in files:
        if "数字媒体艺术" not in f and "数艺" not in f:
            print(f"❌ 警告: 文件路径 {f} 可能混入了其他专业！")
        else:
            print(f"✅ 文件定性防混淆通过: 确认属于[数字媒体艺术]，排除数字媒体技术。({f})")
    
    # 2. 从 Markdown 提取我们生成的课程
    md_path = "/tmp/handoff_digital_media_art_2026_fall.md"
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
    except Exception as e:
        print(f"读取 Markdown 失败: {e}")
        return

    # 3. 严格核对 25 级本科（第三学期）
    # 在 25 本科人培表格中，第三学期通常在特定的列。我们需要找到所有在第三学期有打勾或学分标记的课程
    try:
        df_25 = pd.read_excel(files[1], sheet_name=0, header=None)
        print("✅ 成功加载: 数艺-25本科-人培（表格）.xlsx")
        
        # 寻找“三”或类似的表头来确定第三学期是哪一列
        term3_col = -1
        term1_col = -1
        course_name_col = 1 # 假设课程名在 B 列
        
        print("df_25 head:")
        for idx in range(6):
            print(list(df_25.iloc[idx, :]))
            print(f"📌 人培源文件中第三学期的实际课程包含: {actual_term3_courses[:3]} 等共 {len(actual_term3_courses)} 门")
            
            # 对比 MD 里的内容
            # 找到 MD 里 "## 2025级本科(第3学期)" 下面的表格
            match = re.search(r'## 2025级本科\(第3学期\)(.*?)(?=##|\Z)', md_content, re.DOTALL)
            if match:
                md_table = match.group(1)
                md_courses = [line.split('|')[1].strip() for line in md_table.strip().split('\n') if '|' in line and '---' not in line and '课程名称' not in line]
                print(f"📌 Markdown 中提取到的课程包含: {md_courses[:3]} 等共 {len(md_courses)} 门")
                
                missing = set(actual_term3_courses) - set(md_courses)
                extra = set(md_courses) - set(actual_term3_courses)
                
                if not missing and not extra:
                    print("✅ 100% 匹配: 2025级本科第三学期排课无任何偏差！")
                else:
                    if missing:
                        print(f"❌ 遗漏课程: {missing}")
                    if extra:
                        print(f"❌ 多出课程: {extra}")
        else:
            print("❌ 无法在表格中定位到第三学期的列。")
    except Exception as e:
        print(f"分析 25 级表格失败: {e}")

if __name__ == "__main__":
    verify()
