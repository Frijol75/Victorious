# Cómo desplegar Victorious en tu propio AWS Learner Lab

Región: **us-east-1**. Rol de la Lambda: **LabRole**. Todo el código está en este repo.

## 1. DynamoDB
1. DynamoDB → *Create table*.
2. Nombre: `Productos` (exacto; la Lambda lo usa).
3. Partition key: `producto_id` (String). Sin sort key.
4. Capacity mode: On-demand → Create.

## 2. Lambda
1. Lambda → *Create function* → *Author from scratch*.
2. Nombre `victorious-productos`, runtime **Python 3.12**.
3. *Change default execution role* → *Use an existing role* → **LabRole**.
4. En la pestaña *Code*, pega el contenido de `src/lambda/lambda_function.py` en `lambda_function.py` y pulsa **Deploy**.

## 3. API Gateway
1. API Gateway → *Create API* → **REST API** (la normal) → nombre `victorious-api`, endpoint *Regional*.
2. *Create resource*: path `/`, nombre `productos`.
3. Sobre `/productos` → *Create method*: **GET**, tipo *Lambda function*, activar **Lambda proxy integration**, elegir `victorious-productos`.
4. Repetir para **POST** (mismas opciones).
5. Sobre `/productos` → *Enable CORS* (marcar GET y POST).
6. **Deploy API** → stage nuevo `prod`.
7. Tu URL queda así (el id es distinto en cada cuenta):
   `https://<TU-API-ID>.execute-api.us-east-1.amazonaws.com/prod/productos`
8. Prueba: abre esa URL en el navegador. Debe responder `[]` mientras la tabla esté vacía.

Cada vez que cambies algo en API Gateway, repite **Deploy API**.

## 4. Datos de prueba
Agrega productos con curl (cambia la URL por la tuya):
```bash
curl -X POST https://<TU-API-ID>.execute-api.us-east-1.amazonaws.com/prod/productos \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Rumours - Fleetwood Mac","categoria":"vinilo","precio":699,"stock":12}'
```

## 5. S3 (sitio web)
1. S3 → *Create bucket*. Nombre único en todo AWS (por ejemplo `victorious-web-<tu-nombre>`), región us-east-1.
2. Desmarcar **Block all public access** y confirmar.
3. *Properties* → *Static website hosting* → Enable → Index document `index.html`.
4. *Permissions* → *Bucket policy* (cambiar `TU-BUCKET`):
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "LecturaPublica",
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::TU-BUCKET/*"
  }]
}
```
5. Abre `src/web/index.html` y **cambia la constante `API`** por tu URL de API Gateway (paso 3.7).
6. Sube ese `index.html` al bucket y abre el *Bucket website endpoint* (*Properties* → *Static website hosting*).

## Notas
- Los recursos de un Learner Lab no se comparten entre cuentas: cada integrante tiene los suyos y su propia URL de API.
- Si el lab se reinicia por completo, puede que haya que recrear los recursos.
- Errores comunes: `Missing Authentication Token` (falta `/productos` en la URL o falta Deploy API) y página sin productos (falta CORS o el Deploy).
- El `Dockerfile` de `src/lambda/` solo empaqueta el código de la función; no crea recursos en AWS.
