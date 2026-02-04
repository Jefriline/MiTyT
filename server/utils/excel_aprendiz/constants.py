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

MAX_FILAS_EXCEL = 3500
BATCH_SIZE_UPLOAD = 250
