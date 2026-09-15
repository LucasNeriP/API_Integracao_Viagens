from copy import deepcopy

from tests.exemplos import PAYLOAD_ROTA, URL, VIAGEM_ROTA


def test_normaliza_payload_da_rota(cliente):
    resposta = cliente.post(URL, json=[PAYLOAD_ROTA])

    assert resposta.status_code == 200
    assert resposta.json()["viagens"][0] == VIAGEM_ROTA


def test_converte_tarifa_de_centavos_para_reais(cliente):
    resposta = cliente.post(URL, json=[PAYLOAD_ROTA])

    assert resposta.json()["viagens"][0]["preco"]["valor"] == 89.90


def test_rejeita_chegada_anterior_a_saida_na_rota(cliente):
    payload = deepcopy(PAYLOAD_ROTA)
    payload["chegada_em"] = "2026-10-15T06:00:00-03:00"

    resposta = cliente.post(URL, json=[payload])

    assert resposta.status_code == 422
    assert resposta.json()["detail"] == {
        "indice": 0,
        "empresa_identificada": "Rota Transportes",
        "campo": "chegada_em",
        "mensagem": "A data de chegada deve ser posterior à data de saída.",
    }


def test_rejeita_objeto_de_origem_incompleto_na_rota(cliente):
    payload = deepcopy(PAYLOAD_ROTA)
    del payload["origem"]["municipio"]

    resposta = cliente.post(URL, json=[payload])

    assert resposta.status_code == 422
    detalhe = resposta.json()["detail"]
    assert detalhe["empresa_identificada"] == "Rota Transportes"
    assert detalhe["campo"] == "origem.municipio"
