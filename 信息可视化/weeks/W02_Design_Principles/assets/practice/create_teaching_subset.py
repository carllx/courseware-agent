"""
从星巴克完整数据集中筛选出教学用子集：
- 5 个品类各选 1 款代表性饮品（Grande 杯型）
- 保留核心营养字段：卡路里、糖、咖啡因、脂肪
- 注入"张力点"：星冰乐的含糖量远超其他品类
"""
import csv
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
raw_path = os.path.join(script_dir, 'starbucks_raw.csv')
out_path = os.path.join(script_dir, 'starbucks_teaching_subset.csv')

# 读取原始数据
with open(raw_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# 清理列名中的多余空格
clean_rows = []
for row in rows:
    clean = {k.strip(): v.strip() for k, v in row.items()}
    clean_rows.append(clean)

# 筛选 Grande 杯型的代表性饮品
# 确保五大品类各至少 1 款，且星冰乐含糖量最高
targets = {
    'Coffee': 'Brewed Coffee',
    'Classic Espresso Drinks': 'Caffè Latte',
    'Signature Espresso Drinks': 'Caramel Macchiato',
    'Tazo® Tea Drinks': 'Tazo® Chai Tea Latte',
    'Frappuccino® Blended Coffee': 'Caramel Frappuccino®',
    'Frappuccino® Blended Crème': 'Vanilla Bean Crème Frappuccino®',
    'Smoothies': 'Strawberry Smoothie',
    'Shaken Iced Beverages': 'Iced Shaken Lemonade',
}

selected = []
for row in clean_rows:
    cat = row.get('Beverage_category', '')
    bev = row.get('Beverage', '')
    prep = row.get('Beverage_prep', '')
    
    if prep == 'Grande' and cat in targets and targets[cat] in bev:
        selected.append({
            '品类': cat,
            '饮品': bev,
            '杯型': prep,
            '卡路里': row.get('Calories', ''),
            '总脂肪_g': row.get('Total Fat (g)', ''),
            '含糖量_g': row.get('Sugars (g)', ''),
            '咖啡因_mg': row.get('Caffeine (mg)', ''),
        })
        del targets[cat]  # 每个品类只选一款

# 如果某些品类没有 Grande 杯型，回退用 Tall
if targets:
    for row in clean_rows:
        cat = row.get('Beverage_category', '')
        bev = row.get('Beverage', '')
        prep = row.get('Beverage_prep', '')
        if prep in ('Tall', 'Venti') and cat in targets and targets[cat] in bev:
            selected.append({
                '品类': cat,
                '饮品': bev,
                '杯型': prep,
                '卡路里': row.get('Calories', ''),
                '总脂肪_g': row.get('Total Fat (g)', ''),
                '含糖量_g': row.get('Sugars (g)', ''),
                '咖啡因_mg': row.get('Caffeine (mg)', ''),
            })
            del targets[cat]
            if not targets:
                break

# 补充更多饮品让数据更丰富（每品类额外 2-3 款 Grande）
extra_targets = [
    ('Coffee', 'Brewed Coffee', 'Venti'),
    ('Classic Espresso Drinks', 'Cappuccino', 'Grande'),
    ('Classic Espresso Drinks', 'Caffè Mocha', 'Grande'),
    ('Signature Espresso Drinks', 'White Chocolate Mocha', 'Grande'),
    ('Signature Espresso Drinks', 'Peppermint Mocha', 'Grande'),
    ('Frappuccino® Blended Coffee', 'Java Chip Frappuccino®', 'Grande'),
    ('Frappuccino® Blended Coffee', 'Mocha Frappuccino®', 'Grande'),
    ('Frappuccino® Blended Crème', 'Strawberries & Crème Frappuccino®', 'Grande'),
    ('Tazo® Tea Drinks', 'Tazo® Green Tea Latte', 'Grande'),
    ('Tazo® Tea Drinks', 'Tazo® Full-Leaf Red Tea Latte', 'Grande'),
]

for cat_t, bev_t, prep_t in extra_targets:
    for row in clean_rows:
        cat = row.get('Beverage_category', '')
        bev = row.get('Beverage', '')
        prep = row.get('Beverage_prep', '')
        if cat == cat_t and bev_t in bev and prep == prep_t:
            entry = {
                '品类': cat,
                '饮品': bev,
                '杯型': prep,
                '卡路里': row.get('Calories', ''),
                '总脂肪_g': row.get('Total Fat (g)', ''),
                '含糖量_g': row.get('Sugars (g)', ''),
                '咖啡因_mg': row.get('Caffeine (mg)', ''),
            }
            # 避免重复
            if not any(s['饮品'] == entry['饮品'] and s['杯型'] == entry['杯型'] for s in selected):
                selected.append(entry)
            break

# 按品类排序
cat_order = ['Coffee', 'Classic Espresso Drinks', 'Signature Espresso Drinks',
             'Tazo® Tea Drinks', 'Frappuccino® Blended Coffee',
             'Frappuccino® Blended Crème', 'Smoothies', 'Shaken Iced Beverages']
selected.sort(key=lambda x: (cat_order.index(x['品类']) if x['品类'] in cat_order else 99, x['饮品']))

# 写出教学子集
fieldnames = ['品类', '饮品', '杯型', '卡路里', '总脂肪_g', '含糖量_g', '咖啡因_mg']
with open(out_path, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(selected)

print(f"✅ 教学子集已生成: {out_path}")
print(f"   共 {len(selected)} 行饮品数据")
print(f"   覆盖 {len(set(r['品类'] for r in selected))} 个品类")
print("\n--- 预览 ---")
for r in selected:
    print(f"  [{r['品类'][:12]:12s}] {r['饮品'][:30]:30s} | 卡路里:{r['卡路里']:>4s} | 糖:{r['含糖量_g']:>4s}g | 咖啡因:{r['咖啡因_mg']:>4s}mg")
