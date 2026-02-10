from utils.excel_aprendiz.constants import (
    CANONICO_A_INDICES_KEY,
    CANONICOS_OPCIONALES,
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

    for canonico in CANONICOS_OPCIONALES:
        candidatos = [
            (idx, col_norm)
            for idx, col_norm in columnas
            if idx not in indices.values() and _columna_coincide_canonico(col_norm, canonico)
        ]
        if not candidatos:
            continue
        exactos = [
            c
            for c in candidatos
            if c[1] in NORMALIZADO_A_CANONICO and NORMALIZADO_A_CANONICO[c[1]] == canonico
        ]
        elegido = exactos[0] if exactos else max(candidatos, key=lambda c: len(c[1]))
        indices[CANONICO_A_INDICES_KEY[canonico]] = elegido[0]

    return indices


def _fila_a_aprendiz(row: tuple, indices: dict[str, int]) -> dict | None:
    def valor(norm: str) -> str:
        idx = indices.get(norm, -1)
        return _celda_str(row[idx] if idx >= 0 and idx < len(row) else None)

    for campo in CAMPOS_OBLIGATORIOS_NORMALIZADOS:
        if not valor(campo):
            return None

    primer_nombre = valor("primernombre")
    segundo_nombre = valor("segundonombre")
    primer_apellido = valor("primerapellido")
    segundo_apellido = valor("segundoapellido")
    nombre_completo = " ".join(
        p for p in (primer_nombre, segundo_nombre, primer_apellido, segundo_apellido) if p
    ).strip() or valor("nrodocumento")

    informacion_formacion = {
        "Regional": valor("regional"),
        "CentroFormacion": valor("centroformacion"),
        "Convocatoria": valor("convocatoria"),
        "Ficha": valor("ficha"),
        "Programa": valor("programa"),
        "Modalidad": valor("modalidad"),
        "FechaInicioFicha": valor("fechainicioficha"),
        "FechaFinFicha": valor("fechafinficha"),
        "PorcentajeAvanceActual": valor("porcentajeavanceactual"),
        "CorreoCentroFormacion": valor("correocentroformacion"),
    }

    informacion_convocatorio = {
        "EstadoListadoSENA": valor("estadolistadosena"),
        "ResponsablePago": valor("responsablepago"),
        "Observaciones": valor("observaciones"),
    }

    return {
        "Nombre": nombre_completo,
        "NroDocumento": valor("nrodocumento"),
        "TipoDocumento": valor("tipodocumento"),
        "CorreoPersonal": valor("correopersonal"),
        "InformacionFormacion": informacion_formacion,
        "InformacionConvocatorio": informacion_convocatorio,
        "UsuarioPrisma": valor("usuarioprisma"),
        "ContrasenaPRISMA": valor("contrasenaprisma"),
        "PrimerApellido": primer_apellido,
        "SegundoApellido": segundo_apellido,
        "PrimerNombre": primer_nombre,
        "SegundoNombre": segundo_nombre,
        "PaisResidencia": valor("paisresidencia"),
        "DepartamentoResidencia": valor("departamentoresidencia"),
        "CiudadResidencia": valor("ciudadresidencia"),
        "EstadoAprendiz": valor("estadoaprendiz"),
        "AplicoBeneficioPagoAnteriormente": valor("aplicobeneficiopagoanteriormente"),
        "DatosBeneficioAplicado": valor("datosbeneficioaplicado"),
        "EstadoInscripcion": valor("estadoinscripcion"),
    }
