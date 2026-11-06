import json
import os
import uuid
from decimal import Decimal

import boto3

# El nombre de la tabla se toma de una variable de entorno (TABLE_NAME).
# Si no existe, se usa "Productos".
NOMBRE_TABLA = os.environ.get("TABLE_NAME", "Productos")
tabla = boto3.resource("dynamodb").Table(NOMBRE_TABLA)

CAMPOS_OBLIGATORIOS = ("nombre", "categoria", "precio", "stock")


def a_json(x):
    # DynamoDB devuelve los números como Decimal; json.dumps no los acepta.
    if isinstance(x, Decimal):
        return int(x) if x % 1 == 0 else float(x)
    if isinstance(x, list):
        return [a_json(i) for i in x]
    if isinstance(x, dict):
        return {k: a_json(v) for k, v in x.items()}
    return x


def respuesta(codigo, cuerpo):
    return {
        "statusCode": codigo,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(a_json(cuerpo)),
    }


def lambda_handler(event, context):
    metodo = event.get("httpMethod")

    if metodo == "GET":
        return respuesta(200, tabla.scan()["Items"])

    if metodo == "POST":
        try:
            datos = json.loads(event.get("body") or "{}")
        except json.JSONDecodeError:
            return respuesta(400, {"error": "JSON inválido"})

        faltan = [c for c in CAMPOS_OBLIGATORIOS if c not in datos]
        if faltan:
            return respuesta(400, {"error": f"faltan campos: {faltan}"})

        item = {
            "producto_id": str(uuid.uuid4()),
            "nombre": datos["nombre"],
            "categoria": datos["categoria"],
            "precio": Decimal(str(datos["precio"])),
            "stock": int(datos["stock"]),
            "imagen_url": datos.get("imagen_url", ""),
        }
        tabla.put_item(Item=item)
        return respuesta(201, item)

    return respuesta(405, {"error": "método no permitido"})
