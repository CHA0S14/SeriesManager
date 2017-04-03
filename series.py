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

#Mensajes temporadas
TEMP_INI = "Temporadas disponibles:"
TEMP_FIN = "Que temporada quieres ver? n de temp:"

#Mensajes caps
CAP_INI = "Capitulos disponibles"
CAP_FIN = "Que capitulo quieres ver? n de cap:"

#####################
#   FUNCIONES       #
#####################

#Recorre un array con las opciones para que el usuario tome una decision
def impArray(mensajeIni, mensajeFin, array, opcionAd = []):
    print(mensajeIni)

    #recorre las opciones adicionales que van a parte del array de series o capitulos
    cont = 0
    for opcion in opcionAd:
        print "\t" + str(cont) + ". " + opcion
        cont = cont +1

    #recorre el array con las series o capitulos
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

#Este metodo se encarda de comprobar si hay temporadas y dar a elegir cual quieres ver
def comprobarTemporada(seriePath):
    elementos = listdir(seriePath)
    if isdir(join(seriePath,elementos[0])):
        temp = impArray(TEMP_INI,TEMP_FIN,elementos)
        seriePath = join(seriePath,elementos[temp])
        elementos = listdir(seriePath)    
    return (seriePath,elementos)

def eliminarCaps(delSchedule,serePath):
    #for que se encarga de borrar los archivos que indica el array delSchedule
    print "Se van a eliminar los archivos planificados"
    if len(delSchedule) > 0:
        for archivo in delSchedule:
            print "eliminadno " + archivo + "..."
            sleep(0.5)
            remove(archivo)
        if len(listdir(seriePath)) == 0:
            print "No quedan capitulos eliminando carpeta..."
            sleep(1)
            rmdir(seriePath)


#####################
#       INICIO      #
#####################

if len(sys.argv) < 2:
    serie = impArray(SERIE_INI, SERIE_FIN, series, SERIE_ADD)
else:
    serie = int(sys.argv[1]) - 1

comprobarAperturaCarpeta(serie)

#consigo que seriePath apunte a la carpeta de la serie a ver y si hay temporadas elegir cual
#caps tiene todos los capitulos de una serie, esta fuera del while para reducir llamadas al sistema
#y se actualizara solo cuando se llame a cambiar serie
(seriePath, caps) = comprobarTemporada(join(seriesPath,series[serie]))

#while que se encarga de preguntar que quieres hacer al acabar de ver el capitulo
continua = True
cap = 0

#array que va guardando los capitulos que has decidido borrar al final de la ejecucion
delSchedule = []

while continua:
    capitulo = join(seriePath,caps[cap])
    print "Reproduciendo " + caps[cap] + "..."
    subprocess.call([reproductor,capitulo])
    
    #comprobacion de si se quiere eliminar el archivo una vez visto
    if capitulo not in delSchedule:
        print("Quieres eliminar el archivo? (se eliminaran al final)[S/s]")
        delete = str(raw_input()) 
        if delete == "S" or delete == "s":
            #se aniade el archivo al array para borrarlo despues
            delSchedule.append(capitulo)
    else:
        print("Quieres evitar la eliminacion del archivo?[S/s]")
        delete = str(raw_input()) 
        if delete == "S" or delete == "s":
            #se quita el archivo al array para no borrarlo despues
            delSchedule.remove(capitulo)

    #segunda tanda de opciones ha realizar
    print "Que quieres hacer?:"
    print "\t1. Siguiente cap -> " + (caps[cap+1] if cap < len(caps) - 1 else caps[cap])
    print "\t2. Anterior cap  -> " + (caps[cap-1] if cap > 0 else caps[cap])
    print """\t3. Elegir cap
	4. Cambiar serie
	5. Salir
Opcion: """

    accion = int(input())
    if accion == 1:
        #si esta apuntado al primer elemento con un indice negativo o el array solo tiene un elemento y el indice es -1 haciendo que 0 y -1
        #apuntan al mismo sitio no quedaran capitulos y se reproducira el ultimo
        if cap + 1 == len(caps) or (cap == 0 and len(caps) == 1):
            print("no hay mas capitulos se reproducira el ultimo")
        else:
            cap += 1
    elif accion == 2:
        #si esta apuntado al primer elemento con un indice negativo o el array solo tiene un elemento y el indice es 0 haciendo que 0 y -1
        #apuntan al mismo sitio no quedaran capitulos y se reproducira el primero
        if cap - 1 < len(caps) * -1 or (len(caps) == 1 and cap == 0):
            print ("no hay mas capitulos se reproducira el primero")
        else:
            cap -= 1
    elif accion == 3:
        cap = impArray(CAP_INI, CAP_FIN, caps)        
    elif accion == 4:
        #se eliminaran los capitulos planificados
        eliminarCaps(delSchedule,seriePath)
        delSchedule = []
        #se actualiza las series disponibles
        series = [fichero for fichero in listdir(seriesPath)
                    if isdir(join(seriesPath, fichero))]
        cap = 0
        serie = impArray(SERIE_INI, SERIE_FIN, series, SERIE_ADD)
        comprobarAperturaCarpeta(serie)
        #consigo que seriePath apunte a la carpeta de la serie a ver y si hay temporadas elegir cual
        #caps tiene todos los capitulos de una serie, esta fuera del while para reducir llamadas al sistema
        #y se actualizara solo cuando se llame a cambiar serie
        (seriePath, caps) = comprobarTemporada(join(seriesPath,series[serie]))
    elif accion == 5:
        continua = False

#Se eliminaran los capitulos planificados
eliminarCaps(delSchedule,seriePath)
print("BYE")
sleep(1)
