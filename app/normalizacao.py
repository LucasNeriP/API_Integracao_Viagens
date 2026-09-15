from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import tzdata  # noqa: F401  # banco IANA de fusos; necessário no Windows

from app.exceptions import ViagemInvalidaError

FUSO_PADRAO = ZoneInfo("America/Bahia")

# A chave é a categoria já simplificada (minúsculas, sem hífen/underscore).
# O valor é uma das quatro categorias oficiais do contrato de saída.
CATEGORIAS_OFICIAIS = {
    "convencional": "convencional",
    "executivo": "executivo",
    "exec": "executivo",
    "semileito": "semileito",
    "semisleeper": "semileito",
    "leito": "leito",
    "sleeper": "leito",
}


@dataclass(frozen=True)
class NomesDosCampos:
    """Guarda os nomes originais dos campos, para as mensagens de erro."""

    partida: str
    chegada: str
    duracao: str
    preco: str
    assentos: str
    uf_origem: str
    uf_destino: str
    categoria: str


def exigir_campos(payload: dict, campos: list[str], prefixo: str = "") -> None:
    """Garante que todos os campos obrigatórios existam e não sejam nulos."""

    for campo in campos:
        nome_completo = f"{prefixo}.{campo}" if prefixo else campo
        if campo not in payload or payload[campo] is None:
            raise ViagemInvalidaError(
                campo=nome_completo,
                mensagem=f"O campo {nome_completo} é obrigatório.",
            )


def exigir_objeto(payload: dict, campo: str) -> dict:
    """Garante que o campo exista e seja um objeto JSON (dicionário)."""

    exigir_campos(payload, [campo])
    valor = payload[campo]
    if not isinstance(valor, dict):
        raise ViagemInvalidaError(
            campo=campo,
            mensagem=f"O campo {campo} deve ser um objeto.",
        )
    return valor


def para_inteiro(valor, campo: str) -> int:
    try:
        return int(valor)
    except (TypeError, ValueError):
        raise ViagemInvalidaError(
            campo=campo,
            mensagem=f"O campo {campo} não pôde ser convertido para número inteiro.",
        )


def para_decimal(valor, campo: str) -> float:
    try:
        texto = str(valor).strip().replace(",", ".")
        return float(texto)
    except (TypeError, ValueError):
        raise ViagemInvalidaError(
            campo=campo,
            mensagem=f"O campo {campo} não pôde ser convertido para número decimal.",
        )


def interpretar_data_brasileira(valor, campo: str, nome_do_fuso: str) -> datetime:
    """Interpreta datas no formato dd/mm/aaaa HH:MM e aplica o fuso informado."""

    try:
        data = datetime.strptime(str(valor), "%d/%m/%Y %H:%M")
    except (TypeError, ValueError):
        raise ViagemInvalidaError(
            campo=campo,
            mensagem=f"O campo {campo} possui uma data em formato inválido.",
        )

    try:
        fuso = ZoneInfo(nome_do_fuso)
    except (ZoneInfoNotFoundError, TypeError, ValueError):
        raise ViagemInvalidaError(
            campo="fusoHorario",
            mensagem="O fuso horário informado é inválido.",
        )

    return data.replace(tzinfo=fuso)


def interpretar_data_iso(valor, campo: str) -> datetime:
    """
    Interpreta uma data ISO 8601.

    Se a data não tiver fuso, assume America/Bahia.
    O sufixo Z (UTC) é aceito e convertido para o fuso correspondente.
    """

    try:
        texto = str(valor).replace("Z", "+00:00")
        data = datetime.fromisoformat(texto)
    except (TypeError, ValueError):
        raise ViagemInvalidaError(
            campo=campo,
            mensagem=f"O campo {campo} possui uma data em formato inválido.",
        )

    if data.tzinfo is None:
        data = data.replace(tzinfo=FUSO_PADRAO)

    return data


def para_iso8601(data: datetime) -> str:
    """Converte a data para ISO 8601 no fuso homogêneo America/Bahia."""

    data_no_fuso_padrao = data.astimezone(FUSO_PADRAO).replace(microsecond=0)
    return data_no_fuso_padrao.isoformat()


