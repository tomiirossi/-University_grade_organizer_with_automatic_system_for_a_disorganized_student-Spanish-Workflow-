"""
Script para obtener paginas y bloques de codigo de Notion
del Organizador Universitario.

Uso:
    python -m notion.fetch_pages

Variables de entorno requeridas (ver .env.example):
    NOTION_TOKEN
    NOTION_PAGE_IDS (IDs separados por coma, opcional)
"""

import json
import os
from dotenv import load_dotenv
from notion.client import fetch_page, fetch_page_blocks, fetch_code_blocks

load_dotenv()


def obtener_paginas(page_ids: list) -> dict:
    """
    Obtiene el contenido de una lista de paginas de Notion.

    Args:
        page_ids: Lista de IDs de paginas en Notion.

    Returns:
        Diccionario con la informacion de cada pagina.
    """
    resultados = {}
    for page_id in page_ids:
        page_id = page_id.strip()
        if not page_id:
            continue
        print(f"Obteniendo pagina (ID: {page_id})...")
        try:
            pagina = fetch_page(page_id)
            bloques = fetch_page_blocks(page_id)
            codigos = fetch_code_blocks(page_id)
            titulo = _extraer_titulo(pagina)
            resultados[page_id] = {
                "titulo": titulo,
                "pagina": pagina,
                "bloques": bloques,
                "bloques_de_codigo": codigos,
            }
            print(f"  -> Pagina '{titulo}': {bloques['total']} bloque(s), {len(codigos)} codigo(s).")
        except Exception as e:
            print(f"  [ERROR] No se pudo obtener la pagina '{page_id}': {e}")
    return resultados


def _extraer_titulo(pagina: dict) -> str:
    """Extrae el titulo de una pagina de Notion."""
    try:
        propiedades = pagina.get("properties", {})
        for prop in propiedades.values():
            if prop.get("type") == "title":
                partes = prop.get("title", [])
                return "".join(parte.get("plain_text", "") for parte in partes)
    except Exception:
        pass
    return pagina.get("id", "Sin titulo")


def main():
    print("=== Organizador Universitario - Importacion de Paginas y Codigos de Notion ===\n")

    ids_env = os.getenv("NOTION_PAGE_IDS", "")
    page_ids = [pid.strip() for pid in ids_env.split(",") if pid.strip()] if ids_env else []

    if not page_ids:
        print(
            "No se encontraron IDs de paginas. "
            "Define la variable NOTION_PAGE_IDS en tu archivo .env con los IDs separados por coma."
        )
        return

    datos = obtener_paginas(page_ids)

    if datos:
        total_codigos = sum(len(v["bloques_de_codigo"]) for v in datos.values())
        print(f"\nResumen: {len(datos)} pagina(s), {total_codigos} bloque(s) de codigo en total.")
        print(json.dumps(datos, indent=2, ensure_ascii=False, default=str))
    else:
        print("\nNo se obtuvieron datos.")


if __name__ == "__main__":
    main()
