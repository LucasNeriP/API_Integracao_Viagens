from app.integrations.base import IntegracaoCompanhia
from app.integrations.registry import registro
from app.normalizacao import (
    NomesDosCampos,
    aplicar_regras_comuns,
    exigir_campos,
    interpretar_data_iso,
    normalizar_categoria,
    para_inteiro,
    para_iso8601,
    preco_de_decimal,
)
from app.schemas import montar_viagem_normalizada
from tests.exemplos import PAYLOAD_PROGRESSO, URL


class IntegracaoLaboratorio(IntegracaoCompanhia):
    """Companhia criada só nos testes, para provar que o fluxo principal não muda."""

    nome_empresa = "Laboratório Bus"

    def reconhecer(self, payload: dict) -> bool:
        return "id_laboratorio" in payload

    def validar(self, payload: dict) -> None:
        exigir_campos(
            payload,
            [
                "id_laboratorio",
                "cidade_origem",
                "uf_origem",
                "cidade_destino",
                "uf_destino",
                "saida",
                "chegada",
                "minutos",
                "preco",
                "moeda",
                "categoria",
                "vagas",
            ],
        )
        partida = interpretar_data_iso(payload["saida"], "saida")
        chegada = interpretar_data_iso(payload["chegada"], "chegada")
        aplicar_regras_comuns(
            partida=partida,
            chegada=chegada,
            duracao_minutos=para_inteiro(payload["minutos"], "minutos"),
            preco=preco_de_decimal(payload["preco"], "preco"),
            assentos=para_inteiro(payload["vagas"], "vagas"),
            uf_origem=str(payload["uf_origem"]).strip().upper(),
            uf_destino=str(payload["uf_destino"]).strip().upper(),
            campos=NomesDosCampos(
                partida="saida",
                chegada="chegada",
                duracao="minutos",
                preco="preco",
                assentos="vagas",
                uf_origem="uf_origem",
                uf_destino="uf_destino",
                categoria="categoria",
            ),
        )
        normalizar_categoria(payload["categoria"], "categoria")

    def normalizar(self, payload: dict) -> dict:
        partida = interpretar_data_iso(payload["saida"], "saida")
        chegada = interpretar_data_iso(payload["chegada"], "chegada")
        return montar_viagem_normalizada(
            id_viagem=str(payload["id_laboratorio"]),
            empresa=self.nome_empresa,
            cidade_origem=str(payload["cidade_origem"]).strip(),
            uf_origem=str(payload["uf_origem"]).strip().upper(),
            cidade_destino=str(payload["cidade_destino"]).strip(),
            uf_destino=str(payload["uf_destino"]).strip().upper(),
            partida=para_iso8601(partida),
            chegada=para_iso8601(chegada),
            duracao_minutos=para_inteiro(payload["minutos"], "minutos"),
            preco=preco_de_decimal(payload["preco"], "preco"),
            moeda=str(payload["moeda"]).strip().upper(),
            categoria=normalizar_categoria(payload["categoria"], "categoria"),
            assentos_disponiveis=para_inteiro(payload["vagas"], "vagas"),
        )


def test_nova_companhia_entra_so_com_registro_da_estrategia(cliente):
    laboratorio = IntegracaoLaboratorio()
    registro.registrar(laboratorio)

    payload_laboratorio = {
        "id_laboratorio": "LAB-2026-001",
        "cidade_origem": "Paulo Afonso",
        "uf_origem": "BA",
        "cidade_destino": "Petrolina",
        "uf_destino": "PE",
        "saida": "2026-10-16T09:00:00-03:00",
        "chegada": "2026-10-16T11:00:00-03:00",
        "minutos": 120,
        "preco": 50.00,
        "moeda": "BRL",
        "categoria": "leito",
        "vagas": 4,
    }

    try:
        resposta = cliente.post(
            URL,
            json=[PAYLOAD_PROGRESSO, payload_laboratorio],
        )
    finally:
        registro.remover(laboratorio)

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["total"] == 2
    assert corpo["viagens"][0]["empresa"] == "Auto Viação Progresso"
    assert corpo["viagens"][1]["empresa"] == "Laboratório Bus"
    assert corpo["viagens"][1]["id_viagem"] == "LAB-2026-001"
    assert corpo["viagens"][1]["categoria"] == "leito"
