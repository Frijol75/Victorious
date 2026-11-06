# Victorious

Tienda en línea de productos musicales (vinilos, CDs y ediciones especiales), construida sobre servicios de AWS. Proyecto del curso Desarrollo en la Nube, ITESO.

**Equipo:** Jorge Eduardo Moreno Gutierrez, Katherine A. Perez Arambula, Luis Gerardo Cacho Nafarrate.
**Profesor:** Juan Carlos Jiménez Esquivel.

## Caso de uso de esta entrega
Un cliente abre la página de la tienda, consulta el catálogo de productos y puede agregar un producto nuevo. El flujo completo funciona de punta a punta en AWS:

```
Cliente (navegador)
   │  carga la página
   ▼
Amazon S3  ──────────────►  JavaScript de la página
                                   │  GET / POST /productos
                                   ▼
                          Amazon API Gateway
                                   │  Lambda proxy
                                   ▼
                             AWS Lambda
                                   │  boto3
                                   ▼
                          Amazon DynamoDB (tabla Productos)
```

URL de la API: `https://uq2wsjwg4f.execute-api.us-east-1.amazonaws.com/prod/productos`

## Entregables
| # | Entregable | Ubicación |
|---|---|---|
| 1 | Diagrama de la solución (desplegado y planeado) | [docs/01-diagrama.md](docs/01-diagrama.md) |
| 2 | Modelo de datos | [docs/02-modelo-datos.md](docs/02-modelo-datos.md) |
| 3 | Diseño de la API en API Gateway | [docs/03-api-gateway.md](docs/03-api-gateway.md) |
| 4 | Código fuente | [src/lambda/](src/lambda/) (función y Dockerfile) y [src/web/](src/web/) (página) |
| 5 | Evidencia de despliegue | [docs/05-evidencia.md](docs/05-evidencia.md) y [docs/evidencia/](docs/evidencia/) |
| 6 | Lista de pendientes para la final | [docs/06-pendientes.md](docs/06-pendientes.md) |

Además: [docs/despliegue.md](docs/despliegue.md) explica paso a paso cómo recrear todo en otro AWS Learner Lab.

## Por qué esta arquitectura
La idea fue usar los servicios de la guía del proyecto final y mantener la solución lo más simple posible: no administrar servidores, pagar solo por uso y poder demostrar el flujo completo en poco tiempo.

**Amazon DynamoDB: catálogo de productos.** El acceso principal es por clave (un producto por `producto_id`) y por listado. Es una base NoSQL sin esquema rígido, lo que permite agregar atributos a los productos sin migraciones. Con capacidad on-demand no hay que dimensionar nada, y encaja con el stock que debe actualizarse en cada compra.

**AWS Lambda: lógica de negocio.** La función valida los datos de entrada y escribe o lee en DynamoDB. Corre solo cuando alguien la llama, sin servidor activo, y es el mismo lugar donde en la final vivirá la validación de stock y el registro de pedidos.

**Amazon API Gateway: puerta de entrada.** Es un servicio agregado respecto a la guía inicial. Se incorporó porque una Lambda no tiene URL pública por sí sola: API Gateway expone las rutas `GET` y `POST /productos` por HTTPS, separa la interfaz del backend y será el punto donde se agregue autenticación con Cognito.

**Amazon S3: sitio web estático.** La tienda es una página HTML con JavaScript que consume la API, por lo que no necesita un servidor web. S3 la sirve con bajo costo y alta disponibilidad. En la final también guardará las fotos de los productos.

**CORS.** Como la página (S3) y la API (API Gateway) están en dominios distintos, el navegador exige CORS. La Lambda devuelve el encabezado `Access-Control-Allow-Origin` y API Gateway responde el `OPTIONS` previo.

## Decisiones y límites de esta versión
- Backend completamente serverless: sin EC2 ni administración de servidores.
- La API aún no tiene autenticación; Cognito está planeado para la final.
- CORS está abierto (`*`) para simplificar las pruebas; se restringirá al dominio del sitio.
- El listado usa `Scan`, aceptable con un catálogo pequeño; se cambiará por consultas con índices secundarios cuando crezca.
- `src/lambda/Dockerfile` empaqueta la función como imagen compatible con Lambda. El despliegue actual sube el código directamente en la consola; migrar a imagen de contenedor no es un requisito.

## Servicios de AWS utilizados
| Servicio | Uso |
|---|---|
| Amazon DynamoDB | Tabla `Productos` |
| AWS Lambda | Función `victorious-productos` (GET y POST) |
| Amazon API Gateway | API `victorious-api`, stage `prod` |
| Amazon S3 | Sitio web estático |

## Cómo probarlo
```bash
# Ver el catálogo
curl https://uq2wsjwg4f.execute-api.us-east-1.amazonaws.com/prod/productos

# Agregar un producto
curl -X POST https://uq2wsjwg4f.execute-api.us-east-1.amazonaws.com/prod/productos \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Dark Side of the Moon - Pink Floyd","categoria":"vinilo","precio":799,"stock":8}'
```
También se puede abrir la página del sitio en S3 y usar el formulario "Agregar producto".

## Estructura del repositorio
```
docs/            documentación, evidencia y guía de despliegue
src/lambda/      función Lambda (lambda_function.py) y Dockerfile
src/web/         página web estática que se sube a S3
```

## Siguientes pasos (resumen)
Tabla `Pedidos` y compra simulada con descuento de stock, autenticación y roles con Cognito, fotos de productos en S3 y panel administrativo. El detalle está en [docs/06-pendientes.md](docs/06-pendientes.md).
