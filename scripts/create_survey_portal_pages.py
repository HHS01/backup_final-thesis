import zipfile, xml.etree.ElementTree as ET
from pathlib import Path

def extract_docx_text_and_tables(path):
    with zipfile.ZipFile(path) as z:
        tree = ET.fromstring(z.read('word/document.xml'))
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        elements = []
        for p in tree.iter(f"{{{ns['w']}}}p"):
            t = ''.join(n.text for n in p.iter(f"{{{ns['w']}}}t") if n.text)
            if t.strip():
                elements.append(t.strip())
        return elements

teacher_text = extract_docx_text_and_tables('/workspaces/backup_final-thesis/AoA survey/SSA_Teacher_Survey_v1_PUBLIC.docx')
provider_text = extract_docx_text_and_tables('/workspaces/backup_final-thesis/AoA survey/SSA_Provider_Survey_v1_PUBLIC.docx')

print(f"Teacher doc paragraphs: {len(teacher_text)}")
print(f"Provider doc paragraphs: {len(provider_text)}")
