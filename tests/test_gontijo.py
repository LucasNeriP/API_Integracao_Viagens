from copy import deepcopy

from tests.exemplos import PAYLOAD_GONTIJO, URL, VIAGEM_GONTIJO


def test_normaliza_payload_da_gontijo(cliente):
    resposta = cliente.post(URL, json=[PAYLOAD_GONTIJO])

    assert resposta.status_code == 200
    assert resposta.json()["viagens"][0] == VIAGEM_GONTIJO


def test_converte_utc_para_america_bahia(cliente):
    resposta = cliente.post(URL, json=[PAYLOAD_GONTIJO])
    viagem = resposta.json()["viagens"][0]

    assert viagem["partida"] == "2026-10-15T16:30:00-03:00"
    assert viagem["chegada"] == "2026-10-16T09:10:00-03:00"


def test_converte_duracao_de_segundos_para_minutos(cliente):
    resposta = cliente.post(URL, json=[PAYLOAD_GONTIJO])

    assert resposta.json()["viagens"][0]["duracao_minutos"] == 1000


def test_normaliza_semi_sleeper_para_semileito(cliente):
    resposta = cliente.post(URL, json=[PAYLOAD_GONTIJO])

    assert resposta.json()["viagens"][0]["categoria"] == "semileito"


def test_rejeita_assentos_negativos_na_gontijo(cliente):
    payload = deepcopy(PAYLOAD_GONTIJO)
    payload["availableSeats"] = -1

    resposta = cliente.post(URL, json=[payload])

    assert resposta.status_code == 422
    detalhe = resposta.json()["detail"]
    assert detalhe["empresa_identificada"] == "Gontijo"
    assert detalhe["campo"] == "availableSeats"
    assert "não pode ser negativa" in detalhe["mensagem"]
