from os import listdir, system, remove, rmdir, chdir
from os.path import isdir, join
import subprocess, sys, thread, time, msvcrt

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

#####################
#     Constantes    #
#####################

#Tiempo de espera al siguiente cap
TIEMPO_ESPERA = 5

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

#Acciones tras reproduccion
ACC_INI = 'Que quieres hacer?:'    
ACC_FIN = 'Opcion:'

#Posibilidades de eliminar
DEL_INI = 'Que quieres eliminar?:'
DEL_ARRAY = ['Eliminar todos los capitulos vistos',
             'Eliminar todo menos el ultimo',
             'Elegir cuales eliminar',
             'No eliminar ninguno']
DEL_FIN = 'Opcion:'

#Seleccion de caps a borrar
SELD_INI = 'Capitulos a borrar:'
SELD_FIN = 'Escribe el numero de los caps separados con coma'

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
    return input()

def comprobarAperturaCarpeta(serie):
    #Si quieres abrir la carpeta para aniadir una serie o algo la opcion 0 activa esto
    if serie == -1:
	system('start ' + seriesPath)
	exit()

#Este metodo se encarda de comprobar si hay temporadas y dar a elegir cual quieres ver
def comprobarTemporada(seriePath):
    elementos = listdir(seriePath)
    auxPath = seriePath;
    if isdir(join(seriePath,elementos[0])):
        temp = int(impArray(TEMP_INI,TEMP_FIN,elementos)) - 1
        seriePath = join(seriePath,elementos[temp])
        elementos = listdir(seriePath)
    else:
        auxPath = None
    return (seriePath,elementos,auxPath)

def eliminarCaps(delSchedule,seriePath, auxPath):
    #for que se encarga de borrar los archivos que indica el array delSchedule
    if len(delSchedule) > 0:
        print "Se van a eliminar los archivos planificados"
        for archivo in delSchedule:
            print "eliminadno " + archivo + "..."
            time.sleep(0.5)
            remove(archivo)
        if len(listdir(seriePath)) == 0:
            print "No quedan capitulos eliminando carpeta..."
            time.sleep(1)
            rmdir(seriePath)
            if auxPath is not None and len(listdir(auxPath)) == 0:
                print "No quedan temporadas eliminando carpeta..."
                time.sleep(1)
                rmdir(auxPath)

#hilo para leer si se quiere cortar la reproduccion automatica
def input_thread(L):
    raw_input()
    L.append(None)

#Contador que si no se detiene devuelve None si se detiene devuelve otra cosa
def counter(tiempo, mensaje):
    inp = None
    for i in range(tiempo,0,-1):
        if msvcrt.kbhit():
            inp = msvcrt.getch()
            break
        print mensaje + ' %d sec, presiona algo para parar: \r' % i,
        sys.stdout.flush()
        time.sleep(1)
    if not inp:
        print mensaje + ' 0 sec:                             '
    else:
        #con estre print evito superposiciones de texto
        print ''
    return inp


#####################
#       INICIO      #
#####################

