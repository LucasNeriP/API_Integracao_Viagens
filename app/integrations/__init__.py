"""
Pacote das estratégias de companhia.

Ao importar este pacote, todos os módulos de companhia são carregados.
Cada módulo usa o decorator @registrar_integracao, então as estratégias
entram sozinhas no Registry.

Para adicionar uma companhia, basta criar um novo arquivo neste diretório
com a classe decorada. Não é necessário alterar o endpoint, o Registry
nem as demais integrações.
"""

from pathlib import Path
import importlib

_MODULOS_DE_INFRAESTRUTURA = {"base", "registry"}


def _carregar_estrategias() -> None:
    pasta_atual = Path(__file__).parent

    for arquivo in sorted(pasta_atual.glob("*.py")):
        nome_do_modulo = arquivo.stem
        if nome_do_modulo.startswith("_"):
            continue
        if nome_do_modulo in _MODULOS_DE_INFRAESTRUTURA:
            continue
        importlib.import_module(f"app.integrations.{nome_do_modulo}")


_carregar_estrategias()
