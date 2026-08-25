from docxtpl import DocxTemplate
doc = DocxTemplate('assets/example_template.docx')
xml = doc.get_xml()
print("Original tags:")
import re
for m in re.finditer(r'\{%.*?%\}', xml):
    print(m.group(0))

print("\nProcessed XML tags:")
try:
    xml_processed = doc.build_xml({}, doc.get_env())
    for m in re.finditer(r'\{%.*?%\}', xml_processed):
        print(m.group(0))
except Exception as e:
    print("Error:", e)
