from pydantic import BaseModel, Extra
from typing import List

class MovieItem(BaseModel):
    class config:
        extra = Extra.forbid
    
    title: str
    worldwide_lifetime_gross: str
    domestic_lifetime_gross: str
    international_lifetime_gross: str
    year: str
    rank: str
    movie_url: str
    movie_id: str
    
class CrewItem(BaseModel):
    class config:
        extra = Extra.forbid

    crew_id: str
    name: str
    role: str
    
class CastItem(BaseModel):
    class config:
        extra = Extra.forbid

    cast_id: str
    name: str
    role: str
    
class MovieDetails(BaseModel):
    id: str
    info: MovieItem
    crew: List[CrewItem]
    cast: List[CastItem]
