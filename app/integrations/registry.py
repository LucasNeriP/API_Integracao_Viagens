from app.integrations.base import IntegracaoCompanhia


class RegistroDeIntegracoes:
    """
    Registry das estratégias de companhia.

    A identificação NÃO usa uma cadeia de if/elif/else.
    O fluxo principal apenas pergunta ao registro: "quem reconhece este payload?".
    O registro percorre as estratégias cadastradas e devolve a primeira que
    reconhecer a estrutura do objeto.

    Uma nova companhia entra no sistema ao ser registrada. O loop abaixo
    continua o mesmo, sem novo desvio condicional no fluxo principal.
    """

    def __init__(self):
        self._estrategias: list[IntegracaoCompanhia] = []

    def registrar(self, estrategia: IntegracaoCompanhia) -> None:
        self._estrategias.append(estrategia)

    def remover(self, estrategia: IntegracaoCompanhia) -> None:
        if estrategia in self._estrategias:
            self._estrategias.remove(estrategia)

    def listar(self) -> list[IntegracaoCompanhia]:
        return list(self._estrategias)

    def identificar(self, payload: dict) -> IntegracaoCompanhia | None:
        for estrategia in self._estrategias:
            if estrategia.reconhecer(payload):
                return estrategia
        return None


registro = RegistroDeIntegracoes()


def registrar_integracao(classe):
    """
    Decorator que registra a estratégia no Registry assim que a classe é definida.

    Uso:

        @registrar_integracao
        class IntegracaoNovaCompanhia(IntegracaoCompanhia):
            ...
    """

    registro.registrar(classe())
    return classe
