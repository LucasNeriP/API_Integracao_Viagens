from pydantic import BaseModel


class Localidade(BaseModel):
    cidade: str
    uf: str


class Preco(BaseModel):
    valor: float
    moeda: str


class ViagemNormalizada(BaseModel):
    id_viagem: str
    empresa: str
    origem: Localidade
    destino: Localidade
    partida: str
    chegada: str
    duracao_minutos: int
    preco: Preco
    categoria: str
    assentos_disponiveis: int


class RespostaNormalizacao(BaseModel):
    total: int
    viagens: list[ViagemNormalizada]


class DetalheDoErro(BaseModel):
    indice: int
    empresa_identificada: str | None = None
    campo: str | None = None
    mensagem: str


def montar_viagem_normalizada(
    id_viagem: str,
    empresa: str,
    cidade_origem: str,
    uf_origem: str,
    cidade_destino: str,
    uf_destino: str,
    partida: str,
    chegada: str,
    duracao_minutos: int,
    preco: float,
    moeda: str,
    categoria: str,
    assentos_disponiveis: int,
) -> dict:
    """Monta o dicionário no contrato homogêneo de saída."""

    viagem = ViagemNormalizada(
        id_viagem=id_viagem,
        empresa=empresa,
        origem=Localidade(cidade=cidade_origem, uf=uf_origem),
        destino=Localidade(cidade=cidade_destino, uf=uf_destino),
        partida=partida,
        chegada=chegada,
        duracao_minutos=duracao_minutos,
        preco=Preco(valor=preco, moeda=moeda),
        categoria=categoria,
        assentos_disponiveis=assentos_disponiveis,
    )
    return viagem.model_dump()
