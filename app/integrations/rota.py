from app.integrations.base import IntegracaoBase
from app.integrations.decorators import registrar_integracao

@registrar_integracao
class RotaIntegration(IntegracaoBase):
    nome_empresa = "Rota Transportes"

    def reconhecer(self, viagem: dict):
        return "trip_id" in viagem

    def normalizar(self, viagem: dict):

        valor = viagem["tarifa_centavos"] / 100
        return {
            "id_viagem": viagem["trip_id"],
            "empresa": "Rota Transportes",
            "origem": {
                "cidade": viagem["origem"]["municipio"],
                "uf": viagem["origem"]["estado"]
            },
            "destino": {
                "cidade": viagem["destino"]["municipio"],
                "uf": viagem["destino"]["estado"]
            },

            "partida": viagem["partida_em"],
            "chegada": viagem["chegada_em"],
            "duracao_minutos": viagem["duracao_minutos"],

            "preco": {
                "valor": valor,
                "moeda": viagem["moeda"]
            },

            "categoria": viagem["classe"].lower(),

            "assentos_disponiveis": viagem["vagas"]
        }