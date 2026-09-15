# API de Integração de Viagens

API em Python/FastAPI que recebe viagens de companhias distintas, identifica a origem pela estrutura de cada objeto e devolve um contrato homogêneo.

Companhias suportadas:

- Auto Viação Progresso
- Rota Transportes
- Gontijo
- Sertão Bus (companhia fictícia, usada para demonstrar extensibilidade)

## Instalação

Na raiz do projeto:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

Linux/macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Execução

```bash
uvicorn app.main:app --reload
```

A documentação interativa fica em `http://127.0.0.1:8000/docs`.

Endpoint principal:

```
POST /api/v1/viagens/normalizar
```

O corpo da requisição é um array JSON. Não existe campo `empresa`, `companhia` ou equivalente: cada objeto é reconhecido pela própria estrutura.

Exemplo:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/viagens/normalizar ^
  -H "Content-Type: application/json" ^
  -d "[{\"codigoViagem\":\"PRG-2026-001\",\"cidadeOrigem\":\"Paulo Afonso\",\"ufOrigem\":\"BA\",\"cidadeDestino\":\"Recife\",\"ufDestino\":\"PE\",\"dataHoraSaida\":\"15/10/2026 06:30\",\"dataHoraChegada\":\"15/10/2026 12:50\",\"fusoHorario\":\"America/Bahia\",\"tempoEstimado\":\"06:20\",\"valorPassagem\":\"129,90\",\"tipoServico\":\"EXECUTIVO\",\"assentosDisponiveis\":\"18\"}]"
```

## Testes

```bash
pytest
```

Os testes estão separados por companhia. Incluir uma nova integração não exige alterar os testes das demais.

## Decisões de projeto

A solução combina **Strategy** e **Registry** para atender o princípio **Aberto/Fechado (OCP)** sem usar uma cadeia de `if/elif/else` para escolher a companhia.

### Strategy

Cada companhia é uma estratégia que implementa a mesma interface (`IntegracaoCompanhia`):

- `reconhecer(payload)`: decide se o objeto pertence a ela
- `validar(payload)`: aplica as regras daquele formato
- `normalizar(payload)`: converte para o contrato de saída

O fluxo principal não interpreta `codigoViagem`, `trip_id` ou `serviceCode`. Ele apenas pede à estratégia identificada que processe o objeto.

Essa escolha deixa o código didático: a regra de cada empresa fica no próprio arquivo, sem misturar formatos no endpoint.

### Registry

As estratégias são cadastradas em um registro (`RegistroDeIntegracoes`). A identificação percorre a lista de estratégias e devolve a primeira que reconhecer o payload.

Isso substitui o trecho que o enunciado proíbe:

```python
# Não fazemos isto:
if "codigoViagem" in payload:
    ...
elif "trip_id" in payload:
    ...
elif "serviceCode" in payload:
    ...
```

O equivalente aberto à extensão é:

```python
for estrategia in self._estrategias:
    if estrategia.reconhecer(payload):
        return estrategia
```

Uma companhia nova não cria outro `elif` no fluxo principal. Ela apenas entra no registro.

O cadastro é feito pelo decorator `@registrar_integracao`. Os módulos da pasta `app/integrations/` são carregados automaticamente: criar o arquivo da nova companhia já a coloca no sistema.

### SOLID

- **S (Responsabilidade Única):** cada classe de integração trata de uma companhia; o endpoint só recebe HTTP; o serviço só orquestra.
- **O (Aberto/Fechado):** novas companhias entram por extensão (nova estratégia + registro), sem alterar o endpoint, o contrato de saída ou as integrações existentes.
- **L (Substituição de Liskov):** qualquer estratégia pode substituir outra no Registry, porque todas seguem `IntegracaoCompanhia`.
- **I (Segregação de Interface):** a interface tem só o que o fluxo precisa: reconhecer, validar e normalizar.
- **D (Inversão de Dependência):** o serviço depende da abstração `IntegracaoCompanhia`, não de Progresso, Rota ou Gontijo.

O método `processar` da classe base também aplica um **Template Method** simples: toda companhia valida e depois normaliza, na mesma ordem.

### Por que não priorizar performance

O código repete algumas conversões entre `validar` e `normalizar` de propósito. Em um sistema acadêmico, é mais importante conseguir ler o arquivo de uma companhia de ponta a ponta do que evitar uma segunda interpretação de data.

## Estrutura

```
app/
  main.py                 # endpoint FastAPI e tratamento HTTP 422
  servico.py              # fluxo principal (não conhece companhias)
  schemas.py              # contrato homogêneo de saída
  normalizacao.py         # regras comuns (data, preço, categoria, UF)
  exceptions.py
  integrations/
    base.py               # Strategy (interface)
    registry.py           # Registry + decorator
    progresso.py
    rota.py
    gontijo.py
    sertao_bus.py
tests/
```

## Como adicionar uma companhia

Não altere o endpoint, o contrato de entrada/saída, o loop de `servico.py` nem os testes das outras empresas.

1. Crie um arquivo em `app/integrations/`, por exemplo `nova_companhia.py`.
2. Implemente uma classe que herde de `IntegracaoCompanhia`.
3. Decore a classe com `@registrar_integracao`.
4. Em `reconhecer`, use um campo ou uma combinação de campos exclusiva dessa empresa.
5. Em `validar` e `normalizar`, leia o formato próprio e aproveite os utilitários de `app/normalizacao.py` para as regras comuns.
6. Crie testes só dessa companhia em `tests/test_nova_companhia.py`.

Esqueleto:

```python
from app.integrations.base import IntegracaoCompanhia
from app.integrations.registry import registrar_integracao


@registrar_integracao
class IntegracaoNovaCompanhia(IntegracaoCompanhia):
    nome_empresa = "Nova Companhia"

    def reconhecer(self, payload: dict) -> bool:
        return "campo_exclusivo" in payload

    def validar(self, payload: dict) -> None:
        ...

    def normalizar(self, payload: dict) -> dict:
        ...
```

A Sertão Bus foi incluída exatamente nesse modelo: arquivo novo, decorator e testes próprios, sem mudar Progresso, Rota ou Gontijo.

## Validações

Se qualquer objeto da lista for inválido, a API rejeita a requisição inteira com HTTP 422 e não devolve resultados parciais:

```json
{
  "detail": {
    "indice": 1,
    "empresa_identificada": "Rota Transportes",
    "campo": "chegada_em",
    "mensagem": "A data de chegada deve ser posterior à data de saída."
  }
}
```

Quando o formato não é reconhecido, `empresa_identificada` e `campo` vêm como `null`.
