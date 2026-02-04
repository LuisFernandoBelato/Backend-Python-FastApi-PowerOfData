from dataclasses import dataclass
from typing import Optional
from fastapi import Query

@dataclass
class PeopleQueryParams:
    # Parametros nativos da api SWAPI
    id: Optional[int] = Query(None, description="ID da pessoa na SWAPI")
    name: Optional[str] | None = Query(None, description="Busca pelo nome da pessoa")

    # Parametros personalizados para busca dos relacionamentos sob demanda
    films: Optional[bool] = Query(None, description="Busca também os filmes relacionados aquela pessoa")
    species: Optional[bool] = Query(None, description="Busca também as espécies relacionadas aquela pessoa")
    starships: Optional[bool] = Query(None, description="Busca também as naves espaciais relacionadas aquela pessoa")
    vehicles: Optional[bool] = Query(None, description="Busca também os veículos relacionados aquela pessoa")
    
    # Parametro que inclui todas os relacionamentos
    all: Optional[bool] = Query(None, description="Inclui todos os relacionamentos na resposta")
    order: Optional[str] = Query(None, description="Ordena os resultados pelo campo especificado") # 'ASC' ou 'DESC'

    # def __post_init__(self):
    #     """Converte descriptors Query em valores padrão para uso fora do FastAPI."""
    #     for field_name in self.__dataclass_fields__:
    #         value = getattr(self, field_name)
    #         if isinstance(value, Query):
    #             setattr(self, field_name, value.default)