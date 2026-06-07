from pydantic import BaseModel


class IndicadoresOperacionaisContract(BaseModel):
    vso_liquida: float
    repasse: float
    vendas_financiadas: float
    producao: float


class MRVContract(BaseModel):
    def __init__(self, **data):
        super().__init__(**data)

    indicadores_operacionais: IndicadoresOperacionaisContract
