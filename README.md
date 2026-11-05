# Victorious

Tienda en línea de productos musicales (vinilos, CDs y ediciones especiales). Proyecto del curso Desarrollo en la Nube, ITESO.

**Equipo:** Jorge Eduardo Moreno Gutierrez, Katherine A. Perez Arambula, Luis Gerardo Cacho Nafarrate.
**Profesor:** Juan Carlos Jiménez Esquivel.

## Caso de uso de punta a punta
Consultar el catálogo de productos y agregar un producto nuevo.

**Flujo:** Cliente → Amazon S3 (página web) → Amazon API Gateway → AWS Lambda → Amazon DynamoDB.

URL de la API: `https://uq2wsjwg4f.execute-api.us-east-1.amazonaws.com/prod/productos`

## Entregables
| # | Entregable | Ubicación |
|---|---|---|
| 1 | Diagrama de la solución (desplegado y planeado) | [docs/01-diagrama.md](docs/01-diagrama.md) |
| 2 | Modelo de datos | [docs/02-modelo-datos.md](docs/02-modelo-datos.md) |
| 3 | Diseño de la API en API Gateway | [docs/03-api-gateway.md](docs/03-api-gateway.md) |
| 4 | Código fuente | [src/lambda/lambda_function.py](src/lambda/lambda_function.py) y [src/web/index.html](src/web/index.html) |
| 5 | Evidencia de despliegue | [docs/05-evidencia.md](docs/05-evidencia.md) y `docs/evidencia/` |
| 6 | Lista de pendientes para la final | [docs/06-pendientes.md](docs/06-pendientes.md) |

## Decisión de arquitectura
El backend corre en **AWS Lambda** en lugar de un contenedor en EC2, porque Lambda es uno de los servicios de nuestra guía de proyecto final y EC2 no lo es. Por esa razón este repositorio no incluye Dockerfile. API Gateway se agregó respecto a la guía inicial porque expone la Lambda con una URL pública.

## Servicios de AWS utilizados
- Amazon DynamoDB: tabla `Productos`.
- AWS Lambda: función `victorious-productos` (GET y POST).
- Amazon API Gateway: API `victorious-api`, stage `prod`.
- Amazon S3: sitio web estático.

## Estructura
```
docs/            documentación y evidencia
src/lambda/      código de la función Lambda
src/web/         página web estática (se sube a S3)
```
