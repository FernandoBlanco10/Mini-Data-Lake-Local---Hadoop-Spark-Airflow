# Mini Data Lake Local

Proyecto de aprendizaje para entender, paso a paso, como se conectan varias piezas tipicas de una arquitectura de ingenieria de datos:

- Airflow para orquestacion
- Spark para procesamiento
- HDFS para almacenamiento distribuido
- PostgreSQL para persistencia relacional
- Docker para empaquetar y levantar todo en local

La idea del proyecto no es solo "hacer que funcione", sino entender por que existe cada componente y como se parece a un entorno en Azure.

## Objetivo

Este laboratorio intenta simular una arquitectura de datos simple:

1. Airflow dispara un DAG.
2. El DAG lanza un job de Spark.
3. Spark lee un archivo de ventas.
4. Spark transforma los datos.
5. Spark guarda una version procesada en HDFS.
6. Spark carga los resultados en PostgreSQL.

Piensalo como una cadena de cocina:

- Airflow es el chef que coordina la receta.
- Spark es la estufa y el cocinero que procesa los ingredientes.
- HDFS es la alacena donde se guardan insumos y resultados.
- PostgreSQL es el refrigerador donde dejas el platillo listo para consumir.
- Docker es el edificio donde vive toda la cocina.

## Arquitectura en una frase

Airflow orquesta, Spark procesa, HDFS almacena, PostgreSQL persiste.

## Mapa del proyecto

### `airflow/`

Aqui vive la parte de orquestacion.

- `airflow/dags/spark_sales_dag.py`
  - Define el DAG que lanza el job de Spark.
  - En Azure, esto se parece a Azure Data Factory, Azure Synapse Pipelines o Airflow administrado.

- `airflow/Dockerfile`
  - Crea una imagen custom de Airflow con Spark client y el provider de Spark.
  - En Azure, el equivalente conceptual seria un entorno administrado o una imagen custom en Container Registry.

### `spark/`

Aqui vive el trabajo pesado.

- `spark/jobs/process_sales.py`
  - Lee el CSV.
  - Calcula `venta_total`.
  - Escribe el resultado en HDFS.
  - Carga el resultado en PostgreSQL.
  - En Azure, esto se parece mucho a un notebook o job de Azure Databricks, o a un Spark job en Synapse.

- `spark/data/sales.csv`
  - Datos de entrada del laboratorio.
  - En Azure, esto se pareceria a un archivo en ADLS Gen2 o Blob Storage.

- `spark/output/`
  - Fue util al inicio para pruebas locales.
  - Hoy el proyecto ya quedo mas alineado con HDFS, que es mejor para aprender una arquitectura distribuida.

### `docker-compose.yml`

Levanta toda la arquitectura local:

- PostgreSQL
- Namenode y datanode
- Spark master y worker
- Airflow init, webserver y scheduler

Esto es como un "mini Kubernetes" de aprendizaje, pero mas simple.

En Azure, la idea equivalente no es una sola tecnologia, sino IaC y servicios administrados:

- Bicep o Terraform para definir infraestructura
- Azure Data Factory para orquestacion
- Azure Databricks o Synapse para Spark
- Azure Database for PostgreSQL para la base relacional
- ADLS Gen2 para almacenamiento

### `.gitignore`

Evita subir archivos generados por ejecuciones locales:

- logs de Airflow
- `__pycache__`
- salidas de Spark
- variables de entorno

Es la version practica de decir: "no guardes basura ni archivos temporales en Git".

### `docs/`

Documentacion del proyecto.

- `docs/README.md`
  - Explica para que sirve cada tecnologia y su equivalente en Azure.
- `docs/historial_problemas.md`
  - Resume los errores que aparecieron, por que pasaron y como se resolvieron.

## Flujo del pipeline

### 1. Airflow arranca la orquestacion

El DAG `spark_sales_pipeline` define cuando y como se ejecuta el trabajo.

Analogía:

- Airflow es como el coordinador de una obra.
- No mezcla cemento ni pone ladrillos.
- Solo se asegura de que cada equipo haga su parte en el orden correcto.

### 2. Spark ejecuta la transformacion

El job `process_sales.py` hace el trabajo real de datos.

Ejemplo del caso:

- entrada: ventas con columnas como `producto`, `precio` y `cantidad`
- transformacion: `venta_total = precio * cantidad`
- salida: archivo procesado y tabla relacional

### 3. HDFS guarda el resultado procesado

En vez de depender de una carpeta local de Windows, el resultado se guarda en HDFS.

Eso es importante porque:

- HDFS esta pensado para datos grandes
- soporta mejor el enfoque distribuido
- se parece mucho a ADLS Gen2 en Azure desde la perspectiva de almacenamiento de datos

### 4. PostgreSQL recibe una copia estructurada

La misma informacion tambien se carga a PostgreSQL.

Esto te ayuda a entender un patron comun:

- almacenamiento barato y distribuido para historicos
- base relacional para consultas mas estructuradas o consumo downstream

## Equivalencias con Azure

### Airflow

Papel:
- orquestacion de pipelines

Par en Azure:
- Azure Data Factory
- Synapse Pipelines
- Managed Airflow, si quisieras mantener el mismo estilo de orquestacion

### Spark

Papel:
- procesamiento distribuido y transformaciones

Par en Azure:
- Azure Databricks
- Azure Synapse Spark

### HDFS

Papel:
- almacenamiento distribuido para datos y outputs

Par en Azure:
- Azure Data Lake Storage Gen2

### PostgreSQL

Papel:
- persistencia relacional

Par en Azure:
- Azure Database for PostgreSQL

### Docker

Papel:
- empaquetar servicios y reproducir el entorno local

Par en Azure:
- Azure Container Instances
- Azure Container Apps
- Azure Kubernetes Service, si escalas a algo mas serio

### Docker Compose

Papel:
- levantar varias piezas del sistema en una sola definicion

Par en Azure:
- Bicep
- Terraform
- ARM templates

## Caso real comparado con este proyecto

Imagina una empresa de ecommerce.

Situacion real:

- llegan ventas desde una tienda online
- Airflow dispara el proceso cada hora
- Spark limpia y calcula totales
- los resultados historicos se guardan en un lago de datos
- una tabla resumida se carga a una base relacional para reportes

Tu proyecto hace exactamente una version pequena de eso.

La diferencia es la escala:

- tu proyecto usa un CSV pequeno
- una empresa usarian millones de filas y multiples fuentes

## Lo que aprendiste con este laboratorio

Este proyecto te ensena varias lecciones clave:

1. No todo archivo local existe en todos los contenedores.
2. Las rutas deben ser explicitas.
3. El driver y los executors no siempre ven el mismo filesystem.
4. Los errores en ingenieria de datos suelen ser de infraestructura, no solo de codigo.
5. Separar responsabilidades hace que todo sea mas entendible.

## Como correrlo

1. Levanta Docker Compose.
2. Entra a Airflow.
3. Ejecuta el DAG `spark_sales_pipeline`.
4. Revisa:
   - HDFS en `http://localhost:9870`
   - PostgreSQL con tu cliente favorito

## Estructura mental recomendada

Cuando estudies este proyecto, piensa en capas:

- Capa 1: infraestructura
- Capa 2: orquestacion
- Capa 3: procesamiento
- Capa 4: almacenamiento
- Capa 5: consumo

Si entiendes eso, ya entendiste la base de muchas arquitecturas modernas de datos.
