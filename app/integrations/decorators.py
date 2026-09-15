from app.integrations.base import IntegracaoBase

_integracoes_registradas: list[IntegracaoBase] = []

def registrar_integracao(classe):
    _integracoes_registradas.append(classe())
    return classe

def obter_integracoes_registradas() -> list[IntegracaoBase]:
    return _integracoes_registradas