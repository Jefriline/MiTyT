
NORMALIZADO_A_CANONICO: dict[str, str] = {
    "regional": "Regional",
    "centrodeformación": "CentroFormacion",
    "centroformacion": "CentroFormacion",
    "primerapellido": "PrimerApellido",
    "segundoapellido": "SegundoApellido",
    "primernombre": "PrimerNombre",
    "segundonombre": "SegundoNombre",
    "tipodocumento": "TipoDocumento",
    "nrodocumento": "NroDocumento",
    "nro.documento": "NroDocumento",
    "correopersonal": "CorreoPersonal",
    "paísresidencia": "PaisResidencia",
    "paisresidencia": "PaisResidencia",
    "departamentoresidencia": "DepartamentoResidencia",
    "ciudadresidencia": "CiudadResidencia",
    "programa": "Programa",
    "ficha": "Ficha",
    "fechainicioficha": "FechaInicioFicha",
    "fechafinficha": "FechaFinFicha",
    "modalidad": "Modalidad",
    "estadodelaprendiz": "EstadoAprendiz",
    "porcentajedeavanceactual": "PorcentajeAvanceActual",
    "aplicóbeneficiopagoanteriormente": "AplicoBeneficioPagoAnteriormente",
    "aplicobeneficiopagoanteriormente": "AplicoBeneficioPagoAnteriormente",
    "datosdelbeneficioaplicado": "DatosBeneficioAplicado",
    "estadolistadosena": "EstadoListadoSENA",
    "responsabledepago": "ResponsablePago",
    "usuarioprisma": "UsuarioPrisma",
    "contraseñaprisma": "ContrasenaPRISMA",
    "correodelcentroformación": "CorreoCentroFormacion",
    "correodelcentroformacion": "CorreoCentroFormacion",
}

CANONICOS_REQUERIDOS = frozenset({"NroDocumento", "CorreoPersonal", "Ficha", "EstadoListadoSENA"})


def _primary_norm_por_canonico() -> dict[str, str]:
    canonico_a_norms: dict[str, list[str]] = {}
    for norm, canon in NORMALIZADO_A_CANONICO.items():
        canonico_a_norms.setdefault(canon, []).append(norm)
    return {c: max(norms, key=len) for c, norms in canonico_a_norms.items()}


PRIMARY_NORM_POR_CANONICO = _primary_norm_por_canonico()

CANONICO_A_INDICES_KEY: dict[str, str] = {
    "Regional": "regional",
    "CentroFormacion": "centroformacion",
    "PrimerApellido": "primerapellido",
    "SegundoApellido": "segundoapellido",
    "PrimerNombre": "primernombre",
    "SegundoNombre": "segundonombre",
    "TipoDocumento": "tipodocumento",
    "NroDocumento": "nrodocumento",
    "CorreoPersonal": "correopersonal",
    "PaisResidencia": "paisresidencia",
    "DepartamentoResidencia": "departamentoresidencia",
    "CiudadResidencia": "ciudadresidencia",
    "Programa": "programa",
    "Ficha": "ficha",
    "FechaInicioFicha": "fechainicioficha",
    "FechaFinFicha": "fechafinficha",
    "Modalidad": "modalidad",
    "EstadoAprendiz": "estadoaprendiz",
    "PorcentajeAvanceActual": "porcentajeavanceactual",
    "AplicoBeneficioPagoAnteriormente": "aplicobeneficiopagoanteriormente",
    "DatosBeneficioAplicado": "datosbeneficioaplicado",
    "EstadoListadoSENA": "estadolistadosena",
    "ResponsablePago": "responsablepago",
    "UsuarioPrisma": "usuarioprisma",
    "ContrasenaPRISMA": "contrasenaprisma",
    "CorreoCentroFormacion": "correocentroformacion",
}

CANONICOS_OPCIONALES = frozenset(
    {
        "Regional", "CentroFormacion", "PrimerApellido", "SegundoApellido",
        "PrimerNombre", "SegundoNombre", "TipoDocumento", "PaisResidencia",
        "DepartamentoResidencia", "CiudadResidencia", "FechaInicioFicha", "FechaFinFicha",
        "Modalidad", "EstadoAprendiz", "PorcentajeAvanceActual",
        "AplicoBeneficioPagoAnteriormente", "DatosBeneficioAplicado", "ResponsablePago",
        "UsuarioPrisma", "ContrasenaPRISMA", "CorreoCentroFormacion", "Programa",
    }
)

CAMPOS_OBLIGATORIOS_NORMALIZADOS = ("nrodocumento", "correopersonal", "ficha", "estadolistadosena")

MENSAJE_HEADERS_FALTANTES = (
    "La primera fila debe tener columnas que correspondan (ignorando mayúsculas y espacios) a: "
    "Nro. Documento, Correo personal, Ficha, Estado Listado SENA. "
    "Opcionales: Regional, Centro de formación, Primer/Segundo Apellido/Nombre, Tipo Documento, "
    "País/Departamento/Ciudad Residencia, Programa, Fechas Ficha, Modalidad, Estado del Aprendiz, "
    "Porcentaje Avance, Beneficio Pago, Responsable de Pago, Usuario Prisma, Contraseña PRISMA, "
    "Correo del centro formación."
)

MAX_FILAS_EXCEL = 3500
BATCH_SIZE_UPLOAD = 250
