from app.integrations.base import IntegracaoCompanhia
from app.integrations.registry import registrar_integracao
from app.normalizacao import (
    NomesDosCampos,
    aplicar_regras_comuns,
    exigir_campos,
    exigir_objeto,
    interpretar_data_iso,
    minutos_de_horas,
    normalizar_categoria,
    para_inteiro,
    para_iso8601,
    preco_de_decimal,
    separar_cidade_e_uf,
)
from app.schemas import montar_viagem_normalizada


@registrar_integracao
class IntegracaoSertaoBus(IntegracaoCompanhia):
    """
    Estratégia da companhia fictícia Sertão Bus.

    Serve para demonstrar a extensibilidade: esta classe foi adicionada
    sem alterar o endpoint, o contrato de saída, o Registry nem as
    demais companhias. O campo duracao_horas é exclusivo desta companhia.
    """

    nome_empresa = "Sertão Bus"

    CAMPOS_OBRIGATORIOS = [
        "numero",
        "rota",
        "horarios",
        "duracao_horas",
        "preco_total",
        "moeda",
        "servico",
        "lugares_livres",
    ]

    NOMES_DOS_CAMPOS = NomesDosCampos(
        partida="horarios.saida",
        chegada="horarios.chegada",
        duracao="duracao_horas",
        preco="preco_total",
        assentos="lugares_livres",
        uf_origem="rota.partida",
        uf_destino="rota.chegada",
        categoria="servico",
    )

    def reconhecer(self, payload: dict) -> bool:
        return "duracao_horas" in payload

    def _extrair(self, payload: dict) -> dict:
        rota = exigir_objeto(payload, "rota")
        horarios = exigir_objeto(payload, "horarios")

        exigir_campos(rota, ["partida", "chegada"], prefixo="rota")
        exigir_campos(horarios, ["saida", "chegada"], prefixo="horarios")

        cidade_origem, uf_origem = separar_cidade_e_uf(rota["partida"], "rota.partida")
        cidade_destino, uf_destino = separar_cidade_e_uf(rota["chegada"], "rota.chegada")

        return {
            "id_viagem": str(payload["numero"]),
            "cidade_origem": cidade_origem,
            "uf_origem": uf_origem.upper(),
            "cidade_destino": cidade_destino,
            "uf_destino": uf_destino.upper(),
            "partida": interpretar_data_iso(horarios["saida"], "horarios.saida"),
            "chegada": interpretar_data_iso(horarios["chegada"], "horarios.chegada"),
            "duracao_minutos": minutos_de_horas(payload["duracao_horas"], "duracao_horas"),
            "preco": preco_de_decimal(payload["preco_total"], "preco_total"),
            "moeda": str(payload["moeda"]).strip().upper(),
            "categoria": normalizar_categoria(payload["servico"], "servico"),
            "assentos": para_inteiro(payload["lugares_livres"], "lugares_livres"),
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
