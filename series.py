from os import listdir, system, remove, rmdir
from os.path import isdir, join
import subprocess
import sys

#Ruta a la carpeta con las series
seriesPath = r"D:\Owncloud\Series"
#ruta al programa con el que quieres reproducir
vlc = r"D:\Programas\VLC\vlc.exe"

#Recorro la carpeta de series y creo un array con las carpetas de dentro simbolizando cada una una serie distinta
carpetas = [
        fichero for fichero in listdir(seriesPath)
        if isdir(join(seriesPath, fichero))]

#Imprimo y pregunto por que serie quieres ver. ademas se puede pasar directamente por comandos como un argumento si gustas
print("Series disponibles:")
print("\t0. Abrir carpeta")
if len(sys.argv) < 2:
    cont = 1
    for carpeta in carpetas:
        print "\t" + str(cont) + ". " + carpeta
        cont = cont + 1

    print("Que serie quieres ver? nº de serie:")
    serie = int(input()) - 1
else:
    serie = int(sys.argv[1]) - 1
	
#Si quieres abrir la carpeta para añadir una serie o algo la opcion 0 activa esto
if serie == -1:
	system('start ' + seriesPath)
	exit()

#consigo que seriesPath apunte a la carpeta de la serie a ver
seriesPath = join(seriesPath,carpetas[serie])

#while que se encarga de preguntar que quieres hacer al acabar de ver el capitulo
continua = True
cap = 0

#array que va guardando los capitulos que has decidido borrar al final de la ejecucion
delSchedule = []
while continua:
    capitulo = join(seriesPath,listdir(seriesPath)[cap])
    subprocess.call([vlc,capitulo])
    
    print("Quieres eliminar el archivo? (se eliminaran al final)[S/s]")
    delete = str(raw_input()) 
    if delete == "S" or delete == "s":
        delSchedule.append(capitulo)
    print("""Que quieres hacer?
	1. Siguiente cap
	2. Anterior cap
	3. Salir
Opcion: """)

    accion = int(input())
    if accion == 1:
        cap += 1
    elif accion == 2:
        cap -= 1
    elif accion == 3:
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
    
