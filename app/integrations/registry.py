from app.integrations.progresso import ProgressoIntegration
from app.integrations.rota import RotaIntegration

integracoes = [
    ProgressoIntegration(),
    RotaIntegration()
]

def identificar_integracao(viagem: dict):
    for integracao in integracoes:
        if integracao.reconhecer(viagem):
            return integracao
    return None    