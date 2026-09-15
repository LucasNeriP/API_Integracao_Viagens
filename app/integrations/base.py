from abc import ABC, abstractmethod

class IntegracaoBase(ABC):

    nome_empresa: str

    @abstractmethod
    def reconhecer(self, viagem: dict) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def normalizar(self, viagem: dict) -> dict:
            raise NotImplementedError