def main():

    #####################
    #     Variables     #
    #####################

    #Recorro la carpeta de series y creo un array con las carpetas de dentro simbolizando cada una una serie distinta
    series = [fichero for fichero in listdir(seriesPath)
            if isdir(join(seriesPath, fichero))]

    #####################
    #     INICIO COD    #
    #####################

    if len(sys.argv) < 2:
        serie = int(impArray(SERIE_INI, SERIE_FIN, series, SERIE_ADD)) - 1
    else:
        serie = int(sys.argv[1]) - 1

    apagar = serie<-1;
    if apagar:
        serie = abs(serie + 2)

    comprobarAperturaCarpeta(serie)

    #hago que seriePath apunte a la carpeta de la serie a ver y si hay temporadas elegir cual
    #caps tiene todos los capitulos de una serie, esta fuera del while para reducir llamadas al sistema
    #y se actualizara solo cuando se llame a cambiar serie
    (seriePath, caps, auxPath) = comprobarTemporada(join(seriesPath,series[serie]))

    #while que se encarga de preguntar que quieres hacer al acabar de ver el capitulo
    continua = True
    cap = 0

    #array que guarda los capitulos vistos en reproduccion automatica
    vistos = []

    #array que va guardando los capitulos que has decidido borrar al final de la ejecucion
    delSchedule = []

    #booleana por si se quiere apagar el ordena


    while continua:
        capitulo = join(seriePath,caps[cap])
        print "Reproduciendo " + caps[cap] + "..."
        subprocess.call([reproductor,'--fullscreen',capitulo])

        if apagar:
            if not counter(10, 'El ordenador se apagara en'):
                eliminarCaps(delSchedule,seriePath, auxPath)
                subprocess.call("shutdown -s -t 0")
            else:
                apagar = False
        
        vistos.append(capitulo)

        #inicio del contador para reproduccion automatica
        if cap+1<len(caps) and not counter(TIEMPO_ESPERA, 'Finalizado el siguiente capitulo empezara en'):
            cap += 1
            continue
        elif cap+1==len(caps):
            print 'No quedan mas capitulos'
        
        #comprobacion de si se quieren eliminar los archivos una vez vistos
        if len(vistos) == 1:
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
        else:
            eliminar = int(impArray(DEL_INI,DEL_FIN,DEL_ARRAY))
            
            #eliminar todos menos el ultimo
            if eliminar == 2:
                print 'eliminacion planificada'
                vistos = vistos[0:-1]
            #elegir los que eliminar
            elif eliminar == 3:
                print 'eliminacion planificada'
                elementos = impArray(SELD_INI,SELD_FIN,vistos[1:],[vistos[0]])
                if type(elementos) is tuple:
                    vistosAux = vistos
                    vistos = []
                    for element in elementos:
                        vistos.append(vistosAux[element])
                else:
                    vistos = [vistos[elementos]]
            #no se elimina nada o se eliminan todos
            elif eliminar != 1:
                print 'no se eliminra nada'
                vistos = []

            delSchedule = list(set(delSchedule)|set(vistos))  

        vistos = []  
        

        #segunda tanda de opciones ha realizar
        acciones = ["Siguiente cap -> " + (caps[cap+1] if cap < len(caps) - 1 else caps[cap]),
                    "Anterior cap  -> " + (caps[cap-1] if cap > 0 else caps[cap]),
                    "Elegir cap",
                    "Cambiar serie",
                    "Ultimo y apaga",
                    "Salir"]
        

        accion = int(impArray(ACC_INI,ACC_FIN,acciones))
        #siguiente capitulo
        if accion == 1:
            if cap < len(caps)-1:
                cap += 1
        #anterior capitulo
        elif accion == 2:
            if cap > 0:
                cap -= 1
        #elegir capitulo
        elif accion == 3:
            cap = int(impArray(CAP_INI, CAP_FIN, caps)) - 1
        #Cambiar de serie
        elif accion == 4:
            #se eliminaran los capitulos planificados
            eliminarCaps(delSchedule,seriePath,auxPath)
            delSchedule = []
            #se actualiza las series disponibles
            series = [fichero for fichero in listdir(seriesPath)
                        if isdir(join(seriesPath, fichero))]
            cap = 0
            serie = int(impArray(SERIE_INI, SERIE_FIN, series, SERIE_ADD)) - 1
            comprobarAperturaCarpeta(serie)
            #consigo que seriePath apunte a la carpeta de la serie a ver y si hay temporadas elegir cual
            #caps tiene todos los capitulos de una serie, esta fuera del while para reducir llamadas al sistema
            #y se actualizara solo cuando se llame a cambiar serie
            (seriePath, caps, auxPath) = comprobarTemporada(join(seriesPath,series[serie]))
        #Ultimo capitulo y apagar el ordenador
        elif accion == 5:
            print "Se apagara el ordenador despues de reproducir el capitulo, si se desea anular tendra 5 segundos tras finalizar el capitulo, antes de apagar se borraran todos los capitulos planificados y se mantendra el ultimo"
            time.sleep(2)
            cap += 1
            apagar = True
        #Salir del programa
        elif accion == 6:
            continua = False

    #Se eliminaran los capitulos planificados
    eliminarCaps(delSchedule,seriePath,auxPath)
    print("BYE")
    time.sleep(1)
    

if __name__ == '__main__':
    main()
