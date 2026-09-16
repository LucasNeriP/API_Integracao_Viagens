# Importa as integrações para garantir que sejam registradas
import app.integrations  # noqa: F401

# Importa as exceções utilizadas pelo serviço
from app.exceptions import (
    FalhaNaNormalizacao,
    ViagemInvalidaError,
)

# Importa o Registry
from app.integrations.registry import registro


# Mensagem usada quando nenhuma empresa reconhece o payload
MENSAGEM_FORMATO_DESCONHECIDO = (
    "O formato do payload não corresponde a nenhuma companhia suportada."
)


# Função responsável por coordenar o processamento
def processar_viagens(payloads: list) -> dict:

    # Lista que armazenará as viagens já normalizadas
    viagens_normalizadas = []

    # Percorre todas as viagens recebidas
    # enumerate fornece o índice e o conteúdo
    for indice, payload in enumerate(payloads):

        # Verifica se o objeto recebido é realmente um dict
        if not isinstance(payload, dict):

            # Se não for, interrompe tudo com erro 422
            raise FalhaNaNormalizacao(
                indice=indice,
                empresa_identificada=None,
                campo=None,
                mensagem=MENSAGEM_FORMATO_DESCONHECIDO,
            )

        # Pede ao Registry para descobrir qual empresa reconhece o payload
        estrategia = registro.identificar(payload)

        # Se nenhuma Strategy reconhecer
        if estrategia is None:

            # Interrompe o processamento
            raise FalhaNaNormalizacao(
                indice=indice,
                empresa_identificada=None,
                campo=None,
                mensagem=MENSAGEM_FORMATO_DESCONHECIDO,
            )

        # Tenta validar e normalizar a viagem
        try:

            # A Strategy encontrada faz o processamento
            viagem_normalizada = estrategia.processar(payload)

        # Captura erros de validação
        except ViagemInvalidaError as erro:

            # Transforma o erro em um erro específico da API
            raise FalhaNaNormalizacao(
                indice=indice,
                empresa_identificada=estrategia.nome_empresa,
                campo=erro.campo,
                mensagem=erro.mensagem,
            ) from erro

        # Adiciona a viagem normalizada à lista
        viagens_normalizadas.append(viagem_normalizada)

    # Retorna o resultado final
    return {
        "total": len(viagens_normalizadas),
        "viagens": viagens_normalizadas,
    }