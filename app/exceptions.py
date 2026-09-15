class ViagemInvalidaError(Exception):
    def __init__(self, campo, mensagem):
        self.campo = campo
        self.mensagem = mensagem
        super().__init__(mensagem)