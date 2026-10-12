from pathlib import Path
from docx import Document

pdir = Path('backend/generated')
files = sorted(pdir.glob('plano_mensal_*.docx'))
if not files:
    print('no generated files')
else:
    p = files[-1]
    print('inspecting', p)
    d = Document(p)
    print('tables', len(d.tables))
    for ti, table in enumerate(d.tables):
        print('TABLE', ti, 'rows', len(table.rows), 'cols', len(table.columns))
        for ri, row in enumerate(table.rows[:20]):
            print(' row', ri, [repr(cell.text) for cell in row.cells])
        print('---')
