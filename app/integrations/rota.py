from app.integrations.base import IntegracaoBase
from app.integrations.decorators import registrar_integracao

CATEGORIAS = {
    "executivo": "executivo",
    "convencional": "convencional",
    "semi-leito": "semileito",
    "leito": "leito"
}

@registrar_integracao
class RotaIntegration(IntegracaoBase):
    nome_empresa = "Rota Transportes"

    def reconhecer(self, viagem: dict):
        return "trip_id" in viagem

    def normalizar(self, viagem: dict):
        valor = viagem["tarifa_centavos"] / 100

        categoria_bruta = viagem["classe"].lower()
        categoria = CATEGORIAS.get(categoria_bruta, categoria_bruta)

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

            "categoria": categoria,

            "assentos_disponiveis": viagem["vagas"]
        }