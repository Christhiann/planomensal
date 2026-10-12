from pathlib import Path
from docx import Document

path = Path('templates/PLANO MENSAL CMT XLVII.docx')
doc = Document(path)
print('tables', len(doc.tables))
for ti, table in enumerate(doc.tables):
    print(f'TABLE {ti} rows={len(table.rows)} cols={len(table.columns)}')
    for ri, row in enumerate(table.rows):
        for ci, cell in enumerate(row.cells):
            print(f'  cell {ti}.{ri}.{ci}: text={repr(cell.text)}')
            for pi, para in enumerate(cell.paragraphs):
                print(f'    para {pi}: {repr(para.text)} runs={len(para.runs)}')
                for rj, run in enumerate(para.runs):
                    print(f'      run {rj}: {repr(run.text)}')
        if ri >= 10:
            break
    print('---')
