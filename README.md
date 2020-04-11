# __SYNCDBSY__ (Microsoft SQL server *__a__* MySQL)

SYNCDBSY es un microservicio desarrollado en __Python__ :snake:. Permite __traspasar__ el __resultado__ de una consulta SQL realizada en __MSSQL__ a una base de datos __MySQL__.

---
:warning: __ATENCIÓN__ \
Hay que tener en cuenta que cuando se realiza el traslado hacía la base de datos de MySQL las tablas de destino son __eliminadas__, para luego, ser nuevamente creada.

---

## :rocket: ARRANQUE E INICIO

### CLONE Y COPIA DE CONFIG

```
git clone http://..
cd syncdbsy
cp /build/{syncdb.env-sample,syncdb.env}
```
### VARIABLES DE ENTORNO
Las variables de entorno son bastantes descriptivas. Por lo tanto, no hace falta poner ejemplos.
- DB_MSSQL_SERVER =
- DB_MSSQL_USER =
- DB_MSSQL_PASSWORD =
- DB_MSSQL_DB =
- DB_MYSQL_SERVER =
- DB_MYSQL_USER =
- DB_MYSQL_PASSWORD =
- DB_MYSQL_DB =
- TIMECRON = (default: 00:30)
- DIRSQL = (default: csql)

Deberemos de completar correctamente los datos en el archivo ```/build/syncdb.env```.

## :wrench: ARCHIVOS SQL DE CONSULTAS
### TIPO DE ARCHIVOS Y FORMATO
El script podrá leer todos los archivos con extensión ```.sql``` que se encuentre dentro del directorio definido en ```DIRSQL``` por defecto ```/src/csql/```. 

```bash
├── src
│   ├── csql
│   │   ├── mitabla_destino.sql
```
Todo tipo de archivo con __extensión distinta__ a ```.sql``` __será omitido__.

El archivo ```mitabla_destino.sql``` contiene la consulta que se realizará a la base de datos de Microsoft (MSSQL). Un ejemplo de consulta es la siguiente:

```
SELECT
    ARTICULOS.CAS AS CAS,
    DESCRIPCION,
    SECCION,
    PESO
FROM
    ARTICULOS
    LEFT JOIN PRECIOS
ON
    ARTICULOS.CAS=PRECIOS.CAS
```

La tabla de __destino__ hacía ```MySQL``` será el __nombre del fichero__, en este caso ```mitabla_destino.sql```. Los __atributos__ de la tabla serán los indicados en el ```SELECT``` de la consulta, con la singularidad que si introducimos un ```AS``` en el atributo este, __será__ el __nombre__ del atributo __destino__.


### REINICIO MANUAL

Este servicio __sincronizará__ la tabla A con la tabla B cada día a una hora concreta. Esta hora se __fija__ mediante la variable de entorno ```TIMECRON```. Si queremos __lanzar nuevamente__ la __sincronización__ no deberemos de volver a lanzar el contenedor, basta con __eliminar__ el fichero ```init``` que se __encuentra__ en el __mismo directorio__ de las __consultas__ ```SQL```. Al __eliminar__ este __fichero__ al minuto se __volverá a iniciar__ el proceso de __sincronización__.

## :whale: BUILD CON DOCKER-COMPOSE
Para ejecutar el entorno es tan sencillo como ejecutarlo con docker-compose dentro del directorio del proyecto. 
```
docker-compose up --build --force
```
Para poder visualizar los logs del servicio es tan sencillo como realizar lo siguiente:
```
docker-compose logs
```