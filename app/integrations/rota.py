class RotaIntegration:
    def reconhecer(self, viagem: dict):
        return "trip_id" in viagem

    def normalizar(self, viagem: dict):
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
            "duracao_minutos": viagem["duracao_minutos"]
        }