from pydantic import BaseModel


class InformacionFormacionDTO(BaseModel):
    Regional: str = ""
    CentroFormacion: str = ""
    Convocatoria: str = ""
    Ficha: str = ""
    Programa: str = ""
    Modalidad: str = ""
    FechaInicioFicha: str = ""
    FechaFinFicha: str = ""
    PorcentajeAvanceActual: str = ""
    CorreoCentroFormacion: str = ""


class InformacionConvocatorioDTO(BaseModel):
    EstadoListadoSENA: str = ""
    ResponsablePago: str = ""


class AprendizCreateDTO(BaseModel):
    Nombre: str = ""
    NroDocumento: str = ""
    TipoDocumento: str = ""
    CorreoPersonal: str = ""
    InformacionFormacion: InformacionFormacionDTO
    InformacionConvocatorio: InformacionConvocatorioDTO

    model_config = {"populate_by_name": True, "extra": "allow"}


class UserUploadResponseDTO(BaseModel):
    inserted_count: int
    updated_count: int
    total_rows: int
    errors: list[str]
    warnings: list[str] = []
