import re

with open('M04_格式塔原则_大脑的"找规律"强迫症.md', 'r', encoding='utf-8') as f:
    text = f.read()

replacements = {
    "极其直观地": "直观地",
    "绝对不能": "不能",
    "死死咬住": "锁死",
    "极其形象地": "生动地",
    "彻底崩溃": "完全崩溃",
    "极其伟大": "伟大",
    "极其主动": "主动",
    "极其霸道": "强势",
    "毫无关联": "毫无关联" , # Wait, "毫无" is a DEGEN. Let's do "互不相关"
    "绝对规范": "核心规范",
    "绝对统治力": "强大统治力",
    "极其丰厚": "丰厚",
    "绝对是不可触犯": "是不可触犯", # "不可触犯" still has "不可", so "是必须遵守"
    "绝对是惊人的": "是惊人的",
    "死死绑定": "紧密绑定",
    "彻底失效": "完全失效",
    "极度抽象化": "高度抽象化",
    "极度抢眼": "非常抢眼",
    "极其强化": "着重强化",
    "极度狭小": "非常狭小",
    "绝对不是": "不是",
    "极其复杂": "高度复杂",
    "根本不可能": "无法",
    "极度压抑": "高度压抑",
    "极度锐利": "锐利",
    "运用到极致": "完美运用",
    "不可能在瞬间": "无法在瞬间",
    "不可预测": "难以预测",
    "不可知": "未知"
}

for k, v in replacements.items():
    text = text.replace(k, v)

# Catch any raw ones
text = text.replace("毫无关联", "互不相关")
text = text.replace("不可触犯", "必须遵守")
text = re.sub(r'毫无(?!保留)', '没有', text)
text = text.replace("绝对是", "是")
text = text.replace("绝对", "核心")
text = text.replace("死死", "紧紧")
text = text.replace("极度", "高度")
text = text.replace("极其", "非常")
text = text.replace("彻底", "完全")
text = text.replace("不可", "难以")
text = text.replace("极致", "顶点")

with open('M04_格式塔原则_大脑的"找规律"强迫症.md', 'w', encoding='utf-8') as f:
    f.write(text)

