from copy import deepcopy

from tests.exemplos import PAYLOAD_SERTAO_BUS, URL, VIAGEM_SERTAO_BUS


def test_normaliza_payload_da_sertao_bus(cliente):
    resposta = cliente.post(URL, json=[PAYLOAD_SERTAO_BUS])

    assert resposta.status_code == 200
    assert resposta.json()["viagens"][0] == VIAGEM_SERTAO_BUS


def test_separa_cidade_e_uf_do_campo_rota(cliente):
    resposta = cliente.post(URL, json=[PAYLOAD_SERTAO_BUS])
    viagem = resposta.json()["viagens"][0]

    assert viagem["origem"] == {"cidade": "Paulo Afonso", "uf": "BA"}
    assert viagem["destino"] == {"cidade": "Maceió", "uf": "AL"}


def test_converte_duracao_em_horas_para_minutos(cliente):
    resposta = cliente.post(URL, json=[PAYLOAD_SERTAO_BUS])

    assert resposta.json()["viagens"][0]["duracao_minutos"] == 330


def test_normaliza_exec_para_executivo(cliente):
    resposta = cliente.post(URL, json=[PAYLOAD_SERTAO_BUS])

    assert resposta.json()["viagens"][0]["categoria"] == "executivo"


def test_rejeita_rota_sem_uf_na_sertao_bus(cliente):
    payload = deepcopy(PAYLOAD_SERTAO_BUS)
    payload["rota"]["partida"] = "Paulo Afonso"

    resposta = cliente.post(URL, json=[payload])

    assert resposta.status_code == 422
    detalhe = resposta.json()["detail"]
    assert detalhe["empresa_identificada"] == "Sertão Bus"
    assert detalhe["campo"] == "rota.partida"
