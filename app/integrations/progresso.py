from app.integrations.base import IntegracaoCompanhia
from app.integrations.registry import registrar_integracao
from app.normalizacao import (
    NomesDosCampos,
    aplicar_regras_comuns,
    exigir_campos,
    interpretar_data_brasileira,
    minutos_de_hh_mm,
    normalizar_categoria,
    para_inteiro,
    para_iso8601,
    preco_de_texto_brasileiro,
)
from app.schemas import montar_viagem_normalizada


@registrar_integracao
class IntegracaoProgresso(IntegracaoCompanhia):
    """
    Estratégia da Auto Viação Progresso.

    O payload é plano, com nomes em português e datas no formato brasileiro.
    O campo codigoViagem é exclusivo desta companhia.
    """

    nome_empresa = "Auto Viação Progresso"

    CAMPOS_OBRIGATORIOS = [
        "codigoViagem",
        "cidadeOrigem",
        "ufOrigem",
        "cidadeDestino",
        "ufDestino",
        "dataHoraSaida",
        "dataHoraChegada",
        "fusoHorario",
        "tempoEstimado",
        "valorPassagem",
        "tipoServico",
        "assentosDisponiveis",
    ]

    NOMES_DOS_CAMPOS = NomesDosCampos(
        partida="dataHoraSaida",
        chegada="dataHoraChegada",
        duracao="tempoEstimado",
        preco="valorPassagem",
        assentos="assentosDisponiveis",
        uf_origem="ufOrigem",
        uf_destino="ufDestino",
        categoria="tipoServico",
    )

    def reconhecer(self, payload: dict) -> bool:
        return "codigoViagem" in payload

    def _extrair(self, payload: dict) -> dict:
        partida = interpretar_data_brasileira(
            payload["dataHoraSaida"],
            "dataHoraSaida",
            payload["fusoHorario"],
        )
        chegada = interpretar_data_brasileira(
            payload["dataHoraChegada"],
            "dataHoraChegada",
            payload["fusoHorario"],
        )

        return {
            "id_viagem": str(payload["codigoViagem"]),
            "cidade_origem": str(payload["cidadeOrigem"]).strip(),
            "uf_origem": str(payload["ufOrigem"]).strip().upper(),
            "cidade_destino": str(payload["cidadeDestino"]).strip(),
            "uf_destino": str(payload["ufDestino"]).strip().upper(),
            "partida": partida,
            "chegada": chegada,
            "duracao_minutos": minutos_de_hh_mm(payload["tempoEstimado"], "tempoEstimado"),
            "preco": preco_de_texto_brasileiro(payload["valorPassagem"], "valorPassagem"),
            "moeda": "BRL",
            "categoria": normalizar_categoria(payload["tipoServico"], "tipoServico"),
            "assentos": para_inteiro(payload["assentosDisponiveis"], "assentosDisponiveis"),
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
