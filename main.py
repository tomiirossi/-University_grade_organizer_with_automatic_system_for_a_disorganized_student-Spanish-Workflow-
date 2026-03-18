"""
Punto de entrada principal del Organizador de Notas Universitarias con Notion.

Uso:
    python main.py [--databases] [--pages]

Si no se pasan argumentos, ejecuta ambas operaciones.
"""

import argparse
import sys

from notion.fetch_databases import main as fetch_databases_main
from notion.fetch_pages import main as fetch_pages_main


def parse_args():
    parser = argparse.ArgumentParser(
        description="Organizador Universitario - Importacion desde Notion"
    )
    parser.add_argument(
        "--databases",
        action="store_true",
        help="Obtener bases de datos (materias, notas, tareas, examenes)",
    )
    parser.add_argument(
        "--pages",
        action="store_true",
        help="Obtener paginas y bloques de codigo",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    ejecutar_todo = not args.databases and not args.pages

    if args.databases or ejecutar_todo:
        fetch_databases_main()
        print()

    if args.pages or ejecutar_todo:
        fetch_pages_main()


if __name__ == "__main__":
    main()
