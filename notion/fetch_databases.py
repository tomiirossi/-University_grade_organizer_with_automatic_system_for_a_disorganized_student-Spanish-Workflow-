"""
Script para obtener las bases de datos de Notion del Organizador Universitario.

Uso:
    python -m notion.fetch_databases

Variables de entorno requeridas (ver .env.example):
    NOTION_TOKEN, NOTION_DB_MATERIAS, NOTION_DB_NOTAS,
    NOTION_DB_TAREAS, NOTION_DB_EXAMENES
"""

import json
import os
from dotenv import load_dotenv
from notion.client import fetch_database

load_dotenv()

BASES_DE_DATOS = {
    "materias": os.getenv("NOTION_DB_MATERIAS"),
    "notas": os.getenv("NOTION_DB_NOTAS"),
    "tareas": os.getenv("NOTION_DB_TAREAS"),
    "examenes": os.getenv("NOTION_DB_EXAMENES"),
}


def obtener_todas_las_bases() -> dict:
    """
    Obtiene todas las bases de datos configuradas desde Notion.

    Returns:
        Diccionario con los resultados de cada base de datos.
    """
    resultados = {}
    for nombre, db_id in BASES_DE_DATOS.items():
        if not db_id:
            print(f"[AVISO] La variable de entorno para '{nombre}' no está configurada. Se omite.")
            continue
        print(f"Obteniendo base de datos '{nombre}' (ID: {db_id})...")
        try:
            resultados[nombre] = fetch_database(db_id)
            total = resultados[nombre]["total"]
            print(f"  -> {total} registro(s) obtenido(s) de '{nombre}'.")
        except Exception as e:
            print(f"  [ERROR] No se pudo obtener '{nombre}': {e}")
    return resultados


def main():
    print("=== Organizador Universitario - Importacion de Bases de Datos de Notion ===\n")
    datos = obtener_todas_las_bases()

    if datos:
        print("\nResumen:")
        for nombre, contenido in datos.items():
            print(f"  {nombre}: {contenido['total']} registro(s)")
        print("\nDatos obtenidos exitosamente.")
        print(json.dumps(datos, indent=2, ensure_ascii=False, default=str))
    else:
        print("\nNo se obtuvieron datos. Verifica que las variables de entorno estén configuradas.")


if __name__ == "__main__":
    main()
