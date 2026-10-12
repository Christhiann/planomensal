import re
from datetime import datetime
from pathlib import Path

from docx import Document
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, field_validator

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = (BASE_DIR.parent / "templates" / "PLANO MENSAL CMT XLVII.docx").resolve()
OUTPUT_DIR = BASE_DIR / "generated"
OUTPUT_DIR.mkdir(exist_ok=True)

app = FastAPI(
    title="Plano Mensal API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)


class PlanoData(BaseModel):
    componente: str
    nomeArquivo: str = Field(min_length=1, max_length=120)
    professor: str
    ano: str
    turma: str
    periodo: str
    objetivos: str
    habilidades: str
    objetosConhecimento: str
    metodologia: str
    recursos: str
    avaliacoes: str
    referencias: str = ""
    assinaturaProfessor: str = ""

    @field_validator("nomeArquivo")
    @classmethod
    def validar_nome_arquivo(cls, value: str) -> str:
        nome = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "-", value).strip(" .")
        nome = re.sub(r"\.docx$", "", nome, flags=re.IGNORECASE).strip(" .")
        if not nome:
            raise ValueError("Informe um nome de arquivo válido.")
        return nome


def _build_replacements(data: PlanoData) -> dict[str, str]:
    return {
        # Keep only explicit placeholder-based replacements here.
        # Plain label replacements (e.g. "COMPONENTE") were removed because
        # they caused label text to be overwritten. Label-based insertion
        # is handled separately by `_fill_fields_by_label` which writes
        # values into the adjacent/appropriate cell instead of replacing labels.
        "{{componente}}": data.componente,
        "{{professor}}": data.professor,
        "{{ano}}": data.ano,
        "{{turma}}": data.turma,
        "{{periodo}}": data.periodo,
        "{{objetivos}}": data.objetivos,
        "{{habilidades}}": data.habilidades,
        "{{objetosConhecimento}}": data.objetosConhecimento,
        "{{metodologia}}": data.metodologia,
        "{{recursos}}": data.recursos,
        "{{avaliacoes}}": data.avaliacoes,
        "{{referencias}}": data.referencias,
        "{{assinaturaProfessor}}": data.assinaturaProfessor,
    }


def _replace_in_paragraph(paragraph, replacements: dict[str, str]) -> None:
    for run in paragraph.runs:
        original_text = run.text or ""
        if not original_text:
            continue

        updated_text = original_text
        for token, value in replacements.items():
            if value:
                updated_text = updated_text.replace(token, value)

        if updated_text != original_text:
            run.text = updated_text


def _replace_in_document(document: Document, replacements: dict[str, str]) -> None:
    for paragraph in document.paragraphs:
        _replace_in_paragraph(paragraph, replacements)

    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    _replace_in_paragraph(paragraph, replacements)


def _set_cell_text(cell, text: str) -> None:
    if not text:
        return

    # Prefer writing into the first paragraph to preserve cell styling.
    if cell.paragraphs:
        para = cell.paragraphs[0]
        # Replace paragraph text (this recreates runs but preserves paragraph style).
        para.text = text
    else:
        cell.add_paragraph(text)


