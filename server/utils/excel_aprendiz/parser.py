from io import BytesIO

from openpyxl import load_workbook

from utils.excel_aprendiz.constants import (
    MAX_FILAS_BUSCAR_HEADER,
    MAX_FILAS_EXCEL,
    MENSAJE_HEADERS_FALTANTES,
)
from utils.excel_aprendiz.normalize import normalize_document_key
from utils.excel_aprendiz.row_mapper import _fila_a_aprendiz, _indices_headers


def _buscar_fila_encabezados(sheet) -> tuple[tuple | None, int]:
    """
    Busca en las primeras filas la que contiene los encabezados requeridos.
    Devuelve (header_row, 1-based_row_index) o (None, 0) si no encuentra.
    """
    primeras_filas = list(
        sheet.iter_rows(min_row=1, max_row=MAX_FILAS_BUSCAR_HEADER, values_only=True)
    )
    for idx, fila in enumerate(primeras_filas):
        if fila is None:
            continue
        if _indices_headers(fila) is not None:
            return (fila, idx + 1)
    return (None, 0)


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

    header_row, header_row_index = _buscar_fila_encabezados(sheet)
    if header_row is None or header_row_index == 0:
        workbook.close()
        return [], [MENSAJE_HEADERS_FALTANTES], []

    indices = _indices_headers(header_row)
    assert indices is not None

    data_start_row = header_row_index + 1
    rows_iter = sheet.iter_rows(min_row=data_start_row, values_only=True)

    for row_index, row in enumerate(rows_iter, start=data_start_row):
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
