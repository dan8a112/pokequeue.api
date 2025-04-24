from pydantic import BaseModel, Field
from typing import Optional


class PokeRequest(BaseModel):
    
    id: Optional[int] = Field(
        default=None,
        ge=1,
        description="ID de la petición"
    )

    pokemon_type: Optional[str] = Field(
        default=None,
        description="Tipo de Pokémon",
        pattern="^[a-zA-Z0-9_]+$"
    )

    url: Optional[str] = Field(
        default=None,
        description="URL del Pokémon",
        pattern="^https?://[a-zA-Z0-9_./-]+$"
    )

    status: Optional[str] = Field(
        default=None,
        description="Estado de la petición",
        pattern="^(sent|completed|inprogress|failed)$"
    ) 

    sample_size: Optional[int] = Field(
        default=None,
        gt=0,
        description="Tamaño de muestra (debe ser > 0)"
    )