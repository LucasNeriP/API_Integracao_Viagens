from abc import ABC, abstractmethod


class IntegracaoCompanhia(ABC):
    """
    Estratégia de uma companhia.

    Cada companhia sabe:
    - reconhecer o próprio formato
    - validar os campos que envia
    - converter os dados para o contrato homogêneo
    """

    nome_empresa: str

    @abstractmethod
    def reconhecer(self, payload: dict) -> bool:
        """Retorna True se este payload pertence a esta companhia."""

    @abstractmethod
    def validar(self, payload: dict) -> None:
        """Levanta ViagemInvalidaError quando o payload for inválido."""

    @abstractmethod
    def normalizar(self, payload: dict) -> dict:
        """Converte o payload da companhia para o contrato de saída."""

    def processar(self, payload: dict) -> dict:
        """Sequência comum: validar e, em seguida, normalizar."""

        self.validar(payload)
        return self.normalizar(payload)
