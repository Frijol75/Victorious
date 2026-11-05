# 1. Diagrama de la solución

Caso de uso de punta a punta: **consultar el catálogo (GET) y agregar un producto (POST)**.

```mermaid
flowchart LR
    C[Cliente<br/>navegador / curl]
    S3[Amazon S3<br/>sitio web estático]
    APIGW[Amazon API Gateway<br/>victorious-api - stage prod]
    LAM[AWS Lambda<br/>victorious-productos]
    DDB[(Amazon DynamoDB<br/>tabla Productos)]

    C -->|carga la página| S3
    C -->|GET / POST /productos| APIGW
    APIGW -->|Lambda proxy| LAM
    LAM -->|boto3| DDB

    subgraph Planeado
        S3F[Amazon S3<br/>fotos de productos]
        COG[Amazon Cognito<br/>cliente / administrador]
        PED[(DynamoDB<br/>tabla Pedidos)]
    end

    C -.-> COG
    LAM -.-> PED
    S3F -.-> S3

    style Planeado stroke-dasharray: 5 5
```

Línea continua: **desplegado**. Línea punteada y recuadro "Planeado": **pendiente para la final**.

| Componente | Estado |
|---|---|
| DynamoDB (tabla Productos) | Desplegado |
| Lambda `victorious-productos` (GET y POST) | Desplegado |
| API Gateway `victorious-api` (GET y POST /productos, con CORS) | Desplegado (servicio agregado respecto a la guía inicial) |
| S3: sitio web estático | Desplegado |
| S3: fotos de productos | Planeado |
| Cognito, tabla Pedidos | Planeado |
