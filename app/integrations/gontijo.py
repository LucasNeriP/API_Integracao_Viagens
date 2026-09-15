from app.integrations.base import IntegracaoCompanhia
from app.integrations.registry import registrar_integracao
from app.normalizacao import (
    NomesDosCampos,
    aplicar_regras_comuns,
    exigir_campos,
    exigir_objeto,
    interpretar_data_iso,
    minutos_de_segundos,
    normalizar_categoria,
    para_inteiro,
    para_iso8601,
    preco_de_decimal,
)
from app.schemas import montar_viagem_normalizada


@registrar_integracao
class IntegracaoGontijo(IntegracaoCompanhia):
    """
    Estratégia da Gontijo.

    O payload usa camelCase em inglês, objetos from/to/fare e duração em segundos.
    As datas chegam em UTC (sufixo Z) e são convertidas para America/Bahia.
    O campo serviceCode é exclusivo desta companhia.
    """

    nome_empresa = "Gontijo"

    CAMPOS_OBRIGATORIOS = [
        "serviceCode",
        "from",
        "to",
        "departure",
        "arrival",
        "estimatedDurationSeconds",
        "fare",
        "serviceClass",
        "availableSeats",
    ]

    NOMES_DOS_CAMPOS = NomesDosCampos(
        partida="departure",
        chegada="arrival",
        duracao="estimatedDurationSeconds",
        preco="fare.amount",
        assentos="availableSeats",
        uf_origem="from.state",
        uf_destino="to.state",
        categoria="serviceClass",
    )

    def reconhecer(self, payload: dict) -> bool:
        return "serviceCode" in payload

    def _extrair(self, payload: dict) -> dict:
        origem = exigir_objeto(payload, "from")
        destino = exigir_objeto(payload, "to")
        tarifa = exigir_objeto(payload, "fare")

        exigir_campos(origem, ["city", "state"], prefixo="from")
        exigir_campos(destino, ["city", "state"], prefixo="to")
        exigir_campos(tarifa, ["amount", "currency"], prefixo="fare")

        return {
            "id_viagem": str(payload["serviceCode"]),
            "cidade_origem": str(origem["city"]).strip(),
            "uf_origem": str(origem["state"]).strip().upper(),
            "cidade_destino": str(destino["city"]).strip(),
            "uf_destino": str(destino["state"]).strip().upper(),
            "partida": interpretar_data_iso(payload["departure"], "departure"),
            "chegada": interpretar_data_iso(payload["arrival"], "arrival"),
            "duracao_minutos": minutos_de_segundos(
                payload["estimatedDurationSeconds"],
                "estimatedDurationSeconds",
            ),
            "preco": preco_de_decimal(tarifa["amount"], "fare.amount"),
            "moeda": str(tarifa["currency"]).strip().upper(),
            "categoria": normalizar_categoria(payload["serviceClass"], "serviceClass"),
            "assentos": para_inteiro(payload["availableSeats"], "availableSeats"),
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
