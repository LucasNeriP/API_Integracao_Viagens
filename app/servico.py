import app.integrations  # noqa: F401  # registra as estratégias no Registry
from app.exceptions import FalhaNaNormalizacao, ViagemInvalidaError
from app.integrations.registry import registro

MENSAGEM_FORMATO_DESCONHECIDO = (
    "O formato do payload não corresponde a nenhuma companhia suportada."
)


def processar_viagens(payloads: list) -> dict:
    """
    Fluxo principal da normalização.

    Este método não conhece nenhuma companhia específica.
    Ele apenas:
    1. percorre os objetos na ordem recebida
    2. pede ao Registry a estratégia correspondente
    3. delega validação e conversão para essa estratégia

    Por isso, uma nova companhia não altera este fluxo.
    """

    viagens_normalizadas = []

    for indice, payload in enumerate(payloads):
        if not isinstance(payload, dict):
            raise FalhaNaNormalizacao(
                indice=indice,
                empresa_identificada=None,
                campo=None,
                mensagem=MENSAGEM_FORMATO_DESCONHECIDO,
            )

        estrategia = registro.identificar(payload)
        if estrategia is None:
            raise FalhaNaNormalizacao(
                indice=indice,
                empresa_identificada=None,
                campo=None,
                mensagem=MENSAGEM_FORMATO_DESCONHECIDO,
            )

        try:
            viagem_normalizada = estrategia.processar(payload)
        except ViagemInvalidaError as erro:
            raise FalhaNaNormalizacao(
                indice=indice,
                empresa_identificada=estrategia.nome_empresa,
                campo=erro.campo,
                mensagem=erro.mensagem,
            ) from erro

        viagens_normalizadas.append(viagem_normalizada)

    return {
        "total": len(viagens_normalizadas),
        "viagens": viagens_normalizadas,
    }
