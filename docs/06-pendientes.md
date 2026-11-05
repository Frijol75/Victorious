# 6. Lista de pendientes para la final

## Alta prioridad
- [ ] Tabla `Pedidos` y `POST /pedidos` con validación de stock y descuento (Lambda).
- [ ] Cognito: registro/login y roles cliente / administrador; proteger rutas en API Gateway.
- [ ] Carrito y compra simulada en la página web.

## Media prioridad
- [ ] S3: fotos de productos (`victorious-productos`) y llenar `imagen_url`.
- [ ] `GET /productos/{id}`, `PUT` y `DELETE` para el panel de administración.
- [ ] GSI por categoría y por estatus.
- [ ] Panel administrativo: productos, pedidos y clientes.
- [ ] Pruebas del flujo completo de compra.

## Calidad y seguridad
- [ ] Restringir CORS al dominio del sitio en S3 en lugar de `*`.
- [ ] Separar el código de la Lambda por rutas / funciones.
- [ ] Rol IAM con permisos mínimos en lugar de LabRole (si el lab lo permite).

## Reparto sugerido (según la guía)
| Persona | Pendiente principal |
|---|---|
| Jorge | S3 (fotos) y tablas DynamoDB (Pedidos, GSI) |
| Katherine | Cognito |
| Luis | Lambda de compra e IAM |
