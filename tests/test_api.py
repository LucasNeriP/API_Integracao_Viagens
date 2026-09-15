from copy import deepcopy

from tests.exemplos import (
    URL,
    PAYLOAD_GONTIJO,
    PAYLOAD_PROGRESSO,
    PAYLOAD_ROTA,
    PAYLOAD_SERTAO_BUS,
    VIAGEM_GONTIJO,
    VIAGEM_PROGRESSO,
    VIAGEM_ROTA,
    VIAGEM_SERTAO_BUS,
)


def test_normaliza_o_exemplo_oficial_das_tres_companhias(cliente):
    resposta = cliente.post(
        URL,
        json=[PAYLOAD_PROGRESSO, PAYLOAD_ROTA, PAYLOAD_GONTIJO],
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["total"] == 3
    assert corpo["viagens"][0] == VIAGEM_PROGRESSO
    assert corpo["viagens"][1] == VIAGEM_ROTA
    assert corpo["viagens"][2] == VIAGEM_GONTIJO


def test_preserva_a_ordem_mesmo_quando_os_objetos_chegam_embaralhados(cliente):
    resposta = cliente.post(
        URL,
        json=[PAYLOAD_GONTIJO, PAYLOAD_PROGRESSO, PAYLOAD_ROTA],
    )

    assert resposta.status_code == 200
    viagens = resposta.json()["viagens"]
    assert [viagem["empresa"] for viagem in viagens] == [
        "Gontijo",
        "Auto Viação Progresso",
        "Rota Transportes",
    ]


def test_inclui_sertao_bus_no_mesmo_endpoint(cliente):
    resposta = cliente.post(
        URL,
        json=[PAYLOAD_SERTAO_BUS],
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["total"] == 1
    assert corpo["viagens"][0] == VIAGEM_SERTAO_BUS


def test_ignora_campos_adicionais_que_nao_fazem_parte_do_contrato(cliente):
    payload = deepcopy(PAYLOAD_PROGRESSO)
    payload["observacaoInterna"] = "campo que deve ser ignorado"
    payload["codigoSecreto"] = 123

    resposta = cliente.post(URL, json=[payload])

    assert resposta.status_code == 200
    viagem = resposta.json()["viagens"][0]
    assert "observacaoInterna" not in viagem
    assert "codigoSecreto" not in viagem
    assert set(viagem.keys()) == set(VIAGEM_PROGRESSO.keys())


def test_lista_vazia_devolve_total_zero(cliente):
    resposta = cliente.post(URL, json=[])

    assert resposta.status_code == 200
    assert resposta.json() == {"total": 0, "viagens": []}
