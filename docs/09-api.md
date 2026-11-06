# Diseño de la API en API Gateway

## Datos generales
| Dato | Valor |
|---|---|
| API | `victorious-api` (REST, Regional) |
| Stage desplegado | `prod` |
| URL de invocación | `https://uq2wsjwg4f.execute-api.us-east-1.amazonaws.com/prod` |
| Destino | AWS Lambda `victorious-productos` |
| Autorización | Ninguna por ahora (Cognito planeado) |
| CORS | Habilitado (`OPTIONS` y encabezado `Access-Control-Allow-Origin`) |

La consola solo muestra la URL base del stage; cada recurso se agrega al final (por ejemplo `/productos`). La raíz `/` no tiene método.

## Cómo fluye un request
```
Cliente (S3 / curl) --HTTPS--> API Gateway --Lambda proxy--> Lambda --boto3--> DynamoDB
```
La respuesta regresa por el mismo camino.

## Integración: proxy
Se usa **Lambda proxy integration**: API Gateway le pasa a la función el request completo (método, ruta, cuerpo) y devuelve tal cual lo que la función responde (`statusCode`, `headers`, `body`).

**Por qué proxy:** hay menos configuración que con mapping templates, y la validación y las respuestas de error viven en un solo lugar (el código de la Lambda). **Desventaja:** la función debe construir la respuesta completa, incluidos los encabezados CORS.

## Recursos y métodos
| Recurso | Método | Tipo | Destino | Request | Response esperada | Estado |
|---|---|---|---|---|---|---|
| `/productos` | GET | Lambda proxy | `victorious-productos` | Sin cuerpo | 200 + lista en JSON | Desplegado |
| `/productos` | POST | Lambda proxy | `victorious-productos` | JSON con `nombre`, `categoria`, `precio`, `stock` (`imagen_url` opcional) | 201 + producto creado; 400 si faltan campos o el JSON es inválido | Desplegado |
| `/productos` | OPTIONS | Mock (CORS) | — | Preflight del navegador | 200 | Desplegado |
| `/productos/{id}` | GET | Lambda proxy | por crear | `id` en la ruta | 200 + producto; 404 si no existe | Planeado |
| `/productos/{id}` | DELETE | Lambda proxy | por crear | `id` en la ruta | 204; 404 si no existe | Planeado |
| `/pedidos` | POST | Lambda proxy | por crear | Producto y cantidad | 201 + pedido; 400 si no hay stock | Planeado |

## Validación y errores
La validación se hace **en la Lambda**, no en API Gateway:
- JSON mal formado → `400` con `{"error": "JSON inválido"}`.
- Faltan `nombre`, `categoria`, `precio` o `stock` → `400` con la lista de campos faltantes.
- Método distinto de GET o POST → `405`.

(Validar el request en API Gateway con un modelo es una mejora planeada.)

## Pruebas (curl)

**GET /productos**
```bash
curl https://uq2wsjwg4f.execute-api.us-east-1.amazonaws.com/prod/productos
```
Respuesta (`200`):
```json
[
  {"nombre": "Random Access Memories - Daft Punk (Deluxe)", "stock": 5, "imagen_url": "", "producto_id": "p-003", "categoria": "edicion especial", "precio": 1299},
  {"nombre": "Abbey Road - The Beatles", "stock": 20, "imagen_url": "", "categoria": "CD", "producto_id": "p-002", "precio": 299},
  {"nombre": "Rumours - Fleetwood Mac", "stock": 12, "imagen_url": "", "producto_id": "p-001", "categoria": "vinilo", "precio": 699}
]
```

**POST /productos**
```bash
curl -X POST https://uq2wsjwg4f.execute-api.us-east-1.amazonaws.com/prod/productos \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Dark Side of the Moon - Pink Floyd","categoria":"vinilo","precio":799,"stock":8}'
```
Respuesta (`201`):
```json
{"producto_id": "7c41eed6-5206-4594-afe3-1c03de9d6860", "nombre": "Dark Side of the Moon - Pink Floyd", "categoria": "vinilo", "precio": 799, "stock": 8, "imagen_url": ""}
```

**POST con campos faltantes**
```bash
curl -X POST https://uq2wsjwg4f.execute-api.us-east-1.amazonaws.com/prod/productos \
  -H "Content-Type: application/json" -d '{"nombre":"Incompleto"}'
```
Respuesta (`400`):
```json
{"error": "faltan campos: ['categoria', 'precio', 'stock']"}
```
