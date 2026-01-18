from openai import OpenAI
from decouple import config
import json
import re

client = OpenAI(
    api_key=config("OPENAI_API_KEY")
)

def interpretar_mensaje(mensaje):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"""
Devuelve EXCLUSIVAMENTE JSON válido.
NO texto adicional.
NO markdown.

Formato exacto:
{{
  "accion": "registrar_venta | consultar_stock | productos_mas_vendidos | listar_productos | pedir_aclaracion",
  "producto": null,
  "cantidad": null
}}

Reglas:
- Si el mensaje pregunta por TODOS los productos, inventario o lista → listar_productos
- Si el mensaje pregunta por productos más vendidos → productos_mas_vendidos
- Si falta información → pedir_aclaracion
- Si no se menciona cantidad → usar 1

Mensaje: "{mensaje}"
"""
    )

    texto = response.output_text

    if not texto:
        return {"accion": "pedir_aclaracion"}

    match = re.search(r"\{.*\}", texto, re.DOTALL)

    if not match:
        return {"accion": "pedir_aclaracion"}

    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        return {"accion": "pedir_aclaracion"}

