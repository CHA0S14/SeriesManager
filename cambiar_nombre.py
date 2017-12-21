"""
            Autor: Ismael Ortega			Email: ismaelortegasanchez@hotmail.com

    LEE EL README DE GITHUB ANTES DE USAR:	https://github.com/CHA0S14/SeriesManager.git

    Este programa se encarga de cambiar el nombre de todos los archivos en una carpeta
    por su diferencia
    cap1.txt seria 1.txt si los demas archivos se llaman por ejemplo cap2.txt, cap3.txt
"""
import sys
import os
import re


def main():
    """ Metodo principal del programa """
    # Comprobamos los parametros del programa
    if len(sys.argv) < 2:
        _, tail = os.path.split(sys.argv[0])
        print """Uso: """ + tail + """ [Folder path]"""
        exit(1)

    os.chdir(sys.argv[1])
    archivos = [fichero for fichero in os.listdir(".")]

    print get_nombres_modificados(archivos)


def get_nombres_modificados(archivos):
    """ Metodo que se encarga de devolver los nombres modificados del array de archivos """
    digitos = []
    for archivo in archivos:
        str1, extension = os.path.splitext(archivo)

        digitos.append(int(re.sub(r"\D", "", str1)))

    nombres = []
    print digitos
    # TODO Ahora que????
    return nombres


def sacar_numeros(str1):
    """ Metodo que se encarga de devolver los numeros de un texto """
    


if __name__ == '__main__':
    main()
