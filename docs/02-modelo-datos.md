# Modelo de datos

Base de datos: **Amazon DynamoDB** (NoSQL, clave-valor). Se eligió porque el acceso principal es por clave y por listado, y no se necesitan joins ni un esquema rígido. Detalle de la decisión en el [README](../README.md).

## Tabla `Productos` (desplegada)

| Elemento | Valor |
|---|---|
| Partition Key (PK) | `producto_id` (String) |
| Sort Key (SK) | no tiene |
| Capacidad | On-demand |
| Índices secundarios | ninguno por ahora (planeado: `categoria-index`) |

**Por qué esa clave:** cada producto es único y se identifica por su id (la Lambda genera un UUID). Con `producto_id` como PK, buscar un producto es una lectura directa, y los items se reparten bien entre particiones.

| Atributo | Tipo | Descripción | Ejemplo |
|---|---|---|---|
| `producto_id` | String (PK) | Identificador único | `p-001` |
| `nombre` | String | Título del producto | `Rumours - Fleetwood Mac` |
| `categoria` | String | `vinilo`, `CD` o `edicion especial` | `vinilo` |
| `precio` | Number | Precio en pesos | `699` |
| `stock` | Number | Piezas disponibles | `12` |
| `imagen_url` | String | URL de la foto (vacío por ahora) | `""` |

Ejemplo de item:
```json
{
  "producto_id": "p-001",
  "nombre": "Rumours - Fleetwood Mac",
  "categoria": "vinilo",
  "precio": 699,
  "stock": 12,
  "imagen_url": ""
}
```

**Datos de prueba cargados:** Rumours (vinilo), Abbey Road (CD), Random Access Memories Deluxe (edición especial), más los productos agregados mediante el POST. El script `src/scripts/cargar_datos.py` carga los datos iniciales.

## Consultas principales

| # | Consulta | Operación DynamoDB | Endpoint | Estado |
|---|---|---|---|---|
| 1 | Listar el catálogo completo | `Scan` | `GET /productos` | Desplegada |
| 2 | Agregar un producto nuevo | `PutItem` | `POST /productos` | Desplegada |
| 3 | Obtener un producto por su id | `GetItem` (por PK) | `GET /productos/{id}` | Planeada |
| 4 | Filtrar el catálogo por categoría | `Query` sobre `categoria-index` | `GET /productos?categoria=vinilo` | Planeada |

`Scan` es aceptable con un catálogo pequeño; al crecer se reemplaza por consultas con índices.

## Tabla `Pedidos` (planeada)

| Elemento | Valor |
|---|---|
| Partition Key | `usuario_id` (String) |
| Sort Key | `fecha_hora` (String, ISO 8601) |
| Atributos | `producto_id`, `cantidad`, `estatus`, `total` |
| Índice secundario | `estatus-index` (PK: `estatus`) para ver pedidos pendientes |

Consultas principales: *todos los pedidos de un usuario* (`Query` por `usuario_id`, ordenados por fecha) y *pedidos pendientes* (`Query` sobre `estatus-index`).

Al confirmar una compra, la Lambda registrará el pedido y descontará el `stock` del producto.
