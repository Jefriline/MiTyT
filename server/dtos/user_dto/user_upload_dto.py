from pydantic import BaseModel, Field


class InformacionFormacionDTO(BaseModel):
    Regional: str
    CentroFormacion: str
    CorreoContacto: str
    Ficha: str
    Programa: str
    Modalidad: str
    Avance: str


class InformacionConvocatorioDTO(BaseModel):
    Convocatoria: str
    EstadoTerminos: str
    EstadoConvocatoria: str
    ResponablePago: str
    Observaciones: str


class AprendizCreateDTO(BaseModel):
    Nombre: str
    TipoDocumento: str
    nro_documento: str = Field(alias="Nro-Documento")
    Correo: str
    InformacionFormacion: InformacionFormacionDTO
    InformacionConvocatorio: InformacionConvocatorioDTO

    model_config = {"populate_by_name": True, "extra": "forbid"}


class UserUploadResponseDTO(BaseModel):
    inserted_count: int
    updated_count: int
    total_rows: int
    errors: list[str]
    warnings: list[str] = []