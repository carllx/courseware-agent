import pandas as pd
import yaml
import xlsxwriter

# Load students
with open("students_roster.yaml", "r", encoding="utf-8") as f:
    roster = yaml.safe_load(f)["students"]

# Prepare data
course1_students = [s for s in roster if "23" in s["class_name"] and "影视" in s["class_name"]]
course2_students = [s for s in roster if "24" in s["class_name"] and ("游戏" in s["class_name"] or "影视" in s["class_name"])]

# But to be safe, let's just group them by class_name for all students
classes = {}
for s in roster:
    c = s["class_name"]
    if c not in classes:
        classes[c] = []
    classes[c].append(s)

# Create an Excel workbook
workbook = xlsxwriter.Workbook('课程成绩实时计算系统.xlsx')

# Formats
header_format = workbook.add_format({
    'bold': True, 'text_wrap': True, 'valign': 'top', 
    'fg_color': '#D7E4BC', 'border': 1, 'align': 'center'
})
avg_format = workbook.add_format({
    'bold': True, 'fg_color': '#FCE4D6', 'border': 1, 'align': 'center', 'num_format': '0.00'
})
cell_format = workbook.add_format({'border': 1, 'align': 'center'})
name_format = workbook.add_format({'border': 1, 'align': 'left'})

def create_course_sheet(sheet_name, columns, classes_to_include):
    worksheet = workbook.add_worksheet(sheet_name)
    worksheet.freeze_panes(2, 0) # Freeze top 2 rows
    
    # Headers
    headers = ["学号", "姓名", "班级"] + [c["name"] + f" ({c['weight']}%)" for c in columns] + ["总分 (100%)"]
    for col_num, header in enumerate(headers):
        worksheet.write(1, col_num, header, header_format)
        worksheet.set_column(col_num, col_num, 15)
    worksheet.set_column(1, 1, 10) # Name column slightly narrower
    worksheet.set_column(2, 2, 25) # Class column wider
    
    # Write class average formulas at the very top (Row 0)
    worksheet.write(0, 0, "各班实时平均分：", workbook.add_format({'bold': True, 'align': 'right'}))
    
    current_row = 2
    class_ranges = {}
    
    for c_name in classes_to_include:
        if c_name not in classes: continue
        start_row = current_row + 1
        for s in classes[c_name]:
            worksheet.write(current_row, 0, s["id"], cell_format)
            worksheet.write(current_row, 1, s["name"], name_format)
            worksheet.write(current_row, 2, s["class_name"], cell_format)
            
            # Write 0 or empty for scores
            col_idx = 3
            for col in columns:
                worksheet.write(current_row, col_idx, 0, cell_format)
                col_idx += 1
                
            # Total score formula: sum of scores
            col_letter_start = xlsxwriter.utility.xl_col_to_name(3)
            col_letter_end = xlsxwriter.utility.xl_col_to_name(3 + len(columns) - 1)
            total_formula = f"=SUM({col_letter_start}{current_row+1}:{col_letter_end}{current_row+1})"
            worksheet.write_formula(current_row, 3 + len(columns), total_formula, avg_format)
            
            current_row += 1
        end_row = current_row
        class_ranges[c_name] = (start_row, end_row)
        
    # Write averages at the top for each class
    avg_col = 1
    total_col_letter = xlsxwriter.utility.xl_col_to_name(3 + len(columns))
    for c_name, (start_row, end_row) in class_ranges.items():
        worksheet.write(0, avg_col, f"{c_name}:", workbook.add_format({'bold': True, 'align': 'right'}))
        avg_formula = f"=AVERAGE({total_col_letter}{start_row}:{total_col_letter}{end_row})"
        worksheet.write_formula(0, avg_col + 1, avg_formula, avg_format)
        avg_col += 2

# Course 1: 交互产品开发
c1_cols = [
    {"name": "实验1(测试一)", "weight": 10},
    {"name": "实验2(测试二)", "weight": 15},
    {"name": "实验3(测试三)", "weight": 15},
    {"name": "期末项目(实验4)", "weight": 50},
    {"name": "考勤", "weight": 10},
]
create_course_sheet("交互产品开发", c1_cols, ["23数艺影视班", "23数艺游戏动画班", "22数字媒体艺术", "22数艺专升本2班"])

# Course 2: 信息可视化
c2_cols = [
    {"name": "实验1(测试一)", "weight": 20},
    {"name": "实验2(测试二)", "weight": 20},
    {"name": "期末项目(实验3)", "weight": 50},
    {"name": "考勤", "weight": 10},
]
create_course_sheet("信息可视化", c2_cols, ["24数字媒体艺术游戏班", "24数字媒体艺术影视班"])

workbook.close()
print("Excel generated successfully.")
