from fastapi import FastAPI
from typing import Any
from app.integrations.registry import identificar_integracao
app = FastAPI()

@app.get("/")
def inicio():
    return {"message": "Bem-vindo à API de Integração de Viagens!"}

@app.post("/api/v1/viagens/normalizar")

def normalizar_viagem(viagens: list[dict]):
    for viagem in viagens:
        integracao = identificar_integracao(viagem)
        print(integracao.normalizar(viagem))
    return viagens    