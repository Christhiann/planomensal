from pathlib import Path
from docx import Document

p = Path('backend/generated')
files = sorted(p.glob('plano_mensal_*.docx'))
if not files:
    print('no generated files')
    raise SystemExit(1)
file = files[-1]
print('inspecting', file)
d = Document(file)
# Examine TABLE 1 (index 1) rows around METODOLOGIA
table = d.tables[1]
for r in range(len(table.rows)):
    row = table.rows[r]
    for c in range(len(row.cells)):
        cell = row.cells[c]
        print(f'CELL {1}.{r}.{c} TEXT={repr(cell.text)}')
        for pi, para in enumerate(cell.paragraphs):
            print(f'  para {pi} text={repr(para.text)} runs={len(para.runs)}')
            for rj, run in enumerate(para.runs):
                print(f'    run {rj}: {repr(run.text)}')
    if r>=5:
        break
