from dataclasses import dataclass
from typing import Optional
from fastapi import Query
from fastapi.params import Param

@dataclass
class FilmsQueryParams:
    # Parametros nativos da api SWAPI
    id: Optional[int] = Query(None, description="ID do filme na SWAPI")
    title: Optional[str] = Query(None, description="Busca pelo título do filme")

    # Parametros personalizados para busca dos relacionamentos sob demanda
    characters: Optional[bool] = Query(None, description="Busca também os personagens relacionados aquele filme")
    planets: Optional[bool] = Query(None, description="Busca também os planetas relacionados aquele filme")
    starships: Optional[bool] = Query(None, description="Busca também as naves espaciais relacionadas aquele filme")
    vehicles: Optional[bool] = Query(None, description="Busca também os veículos relacionados aquele filme")
    species: Optional[bool] = Query(None, description="Busca também as espécies relacionadas aquele filme")

    # Parametro que inclui todas os relacionamentos
    all: Optional[bool] = Query(None, description="Inclui todos os relacionamentos na resposta")
    order: Optional[str] = Query(None, description="Ordena os resultados pelo campo especificado") # 'ASC' ou 'DESC'

    def __post_init__(self):
        """Converte descriptors Query em valores padrão para uso fora do FastAPI."""
        for field_name in self.__dataclass_fields__:
            value = getattr(self, field_name)
            if isinstance(value, Param):
                setattr(self, field_name, value.default)