from io import BytesIO

from openpyxl import load_workbook

from utils.excel_aprendiz.constants import (
    MAX_FILAS_EXCEL,
    MENSAJE_HEADERS_FALTANTES,
)
from utils.excel_aprendiz.normalize import normalize_document_key
from utils.excel_aprendiz.row_mapper import _fila_a_aprendiz, _indices_headers


def parse_excel_to_aprendices(
    file_stream: bytes,
) -> tuple[list[dict], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    rows_deduped: list[dict] = []
    seen_docs: dict[str, int] = {}

    workbook = load_workbook(filename=BytesIO(file_stream), read_only=True, data_only=True)
    sheet = workbook.active
    if not sheet:
        workbook.close()
        return [], ["El archivo no tiene hojas o está vacío"], []

    rows_iter = sheet.iter_rows(min_row=1, values_only=True)
    header_row = next(rows_iter, None)
    if not header_row:
        workbook.close()
        return [], ["El archivo no tiene filas"], []

    indices = _indices_headers(header_row)
    if indices is None:
        workbook.close()
        return [], [MENSAJE_HEADERS_FALTANTES], []

    for row_index, row in enumerate(rows_iter, start=2):
        if row is None:
            continue
        if len(rows_deduped) >= MAX_FILAS_EXCEL:
            errors.append(
                f"Límite máximo de {MAX_FILAS_EXCEL} registros por archivo. "
                f"Se procesaron solo las primeras {MAX_FILAS_EXCEL} filas válidas. "
                f"Divida el Excel en archivos más pequeños."
            )
            break

        aprendiz = _fila_a_aprendiz(row, indices)
        if aprendiz is None:
            errors.append(
                f"Fila {row_index}: faltan Nro. Documento, Correo personal, Ficha o Estado Listado SENA"
            )
            continue

        raw_doc = aprendiz.get("NroDocumento", "")
        doc_key = normalize_document_key(raw_doc)
        if doc_key is None:
            errors.append(
                f"Fila {row_index}: Nro. Documento inválido o contiene caracteres prohibidos (. $ # [ ] /)"
            )
            continue

        if doc_key in seen_docs:
            prev_row = seen_docs[doc_key]
            warnings.append(
                f"Documento {doc_key} duplicado (filas {prev_row} y {row_index}). Se usa la última."
            )
        seen_docs[doc_key] = row_index

        aprendiz["_firebase_key"] = doc_key
        rows_deduped.append(aprendiz)

    workbook.close()
    return rows_deduped, errors, warnings
