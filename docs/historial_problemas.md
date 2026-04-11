# Historial de problemas y aprendizajes

Este documento resume los errores que aparecieron durante la construccion del proyecto, por que ocurrieron y como se corrigieron.

La idea no es solo recordar "que comando fallaba", sino entender el motivo tecnico.

---

## 1. `cmd /c` no funcionaba dentro de Airflow

### Sintoma

El task fallaba con algo como:

```text
/usr/bin/bash: line 1: cmd: command not found
```

### Causa real

Airflow corre dentro de contenedores Linux.

`cmd /c` pertenece a Windows.

### Aprendizaje

No puedes asumir que un contenedor Linux entiende comandos de Windows.

### Solucion

Reemplazar el comando por un script Bash nativo o usar un operador mas apropiado para el entorno Linux.

---

## 2. Airflow intento interpretar el `.sh` como template

### Sintoma

Error tipo:

```text
jinja2.exceptions.TemplateNotFound
```

### Causa real

`BashOperator` trata ciertos comandos como templates de Jinja.

### Aprendizaje

En Airflow, un comando no siempre es solo un comando: a veces es una plantilla.

### Solucion

Usar `template_searchpath` y pasar el script por nombre, no como texto mezclado con `bash`.

---

## 3. Error de cliente Docker viejo

### Sintoma

```text
client version 1.43 is too old. Minimum supported API version is 1.44
```

### Causa real

El contenedor de Airflow intentaba hablar con el daemon de Docker usando una version de API vieja.

### Aprendizaje

Usar `docker exec` desde un contenedor agrega una dependencia extra: no solo necesitas Docker, tambien necesitas compatibilidad de API.

### Solucion

Abandonar el enfoque basado en `docker exec` y pasar a una arquitectura mas limpia con `SparkSubmitOperator`.

---

## 4. `Broken DAG`

### Sintoma

Airflow no podia ni cargar el DAG.

### Causa real

Se paso un argumento invalido al operador de Spark.

### Aprendizaje

Si el DAG no compila, el problema esta antes de la ejecucion real del job.

### Solucion

Corregir los argumentos del operador y validar el archivo con `py_compile`.

---

## 5. `Could not parse Master URL`

### Sintoma

```text
Could not parse Master URL: 'spark-master:7077'
```

### Causa real

La URL de Spark carecia del esquema correcto.

Spark espera:

```text
spark://spark-master:7077
```

### Aprendizaje

Las URL de servicios distribuidos tienen formato estricto.

### Solucion

Definir la conexion y el master correctamente, con el esquema apropiado.

---

## 6. `Path does not exist: file:/opt/spark/data/sales.csv`

### Sintoma

Spark no encontraba el CSV.

### Causa real

El driver de Spark corria en el contenedor de Airflow y no veia el volumen local esperado.

### Aprendizaje

En modo `client`, el driver lee desde el filesystem del contenedor donde lanza el submit.

### Solucion

Montar el volumen correctamente o usar rutas con esquema explicito.

---

## 7. Problemas de permisos al escribir en el output local

### Sintoma

Errores como:

```text
Permission denied
Unable to clear output directory
Mkdirs failed to create ...
```

### Causa real

Spark estaba escribiendo sobre un bind mount de Windows.

Los archivos temporales, renames y metadatos de Spark no siempre se comportan bien sobre ese tipo de volumen.

### Aprendizaje

El sistema de archivos importa tanto como el codigo.

### Solucion

Mover la salida a HDFS y evitar depender de carpetas locales de Windows para outputs distribuidos.

---

## 8. Rutas locales interpretadas como HDFS

### Sintoma

```text
Path does not exist: hdfs://namenode:9000/opt/spark/data/sales.csv
```

### Causa real

Al configurar `fs.defaultFS` a HDFS, una ruta como `/opt/spark/data/sales.csv` paso a interpretarse como ruta de HDFS.

### Aprendizaje

Una ruta sin esquema puede cambiar de significado segun el filesystem por defecto.

### Solucion

Usar:

- `file:///opt/spark/data/sales.csv` para input local
- `hdfs://namenode:9000/...` para output en HDFS

---

## 9. El output seguia fallando aun con timestamp

### Sintoma

Aunque cada corrida escribia en una carpeta nueva, Spark seguia fallando.

### Causa real

El problema no era solo la carpeta repetida.

El problema base era el filesystem usado para escribir.

### Aprendizaje

Cambiar el nombre de la carpeta ayuda, pero no siempre arregla el problema de fondo.

### Solucion

Mover el output a HDFS y hacer las rutas explicitas.

---

## 10. El proyecto como leccion general

### Lo mas importante que aprendiste

1. Las rutas no son triviales.
2. Los contenedores no comparten todo por defecto.
3. Spark depende mucho del filesystem y del modo de ejecucion.
4. Airflow orquesta, pero no corrige automaticamente tus supuestos.
5. La mayor parte de los problemas de ingenieria de datos son de integracion.

### Idea clave

Un pipeline de datos no falla solo por "codigo malo".

Falla por:

- permisos
- rutas
- montajes
- formato de conexiones
- compatibilidad entre servicios

Y justamente eso es lo que este proyecto te permitio ver.
