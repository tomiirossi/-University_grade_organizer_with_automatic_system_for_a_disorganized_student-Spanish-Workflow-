"""
Cliente de Notion para el Organizador de Notas Universitarias.

Este modulo provee una clase cliente que encapsula las llamadas
a la API oficial de Notion para obtener paginas y bases de datos.
"""

import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()


def _get_token() -> str:
    """Obtiene el token de integracion de Notion desde las variables de entorno."""
    token = os.getenv("NOTION_TOKEN")
    if not token:
        raise EnvironmentError(
            "La variable de entorno NOTION_TOKEN no está configurada. "
            "Copia el archivo .env.example a .env y completa tu token de Notion."
        )
    return token


def get_client() -> Client:
    """Devuelve una instancia autenticada del cliente de Notion."""
    return Client(auth=_get_token())


def fetch_database(database_id: str) -> dict:
    """
    Obtiene todos los registros de una base de datos de Notion.

    Args:
        database_id: El ID de la base de datos en Notion.

    Returns:
        Un diccionario con los resultados paginados de la base de datos.
    """
    client = get_client()
    resultados = []
    siguiente_cursor = None

    while True:
        kwargs = {"database_id": database_id}
        if siguiente_cursor:
            kwargs["start_cursor"] = siguiente_cursor

        respuesta = client.databases.query(**kwargs)
        resultados.extend(respuesta.get("results", []))

        if not respuesta.get("has_more"):
            break
        siguiente_cursor = respuesta.get("next_cursor")

    return {"results": resultados, "total": len(resultados)}


def fetch_page(page_id: str) -> dict:
    """
    Obtiene el contenido de una pagina de Notion.

    Args:
        page_id: El ID de la pagina en Notion.

    Returns:
        Un diccionario con la informacion de la pagina.
    """
    client = get_client()
    return client.pages.retrieve(page_id=page_id)


def fetch_page_blocks(page_id: str) -> dict:
    """
    Obtiene los bloques (contenido) de una pagina de Notion,
    incluyendo bloques de codigo (code blocks).

    Args:
        page_id: El ID de la pagina en Notion.

    Returns:
        Un diccionario con todos los bloques de la pagina.
    """
    client = get_client()
    bloques = []
    siguiente_cursor = None

    while True:
        kwargs = {"block_id": page_id}
        if siguiente_cursor:
            kwargs["start_cursor"] = siguiente_cursor

        respuesta = client.blocks.children.list(**kwargs)
        bloques.extend(respuesta.get("results", []))

        if not respuesta.get("has_more"):
            break
        siguiente_cursor = respuesta.get("next_cursor")

    return {"results": bloques, "total": len(bloques)}


def fetch_code_blocks(page_id: str) -> list:
    """
    Obtiene unicamente los bloques de tipo 'code' de una pagina de Notion.

    Args:
        page_id: El ID de la pagina en Notion.

    Returns:
        Lista de bloques de codigo encontrados en la pagina.
    """
    todos_los_bloques = fetch_page_blocks(page_id)
    return [
        bloque
        for bloque in todos_los_bloques.get("results", [])
        if bloque.get("type") == "code"
    ]
