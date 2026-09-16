# Importa a classe base das integrações
from app.integrations.base import IntegracaoCompanhia


# Classe responsável por armazenar as Strategies
class RegistroDeIntegracoes:

    # Executado quando o Registry é criado
    def __init__(self):

        # Lista que armazenará as integrações
        self._estrategias: list[IntegracaoCompanhia] = []

    # Adiciona uma Strategy ao Registry
    def registrar(self, estrategia: IntegracaoCompanhia) -> None:

        # Coloca a Strategy na lista
        self._estrategias.append(estrategia)

    # Remove uma Strategy
    def remover(self, estrategia: IntegracaoCompanhia) -> None:

        # Verifica se ela existe na lista
        if estrategia in self._estrategias:

            # Remove a Strategy
            self._estrategias.remove(estrategia)

    # Retorna as Strategies cadastradas
    def listar(self) -> list[IntegracaoCompanhia]:

        # Retorna uma cópia da lista
        return list(self._estrategias)

    # Procura qual Strategy reconhece o payload
    def identificar(
        self,
        payload: dict
    ) -> IntegracaoCompanhia | None:

        # Percorre todas as Strategies cadastradas
        for estrategia in self._estrategias:

            # Pergunta para cada Strategy se ela reconhece o payload
            if estrategia.reconhecer(payload):

                # Se reconhecer, retorna essa Strategy
                return estrategia

        # Nenhuma Strategy reconheceu
        return None


# Cria uma única instância do Registry
registro = RegistroDeIntegracoes()


# Decorator usado para registrar automaticamente uma integração
def registrar_integracao(classe):

    # Cria uma instância da classe e registra no Registry
    registro.registrar(classe())

    # Retorna a própria classe
    return classe