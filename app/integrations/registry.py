from app.integrations import progresso, rota
from app.integrations.decorators import obter_integracoes_registradas

def identificar_integracao(viagem: dict):
    for integracao in obter_integracoes_registradas:
        if integracao.reconhecer(viagem):
            return integracao
    return None    