from dataclasses import dataclass
from typing import Optional
from fastapi import Query
from fastapi.params import Param

@dataclass
class StarshipsQueryParams:
    # Parametros nativos da api SWAPI
    id: Optional[int] = Query(None, description="ID da nave espacial na SWAPI")
    name: Optional[str] = Query(None, description="Busca pelo nome da nave espacial")
    model: Optional[str] = Query(None, description="Busca pelo modelo da nave espacial")

    # Parametros personalizados para busca dos relacionamentos sob demanda
    films: Optional[bool] = Query(None, description="Busca também os filmes relacionados aquela nave espacial")
    pilots: Optional[bool] = Query(None, description="Busca também os pilotos relacionados aquela nave espacial")
    
    # Parametro que inclui todas os relacionamentos
    all: Optional[bool] = Query(None, description="Inclui todos os relacionamentos na resposta")
    order: Optional[str] = Query(None, description="Ordena os resultados pelo campo especificado") # 'ASC' ou 'DESC'

    def __post_init__(self):
        """Converte descriptors Query em valores padrão para uso fora do FastAPI."""
        for field_name in self.__dataclass_fields__:
            value = getattr(self, field_name)
            if isinstance(value, Param):
                setattr(self, field_name, value.default)