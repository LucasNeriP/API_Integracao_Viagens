from app.integrations.base import IntegracaoCompanhia
from app.integrations.registry import registrar_integracao
from app.normalizacao import (
    NomesDosCampos,
    aplicar_regras_comuns,
    exigir_campos,
    exigir_objeto,
    interpretar_data_iso,
    normalizar_categoria,
    para_inteiro,
    para_iso8601,
    preco_de_centavos,
)
from app.schemas import montar_viagem_normalizada


@registrar_integracao
class IntegracaoRota(IntegracaoCompanhia):
    """
    Estratégia da Rota Transportes.

    O payload usa snake_case, objetos aninhados de origem/destino
    e o preço em centavos. O campo trip_id é exclusivo desta companhia.
    """

    nome_empresa = "Rota Transportes"

    CAMPOS_OBRIGATORIOS = [
        "trip_id",
        "origem",
        "destino",
        "partida_em",
        "chegada_em",
        "duracao_minutos",
        "tarifa_centavos",
        "moeda",
        "classe",
        "vagas",
    ]

    NOMES_DOS_CAMPOS = NomesDosCampos(
        partida="partida_em",
        chegada="chegada_em",
        duracao="duracao_minutos",
        preco="tarifa_centavos",
        assentos="vagas",
        uf_origem="origem.estado",
        uf_destino="destino.estado",
        categoria="classe",
    )

    def reconhecer(self, payload: dict) -> bool:
        return "trip_id" in payload

    def _extrair(self, payload: dict) -> dict:
        origem = exigir_objeto(payload, "origem")
        destino = exigir_objeto(payload, "destino")
        exigir_campos(origem, ["municipio", "estado"], prefixo="origem")
        exigir_campos(destino, ["municipio", "estado"], prefixo="destino")

        return {
            "id_viagem": str(payload["trip_id"]),
            "cidade_origem": str(origem["municipio"]).strip(),
            "uf_origem": str(origem["estado"]).strip().upper(),
            "cidade_destino": str(destino["municipio"]).strip(),
            "uf_destino": str(destino["estado"]).strip().upper(),
            "partida": interpretar_data_iso(payload["partida_em"], "partida_em"),
            "chegada": interpretar_data_iso(payload["chegada_em"], "chegada_em"),
            "duracao_minutos": para_inteiro(payload["duracao_minutos"], "duracao_minutos"),
            "preco": preco_de_centavos(payload["tarifa_centavos"], "tarifa_centavos"),
            "moeda": str(payload["moeda"]).strip().upper(),
            "categoria": normalizar_categoria(payload["classe"], "classe"),
            "assentos": para_inteiro(payload["vagas"], "vagas"),
        }

    def validar(self, payload: dict) -> None:
        exigir_campos(payload, self.CAMPOS_OBRIGATORIOS)
        dados = self._extrair(payload)
        aplicar_regras_comuns(
            partida=dados["partida"],
            chegada=dados["chegada"],
            duracao_minutos=dados["duracao_minutos"],
            preco=dados["preco"],
            assentos=dados["assentos"],
            uf_origem=dados["uf_origem"],
            uf_destino=dados["uf_destino"],
            campos=self.NOMES_DOS_CAMPOS,
        )

    def normalizar(self, payload: dict) -> dict:
        dados = self._extrair(payload)
        return montar_viagem_normalizada(
            id_viagem=dados["id_viagem"],
            empresa=self.nome_empresa,
            cidade_origem=dados["cidade_origem"],
            uf_origem=dados["uf_origem"],
            cidade_destino=dados["cidade_destino"],
            uf_destino=dados["uf_destino"],
            partida=para_iso8601(dados["partida"]),
            chegada=para_iso8601(dados["chegada"]),
            duracao_minutos=dados["duracao_minutos"],
            preco=dados["preco"],
            moeda=dados["moeda"],
            categoria=dados["categoria"],
            assentos_disponiveis=dados["assentos"],
        )
