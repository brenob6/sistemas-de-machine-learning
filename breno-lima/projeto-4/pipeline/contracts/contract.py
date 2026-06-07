from pydantic import BaseModel


class IndicadoresContract(BaseModel):
    lucro_liquido: float
    roe: float
    lucro_liquido_recorrente: float
    lucro_liquido_por_acao: float
    divida_liquida: float
    patrimonio_liquido: float
    nav: float
    valor_mercado: float
    volume_medio_diario: float


class ResultadoIndividualContract(BaseModel):
    itau: float
    dexco: float
    alpargatas: float
    motiva: float
    aegea: float
    copa_engenharia: float

    despesas_administrativas: float
    despesas_tributarias: float
    doacoes: float


class ItausaContract(BaseModel):
    def __init__(self, **data):
        super().__init__(**data)

    indicadores: IndicadoresContract
    resultado_individual: ResultadoIndividualContract
