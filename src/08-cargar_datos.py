"""Carga productos de prueba en la tabla de DynamoDB.

Uso (desde AWS CloudShell o una terminal con credenciales del Learner Lab):
    python cargar_datos.py

No contiene llaves: boto3 toma las credenciales del entorno.
Variables opcionales: AWS_REGION (us-east-1 por defecto) y TABLE_NAME (Productos).
"""
import os

import boto3

REGION = os.environ.get("AWS_REGION", "us-east-1")
NOMBRE_TABLA = os.environ.get("TABLE_NAME", "Productos")

PRODUCTOS = [
    {"producto_id": "p-001", "nombre": "Rumours - Fleetwood Mac",
     "categoria": "vinilo", "precio": 699, "stock": 12, "imagen_url": ""},
    {"producto_id": "p-002", "nombre": "Abbey Road - The Beatles",
     "categoria": "CD", "precio": 299, "stock": 20, "imagen_url": ""},
    {"producto_id": "p-003", "nombre": "Random Access Memories - Daft Punk (Deluxe)",
     "categoria": "edicion especial", "precio": 1299, "stock": 5, "imagen_url": ""},
]


def main():
    tabla = boto3.resource("dynamodb", region_name=REGION).Table(NOMBRE_TABLA)
    for producto in PRODUCTOS:
        tabla.put_item(Item=producto)
        print("cargado:", producto["producto_id"], producto["nombre"])
    print(f"Listo: {len(PRODUCTOS)} productos en la tabla {NOMBRE_TABLA}.")


if __name__ == "__main__":
    main()
