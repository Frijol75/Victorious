# 2. Modelo de datos

## Tabla `Productos` (desplegada)
| Elemento | Valor |
|---|---|
| Partition Key | `producto_id` (String, UUID generado por la Lambda) |
| Sort Key | — |
| Capacidad | On-demand |
| Atributos | `nombre`, `categoria` (vinilo / CD / edicion especial), `precio`, `stock`, `imagen_url` |
| GSI (planeado) | `categoria-index` (PK: `categoria`) para filtrar el catálogo |

Patrones de acceso: listar catálogo (Scan), agregar producto (PutItem), filtrar por categoría (GSI, planeado).

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

## Tabla `Pedidos` (planeada)
| Elemento | Valor |
|---|---|
| Partition Key | `usuario_id` |
| Sort Key | `fecha_hora` |
| Atributos | `producto_id`, `cantidad`, `estatus`, `total` |
| GSI | `estatus-index` para ver pedidos pendientes |
