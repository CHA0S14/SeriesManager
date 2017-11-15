from os import listdir, system, remove, rmdir
from os.path import isdir, join
import subprocess
import sys
import time
import msvcrt

#############################################################################################
#	        Autor: Ismael Ortega			Email: ismaelortegasanchez@hotmail.com		    #
#														                                    #
#	LEE EL README DE GITHUB ANTES DE USAR:	https://github.com/CHA0S14/SeriesManager.git    #
#############################################################################################

#####################
#VARIABLES GLOBALES #
#####################

# Ruta a la carpeta con las series
SERIES_PATH = r"D:\Owncloud\Series"
# ruta al programa con el que quieres reproducir
REPRODUCTOR = r"D:\Programas\VLC\vlc.exe"

#####################
#     Constantes    #
#####################

# Tiempo de espera al siguiente cap
TIEMPO_ESPERA = 5

# Mensajes series
SERIE_INI = "Series disponibles:"
SERIE_FIN = "Que serie quieres ver? n de serie:"
SERIE_ADD = ["Abrir carpeta"]

# Mensajes temporadas
TEMP_INI = "Temporadas disponibles:"
TEMP_FIN = "Que temporada quieres ver? n de temp:"

# Mensajes caps
CAP_INI = "Capitulos disponibles"
CAP_FIN = "Que capitulo quieres ver? n de cap:"

# Acciones tras reproduccion
ACC_INI = 'Que quieres hacer?:'
ACC_FIN = 'Opcion:'

# Posibilidades de eliminar
DEL_INI = 'Que quieres eliminar?:'
DEL_ARRAY = ['Eliminar todos los capitulos vistos',
             'Eliminar todo menos el ultimo',
             'Elegir cuales eliminar',
             'No eliminar ninguno']
DEL_FIN = 'Opcion:'

# Seleccion de caps a borrar
SELD_INI = 'Capitulos a borrar:'
SELD_FIN = 'Escribe el numero de los caps separados con coma'

#####################
#   FUNCIONES       #
#####################

def imprimir_array_mensajes(mensaje_ini, mensaje_fin, array, opcion_adicional=None):
    """ Recorre un array con las opciones para que el usuario tome una decision """
    print mensaje_ini

    # recorre las opciones adicionales que van a parte del array de series o capitulos
    cont = 0
    for opcion in opcion_adicional:
        print "\t" + str(cont) + ". " + opcion
        cont = cont + 1

    # recorre el array con las series o capitulos
    cont = 1 if cont == 0 else cont
    for elem in array:
        print "\t" + str(cont) + ". " + elem
        cont = cont + 1

    print mensaje_fin
    return input()


def comprobar_apertura_carpeta(serie):
    """Se encarga de comprobar si quieres hbrir la carpeta de las series"""
    # Si quieres abrir la carpeta para aniadir una serie o algo la opcion 0 activa esto
    if serie == -1:
        system('start ' + SERIES_PATH)
        exit()


def obtener_temporadas(serie_path, elegir=False):
    """ Este metodo se encarda de comprobar si hay temporadas, si
    elegir es falso devuelve la primera carpeta si no da a elegir cual quieres ver """
    elementos = listdir(serie_path)
    path_auxiliar = serie_path
    if isdir(join(serie_path, elementos[0])):
        temp = 0
        if elegir:
            temp = int(imprimir_array_mensajes(
                TEMP_INI, TEMP_FIN, elementos)) - 1
        serie_path = join(serie_path, elementos[temp])
        elementos = listdir(serie_path)
    else:
        path_auxiliar = None
    return (serie_path, elementos, path_auxiliar)


def eliminar_capitulos(eliminaciones_programadas, serie_path, path_auxiliar):
    """ Metodo que se encarga de borrar los archivos que indica el array
    eliminaciones_programadas """
    if eliminaciones_programadas:
        print "Se van a eliminar los archivos planificados"
        for archivo in eliminaciones_programadas:
            print "eliminadno " + archivo + "..."
            time.sleep(0.5)
            remove(archivo)
        if not listdir(serie_path):
            print "No quedan capitulos eliminando carpeta..."
            time.sleep(1)
            rmdir(serie_path)
            if path_auxiliar is not None and not listdir(path_auxiliar):
                print "No quedan temporadas eliminando carpeta..."
                time.sleep(1)
                rmdir(path_auxiliar)


def counter(tiempo, mensaje):
    """ Contador que si no se detiene devuelve None si se detiene devuelve otra cosa"""
    inp = None
    for i in range(tiempo, 0, -1):
        if msvcrt.kbhit():
            inp = msvcrt.getch()
            break
        print mensaje + ' %d sec, presiona algo para parar: \r' % i,
        sys.stdout.flush()
        time.sleep(1)
    if not inp:
        print mensaje + ' 0 sec:                             '
    else:
        # con estre print evito superposiciones de texto
        print ''
    return inp


#####################
#       INICIO      #
#####################

