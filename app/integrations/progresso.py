from datetime import datetime
from zoneinfo import ZoneInfo

class ProgressoIntegration:
    def reconhecer(self, viagem: dict):
        return "codigoViagem" in viagem
    
    def normalizar(self, viagem: dict):
        partida = datetime.strptime(
            viagem["dataHoraSaida"], "%d/%m/%Y %H:%M"
        )

        partida = partida.replace(
            tzinfo = ZoneInfo(viagem["fusoHorario"])
        )

        chegada = datetime.strptime(
            viagem["dataHoraChegada"], "%d/%m/%Y %H:%M"
        )

        chegada = chegada.replace(
            tzinfo = ZoneInfo(viagem["fusoHorario"])
        )

        horas, minutos = viagem["tempoEstimado"].split(":")
        duracao_minutos = int(horas) * 60 + int(minutos)

        valor = float(
            viagem["valorPassagem"].replace(",", ".")
        )

        return {
            "id_viagem": viagem["codigoViagem"],
            "empresa": "Auto Viação Progresso",
            "origem": {
                "cidade": viagem["cidadeOrigem"],
                "uf": viagem["ufOrigem"]
            },

            "destino": {
                "cidade": viagem["cidadeDestino"],
                "uf": viagem["ufDestino"]
            },

            "partida": partida.isoformat(),
            "chegada": chegada.isoformat(),
            "duracao_minutos": duracao_minutos,

            "preço": {
                "valor": valor,
                "moeda": "BRL"
            },

            "categoria": viagem["tipoServico"].lower(),

            "assentos_disponiveis": int(viagem["assentosDisponiveis"])

        }