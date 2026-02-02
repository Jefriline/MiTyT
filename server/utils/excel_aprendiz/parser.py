from io import BytesIO

from openpyxl import load_workbook

NORMALIZADO_A_CANONICO: dict[str, str] = {
    "nombre": "Nombre",
    "tipodocumento": "TipoDocumento",
    "nrodocumento": "Nro-Documento",
    "nro-documento": "Nro-Documento",
    "correo": "Correo",
    "regional": "Regional",
    "centroformacion": "CentroFormacion",
    "correocontacto": "CorreoContacto",
    "ficha": "Ficha",
    "programa": "Programa",
    "modalidad": "Modalidad",
    "avance": "Avance",
    "convocatoria": "Convocatoria",
    "estadoterminos": "EstadoTerminos",
    "estadoconvocatoria": "EstadoConvocatoria",
    "responablepago": "ResponablePago",
    "responsablepago": "ResponablePago",
    "observaciones": "Observaciones",
}

CANONICOS_REQUERIDOS = frozenset(NORMALIZADO_A_CANONICO.values())

def _primary_norm_por_canonico() -> dict[str, str]:
    canonico_a_norms: dict[str, list[str]] = {}
    for norm, canon in NORMALIZADO_A_CANONICO.items():
        canonico_a_norms.setdefault(canon, []).append(norm)
    return {c: max(norms, key=len) for c, norms in canonico_a_norms.items()}

PRIMARY_NORM_POR_CANONICO = _primary_norm_por_canonico()

CANONICO_A_INDICES_KEY: dict[str, str] = {
    "Nombre": "nombre",
    "TipoDocumento": "tipodocumento",
    "Nro-Documento": "nrodocumento",
    "Correo": "correo",
    "Regional": "regional",
    "CentroFormacion": "centroformacion",
    "CorreoContacto": "correocontacto",
    "Ficha": "ficha",
    "Programa": "programa",
    "Modalidad": "modalidad",
    "Avance": "avance",
    "Convocatoria": "convocatoria",
    "EstadoTerminos": "estadoterminos",
    "EstadoConvocatoria": "estadoconvocatoria",
    "ResponablePago": "responablepago",
    "Observaciones": "observaciones",
}

CAMPOS_OBLIGATORIOS_NORMALIZADOS = ("nrodocumento", "correo", "ficha", "estadoconvocatoria")

MENSAJE_HEADERS_FALTANTES = (
    "La primera fila debe tener columnas que correspondan (ignorando mayusculas y espacios) a: "
    "Nombre, TipoDocumento, Nro-Documento, Correo, Regional, CentroFormacion, CorreoContacto, "
    "Ficha, Programa, Modalidad, Avance, Convocatoria, EstadoTerminos, EstadoConvocatoria, "
    "ResponablePago, Observaciones."
)


def _normalizar_header(celda: object) -> str:
    if celda is None:
        return ""
    return str(celda).strip().lower().replace(" ", "")


def _celda_str(value: object) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _columna_coincide_canonico(col_norm: str, canonico: str) -> bool:
    if col_norm in NORMALIZADO_A_CANONICO and NORMALIZADO_A_CANONICO[col_norm] == canonico:
        return True
    primary = PRIMARY_NORM_POR_CANONICO.get(canonico, "")
    return bool(primary and (primary.startswith(col_norm) or col_norm.startswith(primary)))


def _indices_headers(header_row: tuple) -> dict[str, int] | None:
    columnas: list[tuple[int, str]] = []
    for idx, celda in enumerate(header_row):
        norm = _normalizar_header(celda)
        if norm:
            columnas.append((idx, norm))

    indices: dict[str, int] = {}
    canonicos_orden = sorted(
        CANONICOS_REQUERIDOS,
        key=lambda c: len(PRIMARY_NORM_POR_CANONICO.get(c, "")),
        reverse=True,
    )
    for canonico in canonicos_orden:
        candidatos = [
            (idx, col_norm)
            for idx, col_norm in columnas
            if idx not in indices.values() and _columna_coincide_canonico(col_norm, canonico)
        ]
        if not candidatos:
            return None
        exactos = [c for c in candidatos if c[1] in NORMALIZADO_A_CANONICO and NORMALIZADO_A_CANONICO[c[1]] == canonico]
        elegido = exactos[0] if exactos else max(candidatos, key=lambda c: len(c[1]))
        idx_elegido = elegido[0]
        indices[CANONICO_A_INDICES_KEY[canonico]] = idx_elegido

    return indices


def _fila_a_aprendiz(row: tuple, indices: dict[str, int]) -> dict | None:
    def valor(norm: str) -> str:
        idx = indices.get(norm, -1)
        return _celda_str(row[idx] if idx >= 0 and idx < len(row) else None)

    for campo in CAMPOS_OBLIGATORIOS_NORMALIZADOS:
        if not valor(campo):
            return None

    informacion_formacion = {
        "Regional": valor("regional"),
        "CentroFormacion": valor("centroformacion"),
        "CorreoContacto": valor("correocontacto"),
        "Ficha": valor("ficha"),
        "Programa": valor("programa"),
        "Modalidad": valor("modalidad"),
        "Avance": valor("avance"),
    }
    informacion_convocatorio = {
        "Convocatoria": valor("convocatoria"),
        "EstadoTerminos": valor("estadoterminos"),
        "EstadoConvocatoria": valor("estadoconvocatoria"),
        "ResponablePago": valor("responablepago"),
        "Observaciones": valor("observaciones"),
    }
    return {
        "Nombre": valor("nombre"),
        "TipoDocumento": valor("tipodocumento"),
        "Nro-Documento": valor("nrodocumento"),
        "Correo": valor("correo"),
        "InformacionFormacion": informacion_formacion,
        "InformacionConvocatorio": informacion_convocatorio,
    }


def parse_excel_to_aprendices(file_stream: bytes) -> tuple[list[dict], list[str]]:
    errors: list[str] = []
    rows_to_insert: list[dict] = []

    workbook = load_workbook(filename=BytesIO(file_stream), read_only=True, data_only=True)
    sheet = workbook.active
    if not sheet:
        workbook.close()
        return [], ["El archivo no tiene hojas o esta vacio"]

    rows_iter = sheet.iter_rows(min_row=1, values_only=True)
    header_row = next(rows_iter, None)
    if not header_row:
        workbook.close()
        return [], ["El archivo no tiene filas"]

    indices = _indices_headers(header_row)
    if indices is None:
        workbook.close()
        return [], [MENSAJE_HEADERS_FALTANTES]

    for row_index, row in enumerate(rows_iter, start=2):
        if row is None:
            continue
        aprendiz = _fila_a_aprendiz(row, indices)
        if aprendiz is None:
            errors.append(
                f"Fila {row_index}: faltan Nro-Documento, Correo, Ficha o EstadoConvocatoria"
            )
            continue
        rows_to_insert.append(aprendiz)

    workbook.close()
    return rows_to_insert, errors
