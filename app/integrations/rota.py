class RotaIntegration:
    def reconhecer(self, viagem: dict):
        return "trip_id" in viagem


    def validar(self, viagem: dict):

        campos_obrigatorios = [
            "trip_id",
            "origem",
            "destino",
            "partida_em",
            "chegada_em",
            "duracao_minutos",
            "tarifa_centavos",
            "moeda",
            "classe",
            "vagas"
        ]

        for campo in campos_obrigatorios:
            if campo not in viagem:
                raise ViagemInvalidaError(
                    campo=campo,
                    mensagem=f"O campo {campo} é obrigatório."
                )

        if "municipio" not in viagem["origem"]:
            raise ViagemInvalidaError(
                campo="origem.municipio",
                mensagem="O campo origem.municipio é obrigatório."
            )

        if "estado" not in viagem["origem"]:
            raise ViagemInvalidaError(
                campo="origem.estado",
                mensagem="O campo origem.estado é obrigatório."
            )

        if "municipio" not in viagem["destino"]:
            raise ViagemInvalidaError(
                campo="destino.municipio",
                mensagem="O campo destino.municipio é obrigatório."
            )

        if "estado" not in viagem["destino"]:
            raise ViagemInvalidaError(
                campo="destino.estado",
                mensagem="O campo destino.estado é obrigatório."
            )

        if len(viagem["origem"]["estado"]) != 2:
            raise ViagemInvalidaError(
                campo="origem.estado",
                mensagem="O campo origem.estado deve conter exatamente 2 caracteres."
            )

        if len(viagem["destino"]["estado"]) != 2:
            raise ViagemInvalidaError(
                campo="destino.estado",
                mensagem="O campo destino.estado deve conter exatamente 2 caracteres."
            )

        try:
            duracao = int(viagem["duracao_minutos"])

        except (ValueError, TypeError):
            raise ViagemInvalidaError(
                campo="duracao_minutos",
                mensagem="O campo duracao_minutos deve ser um número inteiro."
            )

        try:
            tarifa = int(viagem["tarifa_centavos"])

        except (ValueError, TypeError):
            raise ViagemInvalidaError(
                campo="tarifa_centavos",
                mensagem="O campo tarifa_centavos deve ser um número inteiro."
            )

        try:
            vagas = int(viagem["vagas"])

        except (ValueError, TypeError):
            raise ViagemInvalidaError(
                campo="vagas",
                mensagem="O campo vagas deve ser um número inteiro."
            )

        if duracao <= 0:
            raise ViagemInvalidaError(
                campo="duracao_minutos",
                mensagem="O campo duracao_minutos deve representar uma duração positiva."
            )

        if tarifa <= 0:
            raise ViagemInvalidaError(
                campo="tarifa_centavos",
                mensagem="O campo tarifa_centavos deve representar um valor positivo."
            )

        if vagas < 0:
            raise ViagemInvalidaError(
                campo="vagas",
                mensagem="O campo vagas não pode ser negativo."
            )

        try:
            partida = datetime.fromisoformat(viagem["partida_em"])
            chegada = datetime.fromisoformat(viagem["chegada_em"])

        except (ValueError, TypeError):
            raise ViagemInvalidaError(
                campo="partida_em/chegada_em",
                mensagem="Os campos partida_em e chegada_em possuem um formato inválido."
            )

        if chegada <= partida:
            raise ViagemInvalidaError(
                campo="chegada_em",
                mensagem="O campo chegada_em deve ser posterior a partida_em."
            )

        duracao_real = int(
            (chegada - partida).total_seconds() / 60
        )

        if duracao != duracao_real:
            raise ViagemInvalidaError(
                campo="duracao_minutos",
                mensagem="A duração informada não corresponde à diferença entre partida e chegada."
            )

        categoria = viagem["classe"].lower()

        categorias_validas = [
            "convencional",
            "executivo",
            "semileito",
            "leito"
        ]

        if categoria not in categorias_validas:
            raise ViagemInvalidaError(
                campo="classe",
                mensagem="O campo classe deve ser um dos valores válidos."
            )


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

            "duracao_minutos": int(
                viagem["duracao_minutos"]
            ),

            "preco": {
                "valor": valor,
                "moeda": viagem["moeda"]
            },

            "categoria": categoria,

            "assentos_disponiveis": int(
                viagem["vagas"]
            )
        }