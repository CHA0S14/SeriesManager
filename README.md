# SeriesManager
Scrip muy sencillo en python para gestionar las series descargadas en una carpeta

Para usarlo tienes que tener una carpeta que dentro va ha tener una carpeta por cada serie.

en seriesPath va la direccion de la carpeta que contiene las carpetas de cada serie
en reproductor la ruta al reproductor que vas ha usar (el reproductor debe permitir ser llamado desde linea de comandos teniendo como       argumento el video por ejemplo VLC que es el que he usado)


Este script mostrara todas las series(carpetas) en la carpeta y te dara a elegir la que quieras ver y la opcion 0 que es abrir la carpeta de series, reproducira automaticamente el primer video en orden alfabetico, cuando acabe y cierres la ventana te dara la opcion de borrar el video, este video se borrara al finalizar la ejecucion por si quieres verlo de nuevo antes de cerrar, esto es porque despues de esto te da 3 opciones, una ver el siguiente cap, otra es volver al anterior y la ultima es salir, se borran al final por si ves dos caps seguidos en una sesion y luego quieres volver al anterior, daria error si ya lo has borrado y seria mas complicado y menos util.


Espero que lo disfruteis
