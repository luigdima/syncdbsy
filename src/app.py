import logging
import sys
import re
import schedule
import time
import os
from os import walk
from os.path import join
from os import PathLike
from packages.db.mssql import MsSQL
from packages.db.mysql import MySQL
from packages.utils.log import moduloLog as log

def main():
    basePath = os.getenv("DIRSQL")
    try:
        initFile = open(basePath + "/init", "r")
    except:
        log(__name__).info('Creando fichero init!')
        initFile = open(basePath + "/init", "w")
        importador()
    finally:
        initFile.close()

def cargarCSQL():
    log(__name__).info('Cargando archivos SQL...')

    basePath = os.getenv("DIRSQL")
    consultas = {}

    for (dirPath, dirNames, fileNames) in walk(basePath):
        for file in fileNames:
            if os.path.splitext(file)[1] != ".sql":
                continue
            
            contentFileStrip = ""
            contentFile = open(basePath +"/"+ file, "r").readlines()

            for contentFileLine in contentFile:        
                contentFileStrip = contentFileStrip +" "+ contentFileLine.strip(' ').rstrip("\n")

            atributosConsulta = re.search('SELECT(.*)FROM', contentFileStrip).group(1).split(',')
            atributosConsultaLimpios = []
            for atributoConsulta in atributosConsulta:
                atributoConsulta = atributoConsulta.split(' AS ')
                if len(atributoConsulta) == 2:
                    atributosConsultaLimpios.append(atributoConsulta[1].strip())
                else:
                    atributosConsultaLimpios.append(atributoConsulta[0].strip())

            consultas[file.split(".")[0]] = {
                "sql_mssql": contentFileStrip,
                "atributos": atributosConsultaLimpios
            }
        break
    return consultas

def importador():
    log(__name__).info('Inicializando proceso de replicado...')

    callMsSQL = MsSQL()
    callMySQL = MySQL()

    consultas = cargarCSQL()

    for consulta in consultas.items():
        consultaMsSQL = callMsSQL.select(consulta[1]['sql_mssql'])
        describeMsSQL = callMsSQL.describes(consulta[1]['sql_mssql'])

        if len(consultaMsSQL) > 0:
            callMySQL.insert(
                consulta[0],
                consulta[1]['atributos'],
                consultaMsSQL,
                describeMsSQL
            )

if __name__ == '__main__':
    main()
    schedule.every().minutes.do(main)
    schedule.every().day.at(os.getenv("TIMECRON")).do(importador)

while True:
    schedule.run_pending()
    time.sleep(1)
