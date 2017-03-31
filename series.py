from os import listdir, system, remove, rmdir
from os.path import isdir, join
import subprocess
import sys

#################################################################################################################
#	Autor: Ismael Ortega				Email: ismaelortegasanchez@hotmail.com			#
#														#
#		LEE EL README DE GITHUB ANTES DE USAR:	https://github.com/CHA0S14/SeriesManager.git		#
#################################################################################################################

#####################
#VARIABLES GLOBALES #
#####################

#Ruta a la carpeta con las series
seriesPath = r"<path a series>"
#ruta al programa con el que quieres reproducir
reproductor = r"<path a reproductor>"
#Recorro la carpeta de series y creo un array con las carpetas de dentro simbolizando cada una una serie distinta
series = [
        fichero for fichero in listdir(seriesPath)
        if isdir(join(seriesPath, fichero))]

#Mensajes series
SERIE_INI = "Series disponibles:"
SERIE_FIN = "Que serie quieres ver? n de serie:"
SERIE_ADD = ["Abrir carpeta"]

#Mensajes caps
CAP_INI = "Capitulos disponibles"
CAP_FIN = "Que capitulo quieres ver? n de cap:"

#####################
#   FUNCIONES       #
#####################

#Imprimo y pregunto por que serie quieres ver. ademas se puede pasar directamente por comandos como un argumento si gustas
def impArray(mensajeIni, mensajeFin, array, opcionAd = []):
    print(mensajeIni)

    cont = 0
    for opcion in opcionAd:
        print "\t" + str(cont) + ". " + opcion
        cont = cont +1

    cont = 1 if cont == 0 else cont
    for elem in array:
        print "\t" + str(cont) + ". " + elem
        cont = cont + 1

    print(mensajeFin)

    return int(input()) - 1

def comprobarAperturaCarpeta(serie):
    #Si quieres abrir la carpeta para aniadir una serie o algo la opcion 0 activa esto
    if serie == -1:
	system('start ' + seriesPath)
	exit()


#####################
#       INICIO      #
#####################

if len(sys.argv) < 2:
    serie = impArray(SERIE_INI, SERIE_FIN, series, SERIE_ADD)
else:
    serie = int(sys.argv[1]) - 1

comprobarAperturaCarpeta(serie)

#consigo que seriePath apunte a la carpeta de la serie a ver
seriePath = join(seriesPath,series[serie])

#while que se encarga de preguntar que quieres hacer al acabar de ver el capitulo
continua = True
cap = 0

#array que va guardando los capitulos que has decidido borrar al final de la ejecucion
delSchedule = []

#caps tiene todos los capitulos de una serie, esta fuera del while para reducir llamadas al sistema
#y se actualizara solo cuando se llame a cambiar serie
caps = listdir(seriePath)
while continua:
    capitulo = join(seriePath,caps[cap])
    subprocess.call([reproductor,capitulo])
    
    #comprobacion de si se quiere eliminar el archivo una vez visto
    print("Quieres eliminar el archivo? (se eliminaran al final)[S/s]")
    delete = str(raw_input()) 
    if delete == "S" or delete == "s":
        #se aniade el archivo al array para borrarlo despues
        delSchedule.append(capitulo)

    #segunda tanda de opciones ha realizar
    print("""Que quieres hacer?
	1. Siguiente cap
	2. Anterior cap
	3. Elegir cap
	4. Cambiar serie
	5. Salir
Opcion: """)

    accion = int(input())
    if accion == 1:
        cap += 1
    elif accion == 2:
        cap -= 1
    elif accion == 3:
        cap = impArray(CAP_INI, CAP_FIN, caps)        
    elif accion == 4:
        serie = impArray(SERIE_INI, SERIE_FIN, series, SERIE_ADD)
        comprobarAperturaCarpeta(serie)
        #consigo que seriePath apunte a la carpeta de la serie a ver
        seriePath = join(seriesPath,series[serie])
        caps = listdir(seriePath)
    elif accion == 5:
        continua = False

#for que se encarga de borrar los archivos que indica el array delSchedule
if len(delSchedule) > 0:
    print("eliminando archivos")
    for archivo in delSchedule:
        print(archivo)
        remove(archivo)
    if len(listdir(seriesPath)) == 0:
	rmdir(seriesPath)
print("BYE")