def _fill_fields_by_label(document: Document, data: PlanoData) -> None:
    """Locate label cells (e.g. 'COMPONENTE', 'PROFESSOR', etc.) and
    write the corresponding value into the intended adjacent/nearby cell
    instead of replacing the label itself.

    Strategy (minimal, template-aware):
    - If a label cell has a right neighbor, write into that neighbor.
    - Else if the cell below is empty, write into the below cell (useful for
      header->content patterns).
    - Else if the left neighbor is empty, use left.
    - Else append after the label in the same cell (preserving label text).
    """
    label_map = {
        "COMPONENTE": data.componente,
        "PROFESSOR": data.professor,
        "ANO": data.ano,
        "TURMA": data.turma,
        "PERIODO": data.periodo,
        "PERÍODO": data.periodo,
        "OBJETIVOS": data.objetivos,
        "HABILIDADES": data.habilidades,
        "OBJETOS DO CONHECIMENTO": data.objetosConhecimento,
        "METODOLOGIA": data.metodologia,
        "METODOLOGIA/ESTRATÉGIAS DIDÁTICAS": data.metodologia,
        "RECURSOS DIDÁTICOS": data.recursos,
        "AVALIAÇÕES": data.avaliacoes,
        "REFERÊNCIAS": data.referencias,
        "ASSINATURA PROFESSOR(A)": data.assinaturaProfessor,
        "ASSINATURA PROFESSOR (A)": data.assinaturaProfessor,
        "ASSINATURA PROFESSOR": data.assinaturaProfessor,
    }

    for table in document.tables:
        nrows = len(table.rows)
        ncols = len(table.columns)
        for r_idx, row in enumerate(table.rows):
            for c_idx, cell in enumerate(row.cells):
                cell_text = (cell.text or "").strip()
                if not cell_text:
                    continue

                # Normalize label
                norm = cell_text.strip().upper()
                # Remove trailing colon and extra spaces
                if norm.endswith(":"):
                    norm = norm[:-1].strip()

                # Try to match any label key (exact match)
                if norm in label_map and label_map[norm]:
                    value = label_map[norm]

                    # Prefer right neighbor
                    target = None
                    if c_idx + 1 < ncols:
                        right = table.rows[r_idx].cells[c_idx + 1]
                        if (right.text or "").strip() == "":
                            target = right

                    # If not right, prefer cell below (useful for header->content)
                    if target is None and r_idx + 1 < nrows:
                        below = table.rows[r_idx + 1].cells[c_idx]
                        if (below.text or "").strip() == "":
                            target = below

                    # If still none, prefer left empty
                    if target is None and c_idx - 1 >= 0:
                        left = table.rows[r_idx].cells[c_idx - 1]
                        if (left.text or "").strip() == "":
                            target = left
                    # For planning fields, prefer writing only into the
                    # designated content area (do NOT append to the label).
                    planning_keys = {
                        "OBJETIVOS",
                        "HABILIDADES",
                        "OBJETOS DO CONHECIMENTO",
                        "METODOLOGIA",
                        "METODOLOGIA/ESTRATÉGIAS DIDÁTICAS",
                        "RECURSOS DIDÁTICOS",
                        "AVALIAÇÕES",
                        "REFERÊNCIAS",
                    }

                    if target is None and norm in planning_keys:
                        # try to find a content cell further below in same column
                        for rr in range(r_idx + 1, nrows):
                            cand = table.rows[rr].cells[c_idx]
                            if (cand.text or "").strip() == "":
                                target = cand
                                break

                    # If still none and field is NOT a planning key, allow appending
                    if target is None and norm not in planning_keys:
                        # Keep original label text exactly as-is and append a space + value
                        for para in cell.paragraphs:
                            if (para.text or "").strip():
                                para.text = para.text + " " + value
                                break
                        else:
                            _set_cell_text(cell, cell_text + " " + value)
                    elif target is not None:
                        _set_cell_text(target, value)


def generate_document_from_template(
    data: PlanoData,
    template_path: Path = TEMPLATE_PATH,
    output_path: Path | None = None,
) -> Path:
    if not template_path.exists():
        raise FileNotFoundError(f"Template não encontrado: {template_path}")

    document = Document(template_path)
    replacements = _build_replacements(data)
    _replace_in_document(document, replacements)
    # Also fill fields located by labels into adjacent cells
    _fill_fields_by_label(document, data)

    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = OUTPUT_DIR / f"plano_mensal_{timestamp}.docx"

    document.save(output_path)
    return output_path


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/planos")
def criar_plano(data: PlanoData):
    try:
        output_path = generate_document_from_template(data)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return FileResponse(
        output_path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=f"{data.nomeArquivo}.docx",
    )
