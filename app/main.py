from fastapi import FastAPI
from typing import Any
from app.integrations.registry import identificar_integracao
app = FastAPI()

@app.get("/")
def inicio():
    return {"message": "Bem-vindo à API de Integração de Viagens!"}

@app.post("/api/v1/viagens/normalizar")
def normalizar_viagem(viagens: list[dict]):
    viagens_normalizadas = []
    for viagem in viagens:
        integracao = identificar_integracao(viagem)
        viagem_normalizada = integracao.normalizar(viagem)

        viagens_normalizadas.append(viagem_normalizada)
    return viagens_normalizadas 