from fastapi import FastAPI, HTTPException

from app.integrations.registry import identificar_integracao
from app.exceptions import ViagemInvalidaError


app = FastAPI()


@app.get("/")
def inicio():
    return {
        "message": "Bem-vindo à API de Integração de Viagens!"
    }


@app.post("/api/v1/viagens/normalizar")
def normalizar_viagem(viagens: list[dict]):

    viagens_normalizadas = []

    for indice, viagem in enumerate(viagens):

        integracao = identificar_integracao(viagem)
        if integracao is None:
            raise HTTPException(
                status_code=422,
                detail={
                    "indice": indice,
                    "empresa_identificada": None,
                    "campo": "formato",
                    "mensagem": "O formato da viagem não foi reconhecido."
                }
            )
        try:
            integracao.validar(viagem)

        except ViagemInvalidaError as erro:
            raise HTTPException(
                status_code=422,
                detail={
                    "indice": indice,
                    "empresa_identificada": integracao.nome_empresa,
                    "campo": erro.campo,
                    "mensagem": erro.mensagem
                }
            )
        viagem_normalizada = integracao.normalizar(viagem)

        viagens_normalizadas.append(
            viagem_normalizada
        )

    return viagens_normalizadas