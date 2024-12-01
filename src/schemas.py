from pydantic import BaseModel
from datetime import datetime


class DimProductSchema(BaseModel):
    id: str
    produto: str
    id_familia: str
    id_grupo: str
    id_subgrupo: str
    familia_descricao: str
    grupo_descricao: str
    subgrupo_descricao: str

class FactSalesSchema(BaseModel):
    id_produto: str
    data: datetime
    faturamento: float
    quantidade: int

class FactMarginSchema(BaseModel):
    id_produto: str
    data: datetime
    valor_margem: float
    
class FactStorageSchema(BaseModel):
    id_produto: str
    quantidade: float