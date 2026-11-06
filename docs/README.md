# Victorious

Tienda en línea de productos musicales (vinilos, CDs y ediciones especiales), construida sobre servicios de AWS. Proyecto del curso Desarrollo en la Nube, ITESO.

**Integrantes:** Jorge Eduardo Moreno Gutierrez, Katherine A. Perez Arambula, Luis Gerardo Cacho Nafarrate.
**Profesor:** Juan Carlos Jiménez Esquivel.

## Caso de uso de esta entrega
Un cliente abre la página de la tienda, consulta el catálogo de productos y puede agregar uno nuevo. El flujo completo funciona de punta a punta en AWS:

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
| 1 | Diagrama de la solución | [docs/solucion.png](docs/solucion.png) |
| 2 | Modelo de datos | [docs/modelo-datos.md](docs/modelo-datos.md) |
| 3 | Diseño de la API en API Gateway | [docs/api.md](docs/api.md) |
| 4 | Código fuente | [src/lambda/](src/lambda/) (función y Dockerfile), [src/web/](src/web/) (página) y [src/scripts/](src/scripts/) (script boto3) |
| 5 | Evidencia de despliegue | [docs/evidencia/](docs/evidencia/) (checklist en [docs/05-evidencia.md](docs/05-evidencia.md)) |
| 6 | Pendientes para la final | [docs/pendientes.md](docs/pendientes.md) |

## Por qué esta arquitectura
La solución usa servicios administrados para no mantener servidores, pagar solo por uso y poder demostrar el flujo completo en poco tiempo. Por indicación del profesor no se usó EC2; el backend corre en AWS Lambda.

| Decisión | Alternativa considerada | Por qué elegimos esta | Desventajas |
|---|---|---|---|
| **DynamoDB** para el catálogo | Amazon RDS | El acceso es por clave (un producto por id) y por listado; no hay esquema rígido ni servidor que administrar; con capacidad on-demand no hay que dimensionar nada | Las consultas complejas (varios filtros, reportes, joins) son más difíciles y requieren índices; si el proyecto necesitara reportes relacionales, RDS sería mejor |
| **Lambda** como backend | Contenedor Docker en EC2 | Sin instancia encendida ni sistema operativo que mantener; se paga por ejecución; se despliega en minutos y no depende de que una instancia siga viva | Arranque en frío, límite de tiempo por ejecución, menos control del entorno y depuración menos directa |
| **API Gateway** como entrada | URL de función de Lambda | Define rutas y métodos, stages, CORS y permite proteger rutas con Cognito en la final | Un servicio más que configurar; hay que hacer *Deploy* por cada cambio |
| **S3** para la página | Servir la página desde un servidor | Bajo costo y alta disponibilidad, sin servidor web | Solo contenido estático (lo dinámico lo aporta JavaScript con la API) y el endpoint de sitio web usa HTTP, no HTTPS |

**CORS:** la página (S3) y la API (API Gateway) están en dominios distintos, por lo que el navegador exige CORS. La Lambda devuelve `Access-Control-Allow-Origin` y API Gateway responde el `OPTIONS` previo.

## Límites de esta versión
- La API aún no tiene autenticación; Cognito está planeado para la final.
- CORS está abierto (`*`) para simplificar las pruebas.
- El listado usa `Scan`, aceptable con un catálogo pequeño.
- `src/lambda/Dockerfile` empaqueta la función como imagen compatible con Lambda; el despliegue actual sube el código directamente en la consola.
- No hay llaves ni contraseñas en el código: la Lambda usa el rol `LabRole` y la tabla se configura con la variable `TABLE_NAME`.

## Cómo correrlo (o recrearlo en otro Learner Lab)
La guía paso a paso está en [docs/despliegue.md](docs/despliegue.md): tabla, Lambda, API Gateway con CORS y sitio en S3. Los datos de prueba se cargan con `python src/scripts/cargar_datos.py` o con el POST de la API.

Probar la API:
```bash
curl https://uq2wsjwg4f.execute-api.us-east-1.amazonaws.com/prod/productos

curl -X POST https://uq2wsjwg4f.execute-api.us-east-1.amazonaws.com/prod/productos \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Dark Side of the Moon - Pink Floyd","categoria":"vinilo","precio":799,"stock":8}'
```
También se puede abrir la página del sitio en S3 y usar el formulario "Agregar producto".

## Estructura del repositorio
```
docs/            diagrama, modelo de datos, API, pendientes y evidencia
src/lambda/      función Lambda y Dockerfile
src/web/         página web estática que se sube a S3
src/scripts/     script boto3 para cargar datos de prueba
```
