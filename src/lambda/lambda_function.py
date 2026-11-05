import json
import uuid
import boto3
from decimal import Decimal

tabla = boto3.resource("dynamodb").Table("Productos")


def a_json(x):
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

        faltan = [c for c in ("nombre", "categoria", "precio", "stock") if c not in datos]
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
