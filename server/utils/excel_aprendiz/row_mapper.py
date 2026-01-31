from utils.excel_aprendiz.constants import (
    CANONICO_A_INDICES_KEY,
    CANONICOS_REQUERIDOS,
    CAMPOS_OBLIGATORIOS_NORMALIZADOS,
    NORMALIZADO_A_CANONICO,
    PRIMARY_NORM_POR_CANONICO,
)
from utils.excel_aprendiz.normalize import _celda_str, _normalizar_header


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
        exactos = [
            c
            for c in candidatos
            if c[1] in NORMALIZADO_A_CANONICO and NORMALIZADO_A_CANONICO[c[1]] == canonico
        ]
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
