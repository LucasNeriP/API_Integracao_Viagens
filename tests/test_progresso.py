from copy import deepcopy

from tests.exemplos import PAYLOAD_PROGRESSO, URL, VIAGEM_PROGRESSO


def test_normaliza_payload_da_progresso(cliente):
    resposta = cliente.post(URL, json=[PAYLOAD_PROGRESSO])

    assert resposta.status_code == 200
    assert resposta.json()["viagens"][0] == VIAGEM_PROGRESSO


def test_rejeita_campo_obrigatorio_ausente_na_progresso(cliente):
    payload = deepcopy(PAYLOAD_PROGRESSO)
    del payload["cidadeOrigem"]

    resposta = cliente.post(URL, json=[payload])

    assert resposta.status_code == 422
    assert resposta.json()["detail"] == {
        "indice": 0,
        "empresa_identificada": "Auto Viação Progresso",
        "campo": "cidadeOrigem",
        "mensagem": "O campo cidadeOrigem é obrigatório.",
    }


def test_rejeita_data_em_formato_invalido_na_progresso(cliente):
    payload = deepcopy(PAYLOAD_PROGRESSO)
    payload["dataHoraSaida"] = "2026-10-15T06:30:00"

    resposta = cliente.post(URL, json=[payload])

    assert resposta.status_code == 422
    detalhe = resposta.json()["detail"]
    assert detalhe["empresa_identificada"] == "Auto Viação Progresso"
    assert detalhe["campo"] == "dataHoraSaida"


def test_rejeita_preco_com_formato_invalido_na_progresso(cliente):
    payload = deepcopy(PAYLOAD_PROGRESSO)
    payload["valorPassagem"] = "doze reais"

    resposta = cliente.post(URL, json=[payload])

    assert resposta.status_code == 422
    assert resposta.json()["detail"]["campo"] == "valorPassagem"


def test_rejeita_duracao_incompativel_na_progresso(cliente):
    payload = deepcopy(PAYLOAD_PROGRESSO)
    payload["tempoEstimado"] = "01:00"

    resposta = cliente.post(URL, json=[payload])

    assert resposta.status_code == 422
    detalhe = resposta.json()["detail"]
    assert detalhe["campo"] == "tempoEstimado"
    assert "incompatível" in detalhe["mensagem"]
