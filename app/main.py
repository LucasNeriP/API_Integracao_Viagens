from fastapi import FastAPI
from app.integrations.progresso import ProgressoIntegration
from typing import Any

app = FastAPI()
progresso = ProgressoIntegration()

@app.get("/")
def inicio():
    return {"message": "Bem-vindo à API de Integração de Viagens!"}

@app.post("/api/v1/viagens/normalizar")
def normalizar_viagem(viagens: list[dict]):
    for viagem in viagens:
        print(progresso.reconhecer(viagem))
    return viagens    