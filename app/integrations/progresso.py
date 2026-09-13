class ProgressoIntegration:
    def reconhecer(self, viagem: dict):
        return "codigoViagem" in viagem
    
    def normalizar(self, viagem: dict):
        return {
            "id_viagem": viagem["codigoViagem"],
            "empresa": "Auto Viação Progresso"
        }