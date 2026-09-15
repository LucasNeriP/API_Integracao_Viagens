class ViagemInvalidaError(Exception):
    """Erro de validação de um payload já identificado como de uma companhia."""

    def __init__(self, campo: str, mensagem: str):
        self.campo = campo
        self.mensagem = mensagem
        super().__init__(mensagem)


class FalhaNaNormalizacao(Exception):
    """Erro de normalização já associado a um índice da requisição."""

    def __init__(
        self,
        indice: int,
        empresa_identificada: str | None,
        campo: str | None,
        mensagem: str,
    ):
        self.indice = indice
        self.empresa_identificada = empresa_identificada
        self.campo = campo
        self.mensagem = mensagem
        super().__init__(mensagem)
