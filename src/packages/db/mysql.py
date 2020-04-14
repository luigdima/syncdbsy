import os
import pymysql
from packages.utils.log import moduloLog as log
import sys

class MySQL:
    def checkType(self, type):
        types = {
            'int': 'int',
            'nchar': 'varchar',
            'nvarchar': 'varchar',
            'float': 'float',
            'smallint': 'smallint',
            'datetime': 'datetime'
        }

        if type in types:
            log(__name__).info('Cambiado type de MsSQL a MySQL (' + type + ')')
            return types[type]
        else:
            log(__name__).critical('No se ha podido cambiar el type de MsSQL a MySQL (' + type + ')')
            sys.exit(1)

    def conn(self):
        try:
            connection = pymysql.connect(
                os.getenv("DB_MYSQL_SERVER"),
                os.getenv("DB_MYSQL_USER"),
                os.getenv("DB_MYSQL_PASSWORD"),
                os.getenv("DB_MYSQL_DB")
            )
            log(__name__).info('Conectado a base de datos MySQL ' +
                               os.getenv("DB_MYSQL_SERVER"))
            return connection.cursor()
        except:
            log(__name__).critical('Error al conectar con MySQL! ' +
                               os.getenv("DB_MYSQL_SERVER"))
            sys.exit(1)

    def numRows(self, tabla):
        return 1

    def drop(self,tabla):
        try:
            log(__name__).info('Borrando la tabla ' + tabla)

            sql = "DROP TABLE " + tabla
            conn = self.conn()
            conn.execute(sql)
            conn.close()
        except:
            log(__name__).warning('Error al borrar la tabla ' + tabla)

    def createTable(self,tabla, atributos, describe):
        try:
            log(__name__).info('Creando tabla ' + tabla)

            atributos = ''
            for atributo in describe:
                if len(atributo['type'].split('(')) > 1:
                    longitud = atributo['type'].split('(')[1].split(')')[0]
                else:
                    longitud = atributo['max_lenght']

                if atributo['type'].split('(')[0] == "datetime":
                    longitud = 6

                if atributo['is_nullable']:
                    nulo = 'NULL'
                else:
                    nulo = 'NOT NULL'

                cadenaAtributo = atributo['name'].lower() + ' ' +  \
                    self.checkType(atributo['type'].split('(')[0]) + \
                    '(' + str(longitud) + ') ' + \
                    nulo + ','

                atributos = atributos + cadenaAtributo

            sql = 'CREATE TABLE ' + tabla + ' (' + atributos[:-1] + ') COLLATE utf8_spanish2_ci'
            conn = self.conn()
            conn.execute(sql)
            conn.close()
        except:
            log(__name__).critical('Error al crear la tabla ' + tabla)
            sys.exit(1)

    def insert(self, tabla, atributos, registros, describe):
        try:
            log(__name__).info('Insertando elementos en la tabla ' + tabla)

            self.drop(tabla)
            self.createTable(tabla, atributos, describe)

            stringAtributos = ','.join(atributos)
            valString = '%s, '*len(registros[0])

            sql = "INSERT INTO " + tabla + \
                ' (' + stringAtributos.lower() + ') VALUES ('+valString[:-2]+') '

            conn = self.conn()
            conn.executemany(sql, registros)
        except pymysql.Error as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))

            log(__name__).critical('Error al insertar elementos en la tabla ' + tabla)

            return False
        finally:
            conn.close()
            sys.exit(1)
