# SeriesManager

Este es uno de mis primeros scripts en python asi que no me manejo muy comodamente, siento si algo no es tecnicamente correcto, si algo esta mal ayudadme a mejorar!

Este es un scrip muy sencillo en python para gestionar las series descargadas en una carpeta

Para usarlo tienes que tener una carpeta que dentro va ha tener una carpeta por cada serie.

En seriesPath sustituir <*> por la direccion de la carpeta que contiene las carpetas de cada serie
En reproductor sustituir <*> por la ruta al reproductor que vas ha usar (el reproductor debe permitir ser llamado desde linea de comandos teniendo como argumento el video por ejemplo VLC que es el que he usado)


Este script mostrara todas las series(carpetas) en la carpeta y te dara a elegir la que quieras ver y la opcion 0 que es abrir la carpeta de series, reproducira automaticamente el primer video en orden alfabetico, cuando acabe y cierres la ventana te dara la opcion de borrar el video, este video se borrara al finalizar la ejecucion por si quieres verlo de nuevo antes de cerrar, esto es porque despues de esto te da 5 opciones, una ver el siguiente cap, otra es volver al anterior, elegir el capitulo a ver*1, cambiar de serie y la ultima es salir, se borran al final por si ves dos caps seguidos en una sesion y luego quieres volver al anterior, daria error si ya lo has borrado y seria mas complicado y menos util.

*1 Por que esta en este punto el elegir el capitulo a ver y no nada mas iniciar?
  Muy sencillo, este script esta creado por mi vagueria suprema y quiero poner el primer cap lo antes posible sin opciones inecesarias, si    no quiero ese cap cosa que es menos comun pues cierro el video y voy a esa opcion
  
Espero que lo disfruteis
