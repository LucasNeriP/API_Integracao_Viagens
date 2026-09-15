from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import app.integrations  # noqa: F401  # carrega e registra as estratégias
from app.exceptions import FalhaNaNormalizacao
from app.schemas import RespostaNormalizacao
from app.servico import processar_viagens

app = FastAPI(
    title="API de Integração de Viagens",
    description=(
        "Recebe viagens de companhias distintas, identifica a origem "
        "pela estrutura do payload e devolve um contrato homogêneo."
    ),
    version="1.0.0",
)


@app.exception_handler(FalhaNaNormalizacao)
async def tratar_falha_na_normalizacao(
    request: Request,
    erro: FalhaNaNormalizacao,
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "detail": {
                "indice": erro.indice,
                "empresa_identificada": erro.empresa_identificada,
                "campo": erro.campo,
                "mensagem": erro.mensagem,
            }
        },
    )


@app.get("/")
def inicio():
    return {
        "message": "Bem-vindo à API de Integração de Viagens!"
    }


@app.post("/api/v1/viagens/normalizar", response_model=RespostaNormalizacao)
def normalizar_viagens(payloads: list[dict]):
    return processar_viagens(payloads)
