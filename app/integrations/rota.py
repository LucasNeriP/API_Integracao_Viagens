class RotaIntegration:
    def reconhecer(self, viagem: dict):
        return "trip_id" in viagem

    def normalizar(self, viagem: dict):
        return {
            "id_viagem": viagem["trip_id"],
            "empresa": "Rota Transportes"
        }