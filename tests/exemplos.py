URL = "/api/v1/viagens/normalizar"

PAYLOAD_PROGRESSO = {
    "codigoViagem": "PRG-2026-001",
    "cidadeOrigem": "Paulo Afonso",
    "ufOrigem": "BA",
    "cidadeDestino": "Recife",
    "ufDestino": "PE",
    "dataHoraSaida": "15/10/2026 06:30",
    "dataHoraChegada": "15/10/2026 12:50",
    "fusoHorario": "America/Bahia",
    "tempoEstimado": "06:20",
    "valorPassagem": "129,90",
    "tipoServico": "EXECUTIVO",
    "assentosDisponiveis": "18",
}

PAYLOAD_ROTA = {
    "trip_id": "ROT-2026-872",
    "origem": {
        "municipio": "Paulo Afonso",
        "estado": "BA",
    },
    "destino": {
        "municipio": "Aracaju",
        "estado": "SE",
    },
    "partida_em": "2026-10-15T07:00:00-03:00",
    "chegada_em": "2026-10-15T12:10:00-03:00",
    "duracao_minutos": 310,
    "tarifa_centavos": 8990,
    "moeda": "BRL",
    "classe": "convencional",
    "vagas": 22,
}

PAYLOAD_GONTIJO = {
    "serviceCode": "GON-2026-554",
    "from": {
        "city": "Paulo Afonso",
        "state": "BA",
    },
    "to": {
        "city": "Belo Horizonte",
        "state": "MG",
    },
    "departure": "2026-10-15T19:30:00Z",
    "arrival": "2026-10-16T12:10:00Z",
    "estimatedDurationSeconds": 60000,
    "fare": {
        "amount": "289.50",
        "currency": "BRL",
    },
    "serviceClass": "SEMI_SLEEPER",
    "availableSeats": 9,
}

PAYLOAD_SERTAO_BUS = {
    "numero": "SER-2026-100",
    "rota": {
        "partida": "Paulo Afonso/BA",
        "chegada": "Maceió/AL",
    },
    "horarios": {
        "saida": "2026-10-16T08:00:00-03:00",
        "chegada": "2026-10-16T13:30:00-03:00",
    },
    "duracao_horas": 5.5,
    "preco_total": 105.90,
    "moeda": "BRL",
    "servico": "EXEC",
    "lugares_livres": 14,
}

VIAGEM_PROGRESSO = {
    "id_viagem": "PRG-2026-001",
    "empresa": "Auto Viação Progresso",
    "origem": {"cidade": "Paulo Afonso", "uf": "BA"},
    "destino": {"cidade": "Recife", "uf": "PE"},
    "partida": "2026-10-15T06:30:00-03:00",
    "chegada": "2026-10-15T12:50:00-03:00",
    "duracao_minutos": 380,
    "preco": {"valor": 129.90, "moeda": "BRL"},
    "categoria": "executivo",
    "assentos_disponiveis": 18,
}

VIAGEM_ROTA = {
    "id_viagem": "ROT-2026-872",
    "empresa": "Rota Transportes",
    "origem": {"cidade": "Paulo Afonso", "uf": "BA"},
    "destino": {"cidade": "Aracaju", "uf": "SE"},
    "partida": "2026-10-15T07:00:00-03:00",
    "chegada": "2026-10-15T12:10:00-03:00",
    "duracao_minutos": 310,
    "preco": {"valor": 89.90, "moeda": "BRL"},
    "categoria": "convencional",
    "assentos_disponiveis": 22,
}

VIAGEM_GONTIJO = {
    "id_viagem": "GON-2026-554",
    "empresa": "Gontijo",
    "origem": {"cidade": "Paulo Afonso", "uf": "BA"},
    "destino": {"cidade": "Belo Horizonte", "uf": "MG"},
    "partida": "2026-10-15T16:30:00-03:00",
    "chegada": "2026-10-16T09:10:00-03:00",
    "duracao_minutos": 1000,
    "preco": {"valor": 289.50, "moeda": "BRL"},
    "categoria": "semileito",
    "assentos_disponiveis": 9,
}

VIAGEM_SERTAO_BUS = {
    "id_viagem": "SER-2026-100",
    "empresa": "Sertão Bus",
    "origem": {"cidade": "Paulo Afonso", "uf": "BA"},
    "destino": {"cidade": "Maceió", "uf": "AL"},
    "partida": "2026-10-16T08:00:00-03:00",
    "chegada": "2026-10-16T13:30:00-03:00",
    "duracao_minutos": 330,
    "preco": {"valor": 105.90, "moeda": "BRL"},
    "categoria": "executivo",
    "assentos_disponiveis": 14,
}
