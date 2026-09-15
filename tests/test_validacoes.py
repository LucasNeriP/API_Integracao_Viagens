from copy import deepcopy

from tests.exemplos import PAYLOAD_PROGRESSO, PAYLOAD_ROTA, URL


def test_rejeita_formato_nao_reconhecido(cliente):
    resposta = cliente.post(URL, json=[{"campoInventado": True}])

    assert resposta.status_code == 422
    assert resposta.json()["detail"] == {
        "indice": 0,
        "empresa_identificada": None,
        "campo": None,
        "mensagem": "O formato do payload não corresponde a nenhuma companhia suportada.",
    }


def test_rejeita_formato_nao_reconhecido_no_meio_da_lista(cliente):
    resposta = cliente.post(
        URL,
        json=[PAYLOAD_PROGRESSO, {"foo": "bar"}, PAYLOAD_ROTA],
    )

    assert resposta.status_code == 422
    assert resposta.json()["detail"]["indice"] == 1
    assert resposta.json()["detail"]["empresa_identificada"] is None
    assert "viagens" not in resposta.json()


def test_rejeita_a_requisicao_inteira_quando_um_objeto_e_invalido(cliente):
    payload_invalido = deepcopy(PAYLOAD_ROTA)
    payload_invalido["chegada_em"] = "2026-10-15T06:00:00-03:00"

    resposta = cliente.post(
        URL,
        json=[PAYLOAD_PROGRESSO, payload_invalido],
    )

    assert resposta.status_code == 422
    detalhe = resposta.json()["detail"]
    assert detalhe["indice"] == 1
    assert detalhe["empresa_identificada"] == "Rota Transportes"
    assert detalhe["campo"] == "chegada_em"
    assert "viagens" not in resposta.json()


def test_rejeita_preco_menor_ou_igual_a_zero(cliente):
    payload = deepcopy(PAYLOAD_PROGRESSO)
    payload["valorPassagem"] = "0,00"

    resposta = cliente.post(URL, json=[payload])

    assert resposta.status_code == 422
    detalhe = resposta.json()["detail"]
    assert detalhe["campo"] == "valorPassagem"
    assert "maior que zero" in detalhe["mensagem"]


def test_rejeita_duracao_menor_ou_igual_a_zero(cliente):
    payload = deepcopy(PAYLOAD_PROGRESSO)
    payload["tempoEstimado"] = "00:00"

    resposta = cliente.post(URL, json=[payload])

    assert resposta.status_code == 422
    detalhe = resposta.json()["detail"]
    assert detalhe["campo"] == "tempoEstimado"
    assert "maior que zero" in detalhe["mensagem"]


def test_rejeita_uf_com_tamanho_diferente_de_dois(cliente):
    payload = deepcopy(PAYLOAD_PROGRESSO)
    payload["ufOrigem"] = "BAHIA"

    resposta = cliente.post(URL, json=[payload])

    assert resposta.status_code == 422
    detalhe = resposta.json()["detail"]
    assert detalhe["campo"] == "ufOrigem"
    assert "dois caracteres" in detalhe["mensagem"]


def test_rejeita_categoria_desconhecida(cliente):
    payload = deepcopy(PAYLOAD_PROGRESSO)
    payload["tipoServico"] = "PREMIUM"

    resposta = cliente.post(URL, json=[payload])

    assert resposta.status_code == 422
    detalhe = resposta.json()["detail"]
    assert detalhe["campo"] == "tipoServico"
    assert "não pôde ser normalizada" in detalhe["mensagem"]