def minutos_de_hh_mm(valor, campo: str) -> int:
    """Converte uma duração no formato HH:MM para minutos inteiros."""

    try:
        partes = str(valor).split(":")
        if len(partes) != 2:
            raise ValueError
        horas = int(partes[0])
        minutos = int(partes[1])
        if horas < 0 or minutos < 0 or minutos >= 60:
            raise ValueError
        return horas * 60 + minutos
    except (TypeError, ValueError):
        raise ViagemInvalidaError(
            campo=campo,
            mensagem=f"O campo {campo} possui uma duração em formato inválido.",
        )


def minutos_de_segundos(valor, campo: str) -> int:
    segundos = para_inteiro(valor, campo)
    return round(segundos / 60)


def minutos_de_horas(valor, campo: str) -> int:
    horas = para_decimal(valor, campo)
    return round(horas * 60)


def preco_de_texto_brasileiro(valor, campo: str) -> float:
    """Converte um preço no formato brasileiro, como '129,90'."""

    return round(para_decimal(valor, campo), 2)


def preco_de_centavos(valor, campo: str) -> float:
    centavos = para_inteiro(valor, campo)
    return round(centavos / 100, 2)


def preco_de_decimal(valor, campo: str) -> float:
    return round(para_decimal(valor, campo), 2)


def simplificar_categoria(valor: str) -> str:
    """Remove diferenças superficiais (maiúsculas, hífen, underscore, espaços)."""

    texto = str(valor).strip().lower()
    texto = texto.replace("_", " ").replace("-", " ")
    texto = "".join(texto.split())
    return texto


def normalizar_categoria(valor, campo: str) -> str:
    """
    Converte a categoria da companhia para uma das quatro oficiais:
    convencional, executivo, semileito ou leito.
    """

    try:
        chave = simplificar_categoria(valor)
    except (TypeError, AttributeError):
        raise ViagemInvalidaError(
            campo=campo,
            mensagem="A categoria não pôde ser normalizada.",
        )

    categoria = CATEGORIAS_OFICIAIS.get(chave)
    if categoria is None:
        raise ViagemInvalidaError(
            campo=campo,
            mensagem="A categoria não pôde ser normalizada.",
        )
    return categoria


def separar_cidade_e_uf(valor, campo: str) -> tuple[str, str]:
    """Separa um texto no formato 'Paulo Afonso/BA' em cidade e UF."""

    texto = str(valor).strip()
    if "/" not in texto:
        raise ViagemInvalidaError(
            campo=campo,
            mensagem=f"O campo {campo} deve estar no formato Cidade/UF.",
        )

    cidade, uf = texto.rsplit("/", 1)
    cidade = cidade.strip()
    uf = uf.strip()

    if not cidade or not uf:
        raise ViagemInvalidaError(
            campo=campo,
            mensagem=f"O campo {campo} deve estar no formato Cidade/UF.",
        )

    return cidade, uf


def aplicar_regras_comuns(
    partida: datetime,
    chegada: datetime,
    duracao_minutos: int,
    preco: float,
    assentos: int,
    uf_origem: str,
    uf_destino: str,
    campos: NomesDosCampos,
) -> None:
    """
    Aplica as regras de negócio que valem para todas as companhias.

    Cada estratégia já converteu os dados do seu formato específico.
    Daqui em diante, as regras são as mesmas.
    """

    if len(str(uf_origem)) != 2:
        raise ViagemInvalidaError(
            campo=campos.uf_origem,
            mensagem="A UF deve possuir exatamente dois caracteres.",
        )

    if len(str(uf_destino)) != 2:
        raise ViagemInvalidaError(
            campo=campos.uf_destino,
            mensagem="A UF deve possuir exatamente dois caracteres.",
        )

    if chegada <= partida:
        raise ViagemInvalidaError(
            campo=campos.chegada,
            mensagem="A data de chegada deve ser posterior à data de saída.",
        )

    if duracao_minutos <= 0:
        raise ViagemInvalidaError(
            campo=campos.duracao,
            mensagem="A duração deve ser maior que zero.",
        )

    duracao_calculada = round((chegada - partida).total_seconds() / 60)
    if duracao_minutos != duracao_calculada:
        raise ViagemInvalidaError(
            campo=campos.duracao,
            mensagem="A duração é incompatível com os horários de partida e chegada.",
        )

    if preco <= 0:
        raise ViagemInvalidaError(
            campo=campos.preco,
            mensagem="O preço deve ser maior que zero.",
        )

    if assentos < 0:
        raise ViagemInvalidaError(
            campo=campos.assentos,
            mensagem="A quantidade de assentos não pode ser negativa.",
        )
