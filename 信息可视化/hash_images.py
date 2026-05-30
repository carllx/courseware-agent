import os
import hashlib
import re

base_dir = "knowledge/textbook/Interactive Data Visualization for the Web -- Scott Murray -- 2017"
images_dir = os.path.join(base_dir, "images")
md_file = os.path.join(base_dir, "_full.md")

with open(md_file, "r", encoding="utf-8") as f:
    content = f.read()

image_files = []
for root, _, files in os.walk(images_dir):
    for file in files:
        if file == ".DS_Store": continue
        image_files.append(os.path.join(root, file))

for img_path in image_files:
    with open(img_path, "rb") as f:
        data = f.read()
    ext = os.path.splitext(img_path)[1].lower()
    h = hashlib.sha256(data).hexdigest()
    new_name = h + ext
    new_path = os.path.join(images_dir, new_name)
    
    if img_path != new_path:
        os.rename(img_path, new_path)
    
    # Path inside markdown
    rel_path = img_path
    
    # Simple replace
    content = content.replace(rel_path, "images/" + new_name)
    
    # Sometimes it's without the base_dir because of how md links work, just in case:
    # rel_img = rel_path.replace(base_dir + "/", "")
    # content = content.replace(rel_img, "images/" + new_name)

# remove empty subdirs
for root, dirs, files in os.walk(images_dir, topdown=False):
    for d in dirs:
        dir_path = os.path.join(root, d)
        if not os.listdir(dir_path):
            os.rmdir(dir_path)

with open(md_file, "w", encoding="utf-8") as f:
    f.write(content)

print("Images hashed and markdown updated.")
