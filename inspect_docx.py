from pathlib import Path
from docx import Document

path = Path('templates/PLANO MENSAL CMT XLVII.docx')
print('template exists', path.exists())
doc = Document(path)
print('paragraphs', len(doc.paragraphs))
print('tables', len(doc.tables))
for ti, table in enumerate(doc.tables):
    print('TABLE', ti, 'rows', len(table.rows), 'cols', len(table.columns))
    for ri, row in enumerate(table.rows[:20]):
        print(' row', ri, [cell.text for cell in row.cells])
    print('---')
