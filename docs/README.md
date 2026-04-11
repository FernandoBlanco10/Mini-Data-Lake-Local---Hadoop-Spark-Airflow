# Guia de estudio del proyecto

Este documento explica para que sirve cada tecnologia del proyecto, como se relaciona con el resto de la arquitectura y cual seria su equivalente mas cercano en Azure.

La idea es leerlo como si estuvieras dibujando una arquitectura en un pizarron.

## 1. Docker

### Para que se usa aqui

Docker empaqueta cada servicio en un contenedor reproducible.

En este proyecto hay varios contenedores:

- Airflow
- Spark master
- Spark worker
- PostgreSQL
- HDFS namenode
- HDFS datanode

### Analogía

Docker es como rentar departamentos separados en el mismo edificio.

Cada servicio vive en su propio departamento, pero todos comparten el mismo edificio y se pueden comunicar por pasillos internos.

### Por que importa

Sin Docker, tendrias que instalar y configurar todo a mano en tu maquina.

Con Docker:

- repites el entorno facilmente
- evitas conflictos entre versiones
- puedes destruir y recrear todo cuando quieras

### Par en Azure

No hay un reemplazo unico.

Dependiendo del caso, se parece a:

- Azure Container Apps
- Azure Container Instances
- AKS si tu arquitectura crece

### En tu proyecto

`docker-compose.yml` define todo el ecosistema local.

---

## 2. Docker Compose

### Para que se usa aqui

Docker Compose levanta varios contenedores con una sola definicion.

### Analogía

Es como un plano de edificios:

- aqui va la cocina
- aqui la oficina
- aqui el almacén
- aqui la sala de control

### Por que importa

Te permite escribir una arquitectura completa en un solo archivo.

### Par en Azure

Se parece mas a:

- Bicep
- Terraform
- ARM templates

porque todos declaran infraestructura de forma repetible.

### En tu proyecto

Tu `docker-compose.yml` es la "maqueta" completa del laboratorio.

---

## 3. Airflow

### Para que se usa aqui

Airflow orquesta tareas.

No procesa datos por si mismo.

Su trabajo es decidir:

- que se ejecuta
- cuando se ejecuta
- en que orden
- que hacer si algo falla

### Analogía

Airflow es el director de cine.

No actua, no filma, no edita.

Solo dice:

- "ahora entra Spark"
- "despues guarda el resultado"
- "si falla algo, marca error"

### Por que importa

En ingenieria de datos, muchas veces el reto no es solo transformar datos, sino coordinar muchas tareas con dependencias.

### Par en Azure

Lo mas cercano es:

- Azure Data Factory
- Synapse Pipelines

Si quisieras mantener un enfoque similar al tuyo, tambien existe el concepto de Airflow administrado.

### En tu proyecto

El DAG `spark_sales_pipeline` lanza el job de Spark.

---

## 4. Spark

### Para que se usa aqui

Spark procesa datos de forma distribuida.

En este proyecto:

- lee el CSV
- calcula `venta_total`
- escribe resultados
- carga en PostgreSQL

### Analogía

Spark es una brigada de cocina:

- una persona lee la receta
- varias personas procesan en paralelo
- al final, el plato sale listo

### Por que importa

Spark es muy usado cuando:

- el volumen de datos crece
- el procesamiento ya no cabe bien en una sola maquina
- quieres trabajar con batch o pipelines de datos

### Par en Azure

Los equivalentes mas comunes son:

- Azure Databricks
- Azure Synapse Spark

### En tu proyecto

El archivo `spark/jobs/process_sales.py` contiene la logica del negocio.

---

## 5. HDFS

### Para que se usa aqui

HDFS guarda datos de forma distribuida.

En tu proyecto, lo usamos como destino del archivo procesado.

### Analogía

HDFS es como un archivador gigante con varios cajones repartidos entre varias personas.

No depende de un solo disco.

### Por que importa

Es la idea clasica de almacenamiento distribuido para datos grandes.

### Par en Azure

Azure Data Lake Storage Gen2.

### En tu proyecto

El output del job Spark termina en:

```text
hdfs://namenode:9000/tmp/sales_processed/<ejecucion>
```

---

## 6. PostgreSQL

### Para que se usa aqui

PostgreSQL guarda una copia estructurada del resultado.

### Analogía

Si HDFS es el almacén grande, PostgreSQL es la bodega organizada con estantes y etiquetas claras.

### Por que importa

Muchas arquitecturas tienen dos destinos:

- uno para almacenamiento masivo
- otro para consulta estructurada

### Par en Azure

Azure Database for PostgreSQL.

### En tu proyecto

El job escribe en la tabla `sales_processed`.

---

## 7. Airflow DAG

### Para que se usa aqui

Un DAG define un flujo de trabajo.

En tu caso:

- iniciar el job
- ejecutar Spark
- guardar datos

### Analogía

Un DAG es como un mapa de estaciones de tren.

Cada estacion depende de la anterior.

### En tu proyecto

El DAG `spark_sales_pipeline` es el punto de entrada.

---

## 8. Carpetas del proyecto

### `airflow/`

Contiene orquestacion y configuracion de Airflow.

### `spark/`

Contiene el job de Spark y los datos de ejemplo.

### `docs/`

Contiene material de estudio.

### `.gitignore`

Evita subir basura generada por ejecuciones locales.

---

## 9. Mapa rapido: tecnologia -> Azure

- Docker -> Container Apps / ACI / AKS
- Docker Compose -> Bicep / Terraform / ARM
- Airflow -> Azure Data Factory / Synapse Pipelines
- Spark -> Databricks / Synapse Spark
- HDFS -> ADLS Gen2
- PostgreSQL -> Azure Database for PostgreSQL

---

## 10. Ejemplo aterrizado en tu proyecto

Supongamos que entra un archivo `sales.csv`.

1. Airflow detecta que toca correr el pipeline.
2. Spark lee el archivo.
3. Calcula una columna nueva.
4. Guarda resultados en HDFS.
5. Carga los datos en PostgreSQL.
6. Tu analista podria consumir la tabla en una herramienta SQL o leer el output procesado.

Esto es una version pequena del tipo de flujo que ves en empresas reales.
