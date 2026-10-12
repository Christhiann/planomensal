from pathlib import Path
from docx import Document

path = Path('backend/generated/plano_mensal_20260804_134434.docx')
print('generated exists', path.exists())
doc = Document(path)
print('paragraphs', len(doc.paragraphs))
print('tables', len(doc.tables))
for ti, table in enumerate(doc.tables):
    print(f'TABLE {ti} rows={len(table.rows)} cols={len(table.columns)}')
    for ri, row in enumerate(table.rows[:20]):
        print(' row', ri, [repr(cell.text) for cell in row.cells])
    print('---')
