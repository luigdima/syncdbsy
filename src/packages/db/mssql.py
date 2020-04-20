import logging
import os
import pymssql
from packages.utils.log import moduloLog as log
import sys

class MsSQL:
    def conn(self, sql):
        try:
            connection = pymssql.connect(
                os.getenv("DB_MSSQL_SERVER"),
                os.getenv("DB_MSSQL_USER"),
                os.getenv("DB_MSSQL_PASSWORD"),
                os.getenv("DB_MSSQL_DB")
            )

            log(__name__).info('Conectado a base de datos MsSQL ' +
                               os.getenv("DB_MSSQL_SERVER"))
        except:
            log(__name__).critical('Error al conectar con MsSQL! ' + os.getenv("DB_MSSQL_SERVER"))
            sys.exit(1)

        try:
            cursor = connection.cursor()
            cursor.execute(sql)
            r = cursor.fetchall()
            connection.close()
            return r
        except:
            log(__name__).critical('Error en consulta SQL de MsSQL: '+sql)
            sys.exit(1)

    def select(self, sql):
        r = self.conn(sql)
        return r

    def describes(self, sql):
        spDescribe = "EXEC sp_describe_first_result_set N'"+sql+"'"
        describe = self.conn(spDescribe)
        describeObject = []

        for item in describe:
            describeObject.append({
                "name": item[2],
                "is_nullable": item[3],
                "type": item[5],
                "max_lenght": item[6]
            })
        return describeObject