def main():

    #####################
    #     Variables     #
    #####################

    # Recorro la carpeta de series y creo un array con las carpetas de dentro
    series = [fichero for fichero in listdir(SERIES_PATH)
              if isdir(join(SERIES_PATH, fichero))]

    #####################
    #     INICIO COD    #
    #####################

    if len(sys.argv) < 2:
        serie = int(imprimir_array_mensajes(
            SERIE_INI, SERIE_FIN, series, SERIE_ADD)) - 1
    else:
        serie = int(sys.argv[1]) - 1

    apagar = serie < -1
    if apagar:
        serie = abs(serie + 2)

    comprobar_apertura_carpeta(serie)

    # hago que serie_path apunte a la carpeta de la serie a ver y si hay temporadas elegir cual
    # caps tiene todos los capitulos de una serie, esta fuera del while para reducir llamadas 
    # al sistema y se actualizara solo cuando se llame a cambiar serie
    (serie_path, caps, path_auxiliar) = obtener_temporadas(
        join(SERIES_PATH, series[serie]))

    # while que se encarga de preguntar que quieres hacer al acabar de ver el capitulo
    continua = True
    cap = 0

    # array que guarda los capitulos vistos en reproduccion automatica
    vistos = []

    # array que va guardando los capitulos que has decidido borrar al final de la ejecucion
    eliminaciones_programadas = []

    # booleana por si se quiere apagar el ordena
    while continua:
        capitulo = join(serie_path, caps[cap])
        print "Reproduciendo " + caps[cap] + "..."
        subprocess.call([REPRODUCTOR, '--fullscreen', capitulo])

        if apagar:
            if not counter(10, 'El ordenador se apagara en'):
                eliminar_capitulos(eliminaciones_programadas,
                                   serie_path, path_auxiliar)
                subprocess.call("shutdown -s -t 0")
            else:
                apagar = False

        vistos.append(capitulo)

        # inicio del contador para reproduccion automatica
        if cap + 1 < len(caps) and not counter(TIEMPO_ESPERA, 'Finalizado "\
        "el siguiente capitulo empezara en'):
            cap += 1
            continue
        elif cap + 1 == len(caps):
            print 'No quedan mas capitulos'

        # comprobacion de si se quieren eliminar los archivos una vez vistos
        if len(vistos) == 1:
            if capitulo not in eliminaciones_programadas:
                print "Quieres eliminar el archivo? (se eliminaran al final)[S/s]"
                delete = str(raw_input())
                if delete == "S" or delete == "s":
                    # se aniade el archivo al array para borrarlo despues
                    eliminaciones_programadas.append(capitulo)
            else:
                print "Quieres evitar la eliminacion del archivo?[S/s]"
                delete = str(raw_input())
                if delete == "S" or delete == "s":
                    # se quita el archivo al array para no borrarlo despues
                    eliminaciones_programadas.remove(capitulo)
        else:
            eliminar = int(imprimir_array_mensajes(
                DEL_INI, DEL_FIN, DEL_ARRAY))

            # eliminar todos menos el ultimo
            if eliminar == 2:
                print 'eliminacion planificada'
                vistos = vistos[0:-1]
            # elegir los que eliminar
            elif eliminar == 3:
                print 'eliminacion planificada'
                elementos = imprimir_array_mensajes(
                    SELD_INI, SELD_FIN, vistos[1:], [vistos[0]])
                if isinstance(elementos, tuple):
                    auxiliar_vistos = vistos
                    vistos = []
                    for element in elementos:
                        vistos.append(auxiliar_vistos[element])
                else:
                    vistos = [vistos[elementos]]
            # no se elimina nada o se eliminan todos
            elif eliminar != 1:
                print 'no se eliminra nada'
                vistos = []

            eliminaciones_programadas = list(
                set(eliminaciones_programadas) | set(vistos))

        vistos = []

        # segunda tanda de opciones ha realizar
        acciones = ["Siguiente cap -> " + (caps[cap + 1] if cap < len(caps) - 1 else caps[cap]),
                    "Anterior cap  -> " +
                    (caps[cap - 1] if cap > 0 else caps[cap]),
                    "Elegir cap",
                    "Cambiar serie",
                    "Ultimo y apaga",
                    "Salir"]

        accion = int(imprimir_array_mensajes(ACC_INI, ACC_FIN, acciones))
        # siguiente capitulo
        if accion == 1:
            if cap < len(caps) - 1:
                cap += 1
        # anterior capitulo
        elif accion == 2:
            if cap > 0:
                cap -= 1
        # elegir capitulo
        elif accion == 3:
            cap = int(imprimir_array_mensajes(CAP_INI, CAP_FIN, caps)) - 1
        # Cambiar de serie
        elif accion == 4:
            # se eliminaran los capitulos planificados
            eliminar_capitulos(eliminaciones_programadas,
                               serie_path, path_auxiliar)
            eliminaciones_programadas = []
            # se actualiza las series disponibles
            series = [fichero for fichero in listdir(SERIES_PATH)
                      if isdir(join(SERIES_PATH, fichero))]
            cap = 0
            serie = int(imprimir_array_mensajes(
                SERIE_INI, SERIE_FIN, series, SERIE_ADD)) - 1
            comprobar_apertura_carpeta(serie)
            # consigo que serie_path apunte a la carpeta de la serie a ver y si hay temporadas
            # elegir cual caps tiene todos los capitulos de una serie, esta fuera del while para
            # reducir llamadas al sistema y se actualizara solo cuando se llame a cambiar serie
            (serie_path, caps, path_auxiliar) = obtener_temporadas(
                join(SERIES_PATH, series[serie]), True)
        # Ultimo capitulo y apagar el ordenador
        elif accion == 5:
            print "Se apagara el ordenador despues de reproducir el capitulo, si se desea anular" \
                " tendra 5 segundos tras finalizar el capitulo, antes de apagar se borraran" \
                " todos los capitulos planificados y se mantendra el ultimo"
            time.sleep(2)
            cap += 1
            apagar = True
        # Salir del programa
        elif accion == 6:
            continua = False

    # Se eliminaran los capitulos planificados
    eliminar_capitulos(eliminaciones_programadas, serie_path, path_auxiliar)
    print "BYE"
    time.sleep(1)


if __name__ == '__main__':
    main()
