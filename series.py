from os import listdir, system, remove, rmdir
from os.path import isdir, join
import subprocess
import sys

#################################################################################################################
#	Autor: Ismael Ortega				Email: ismaelortegasanchez@hotmail.com			#
#														#
#		LEE EL README DE GITHUB ANTES DE USAR:	https://github.com/CHA0S14/SeriesManager.git		#
#################################################################################################################

#Ruta a la carpeta con las series
seriesPath = r"C:\Users\ismae\ownCloud\Series"
#ruta al programa con el que quieres reproducir
reproductor = r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"

#Recorro la carpeta de series y creo un array con las carpetas de dentro simbolizando cada una una serie distinta
carpetas = [
        fichero for fichero in listdir(seriesPath)
        if isdir(join(seriesPath, fichero))]

#Imprimo y pregunto por que serie quieres ver. ademas se puede pasar directamente por comandos como un argumento si gustas
def impSerie():
    print("Series disponibles:")
    print("\t0. Abrir carpeta")
    
    cont = 1
    for carpeta in carpetas:
        print "\t" + str(cont) + ". " + carpeta
        cont = cont + 1

    print("Que serie quieres ver? n de serie:")

    return int(input()) - 1


def comprobarAperturaCarpeta(serie):
    #Si quieres abrir la carpeta para aniadir una serie o algo la opcion 0 activa esto
    if serie == -1:
	system('start ' + seriesPath)
	exit()

if len(sys.argv) < 2:
    serie = impSerie()
else:
    serie = int(sys.argv[1]) - 1

comprobarAperturaCarpeta(serie)

#consigo que seriesPath apunte a la carpeta de la serie a ver
seriePath = join(seriesPath,carpetas[serie])

#while que se encarga de preguntar que quieres hacer al acabar de ver el capitulo
continua = True
cap = 0

#array que va guardando los capitulos que has decidido borrar al final de la ejecucion
delSchedule = []
while continua:
    capitulo = join(seriePath,listdir(seriePath)[cap])
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
	3. Cambiar serie
	4. Salir
Opcion: """)

    accion = int(input())
    if accion == 1:
        cap += 1
    elif accion == 2:
        cap -= 1
    elif accion == 3:
        serie = impSerie()
        comprobarAperturaCarpeta(serie)
        #consigo que seriesPath apunte a la carpeta de la serie a ver
        seriePath = join(seriesPath,carpetas[serie])
    elif accion == 4:
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
   
