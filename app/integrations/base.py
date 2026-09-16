# Importa ferramentas para criar uma classe abstrata
from abc import ABC, abstractmethod


# Classe base que todas as integrações de empresas devem seguir
class IntegracaoCompanhia(ABC):

    # Toda integração deve possuir o nome da empresa
    nome_empresa: str

    # Define o método que identifica a empresa
    @abstractmethod
    def reconhecer(self, payload: dict) -> bool:
        ...

    # Define o método que valida os dados
    @abstractmethod
    def validar(self, payload: dict) -> None:
        ...

    # Define o método que transforma os dados
    @abstractmethod
    def normalizar(self, payload: dict) -> dict:
        ...

    # Processo comum para todas as empresas
    def processar(self, payload: dict) -> dict:

        # Primeiro valida os dados
        self.validar(payload)

        # Depois normaliza os dados
        return self.normalizar(payload)