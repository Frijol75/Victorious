# Pendientes para la entrega final

| Prioridad | Pendiente | Responsable |
|---|---|---|
| Alta | Tabla `Pedidos` y `POST /pedidos` con validación de stock y descuento (Lambda) | Luis |
| Alta | Cognito: registro, login y roles cliente / administrador; proteger rutas en API Gateway | Katherine |
| Alta | Carrito y compra simulada en la página de S3 | Jorge |
| Media | Fotos de productos en un bucket de S3 y llenar `imagen_url` | Jorge |
| Media | `GET /productos/{id}` y `DELETE /productos/{id}` | Luis |
| Media | Índices secundarios (`categoria-index`, `estatus-index`) | Jorge |
| Media | Panel administrativo: productos, pedidos y clientes | Todo el equipo |
| Media | Validar requests también en API Gateway y manejo de errores más completo | Luis |
| Baja | Restringir CORS al dominio del sitio en S3 (hoy es `*`) | Katherine |
| Baja | Permisos IAM mínimos en lugar de `LabRole`, si el lab lo permite | Luis |
| Baja | Pruebas del flujo completo de compra | Todo el equipo |

## Riesgos y plan B
- **El lab se reinicia y se pierden los recursos:** `docs/despliegue.md` y `src/scripts/cargar_datos.py` permiten recrear todo en pocos minutos.
- **Cognito (tema nuevo) tarda más de lo previsto:** plan B, un login simple con roles guardados en DynamoDB, validado en la Lambda.
