from datetime import datetime
from zoneinfo import ZoneInfo
from app.exceptions import ViagemInvalidaError

class ProgressoIntegration:
    nome_empresa = "Auto Viação Progresso"
    def reconhecer(self, viagem: dict):
        return "codigoViagem" in viagem

    def validar(self, viagem: dict):

        campos_obrigatorios = [
            "codigoViagem",
            "cidadeOrigem",
            "ufOrigem",
            "cidadeDestino",
            "ufDestino",
            "dataHoraSaida",
            "dataHoraChegada",
            "fusoHorario",
            "tempoEstimado",
            "valorPassagem",
            "tipoServico",
            "assentosDisponiveis"
        ]

        for campo in campos_obrigatorios:
            if campo not in viagem:
                raise ViagemInvalidaError(
                    campo = campo,
                    mensagem = f"O campo {campo} é obrigatório."
                )

        if len(viagem["ufOrigem"]) != 2:
            raise ViagemInvalidaError(
                campo = "ufOrigem",
                mensagem = "O campo ufOrigem deve conter exatamente 2 caracteres."
            )

        if len(viagem["ufDestino"]) != 2:
            raise ViagemInvalidaError(
                campo = "ufDestino",
                mensagem = "O campo ufDestino deve conter exatamente 2 caracteres."
            )

        try: 
            horas, minutos = viagem["tempoEstimado"].split(":")
            horas = int(horas)
            minutos = int(minutos)

            if horas < 0 or minutos < 0 or minutos >= 60:
                raise ValueError

            duracao = horas * 60 + minutos

        except (ValueError, AttributeError):
            raise ViagemInvalidaError(
                campo = "tempoEstimado",
                mensagem = "O campo tempoEstimado possui um formato inválido."
            )

        if duracao <= 0:
            raise ViagemInvalidaError(
                campo = "tempoEstimado",
                mensagem = "O campo tempoEstimado deve representar uma duração positiva."
            )

        try:
            valor = float(
                str(viagem["valorPassagem"]).replace(",", ".")
            )

        except (ValueError):
            raise ViagemInvalidaError(
                campo = "valorPassagem",
                mensagem = "O campo valorPassagem possui um formato inválido."
            )    

        if valor <= 0:
            raise ViagemInvalidaError(
                campo = "valorPassagem",
                mensagem = "O campo valorPassagem deve representar um valor positivo."
            )  

        if int(viagem["assentosDisponiveis"]) < 0:
            raise ViagemInvalidaError(
                campo = "assentosDisponiveis",
                mensagem = "O campo assentosDisponiveis não pode ser negativo."
            )  

        categoria = viagem["tipoServico"].lower()
        
        categorias_validas = ["convencional", "executivo", "leito", "semi-leito", "premium"]
        
        if categoria not in categorias_validas:
            raise ViagemInvalidaError(
                campo = "tipoServico",
                mensagem = "O campo tipoServico deve ser um dos valores válidos."
            )

        try: 
            partida = datetime.strptime(
                viagem["dataHoraSaida"], "%d/%m/%Y %H:%M"
            )   

            chegada = datetime.strptime(
                viagem["dataHoraChegada"], "%d/%m/%Y %H:%M"
            )       

        except ValueError:
            raise ViagemInvalidaError(
                campo = "dataHoraSaida/dataHoraChegada",
                mensagem = "Os campos dataqHoraSaida e dataHoraChegada possuem um formato inválido."
            )  

        if chegada <= partida: 
            raise ViagemInvalidaError(
                campo = "dataHoraSaida/dataHoraChegada",
                mensagem = "O campo dataHoraChegada deve ser posterior ao campo dataHoraSaida."
            )  

        duracao_real = int((chegada - partida).total_seconds() / 60)

        if duracao != duracao_real:
            raise ViagemInvalidaError(
                campo = "tempoEstimado",
                mensagem = "O tempo estimado não corresponde à diferença entre saída e chegada."
            )

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