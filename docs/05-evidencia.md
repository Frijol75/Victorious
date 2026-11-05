# 5. Evidencia de despliegue

Las capturas van en `docs/evidencia/`. No incluir tokens de sesión (`X-Amz-Security-Token`).

| # | Evidencia | Archivo | Hecho |
|---|---|---|---|
| 1 | Tabla `Productos` en DynamoDB con items | `evidencia/dynamodb.png` | [ ] |
| 2 | Lambda `victorious-productos` (código y rol LabRole) | `evidencia/lambda.png` | [ ] |
| 3 | API Gateway: Resources con GET y POST en /productos | `evidencia/apigw-resources.png` | [ ] |
| 4 | Stage `prod` con Invoke URL | `evidencia/apigw-stage.png` | [ ] |
| 5 | GET en el navegador con la URL completa y el JSON | `evidencia/get.png` | [ ] |
| 6 | POST con curl y su respuesta 201 | `evidencia/post.png` | [ ] |
| 7 | El producto nuevo en DynamoDB y en el siguiente GET | `evidencia/post-verificacion.png` | [ ] |
| 8 | POST con campos faltantes (respuesta 400) | `evidencia/post-error.png` | [ ] |
| 9 | Bucket S3 con `index.html` y static website hosting activado | `evidencia/s3-bucket.png` | [ ] |
| 10 | Página en el navegador mostrando el catálogo (URL del bucket visible) | `evidencia/s3-pagina.png` | [ ] |

Flujo demostrado: Cliente → S3 (página) → API Gateway → Lambda → DynamoDB.
