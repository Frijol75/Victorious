# 3. Diseño de la API en API Gateway

| Dato | Valor |
|---|---|
| Tipo | REST API `victorious-api` (Regional) |
| Stage | `prod` |
| Integración | Lambda proxy hacia `victorious-productos` |
| Autorización | Ninguna (por ahora; Cognito está planeado) |
| CORS | Habilitado (origen `*`) para que la página en S3 pueda llamar a la API |
| URL base | `https://uq2wsjwg4f.execute-api.us-east-1.amazonaws.com/prod` |

## Rutas
| Método | Ruta | Descripción | Respuestas | Estado |
|---|---|---|---|---|
| GET | `/productos` | Lista el catálogo | 200 | Desplegado |
| POST | `/productos` | Crea un producto (`nombre`, `categoria`, `precio`, `stock`, `imagen_url` opcional) | 201, 400 si faltan campos | Desplegado |
| OPTIONS | `/productos` | Preflight de CORS | 200 | Desplegado |
| GET | `/productos/{id}` | Detalle de un producto | — | Planeado |
| POST | `/pedidos` | Registra una compra y descuenta stock | — | Planeado |

## Pruebas
```bash
curl https://uq2wsjwg4f.execute-api.us-east-1.amazonaws.com/prod/productos

curl -X POST https://uq2wsjwg4f.execute-api.us-east-1.amazonaws.com/prod/productos \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Dark Side of the Moon - Pink Floyd","categoria":"vinilo","precio":799,"stock":8}'
```

## Nota
La consola muestra solo la URL base del stage; la ruta `/productos` se agrega al final. La raíz `/` no tiene método.
