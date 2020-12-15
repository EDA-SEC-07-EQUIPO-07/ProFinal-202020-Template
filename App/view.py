"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """


import sys
import config
from App import controller
from DISClib.ADT import stack
import timeit
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from time import process_time
assert config
from DISClib.DataStructures import listiterator as it
from DISClib.ADT.graph import gr

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________

initialStation = None
recursionLimit = 20000
filename = "taxi-trips-wrvz-psew-subset-small.csv"
# ___________________________________________________
#  Menu principal
# ___________________________________________________

"""
Menu principal
"""
def printMenu():
    print("\n")
    print("Bienvenido")
    print("1. Inicializar Analizador")
    print("2. Cargar información archivo")
    print("3. Top de compañías con más servicios y taxis")
    print("4. Top de taxis con más puntos en ciertas fechas")
    print("5. Horario entre areas comunitarias")
    print("6. Salir")
def OtrasOpciones():
    print("1. Ranking de taxis con más puntos para una fecha específica")
    print("2. Ranking de taxis con más puntos para un rango de fechas")
while True:
    printMenu()
    opciones = input('Seleccione una opción para continuar\n>')

    if int(opciones[0]) == 1:
        print("\nInicializando....")
        cont = controller.init()
    elif int(opciones[0]) == 2:
        print("\nCargando información de accidentes ....")
        archivo = input("Ingrese la palabra: small, medium o large, para determinar el archivo a cargar: ")
        if archivo == "small":
            filename = "taxi-trips-wrvz-psew-subset-small.csv"
        if archivo == "medium":
            filename = "taxi-trips-wrvz-psew-subset-medium.csv"
        if archivo == "large":
            filename = "taxi-trips-wrvz-psew-subset-large.csv"
        controller.loadTrips(cont, filename)
        sys.setrecursionlimit(recursionLimit)
    elif int(opciones[0]) == 3:
        top = int(input("Ingrese la cantidad de compañías mostradas en el ranking: "))
        cantTax = controller.Cantidad_Taxis(cont)
        Cantidad_compañias = controller.Cantidad_Taxis(cont)
        topTaxi, topServices = controller.TOP_TAXI(cont, top)
        print("Cantidad total de taxis reportados: {0}".format(cantTax))
        print("Cantidad total de compañías con un taxi inscrito: {0}".format(Cantidad_compañias))
        print("\nEl ranking {0} de compañías con más taxis es: ".format(top))
        iterador1 = it.newIterator(topTaxi)
        numero = 1
        while it.hasNext(iterador1):
            taxi = it.next(iterador1)
            print("{0}. {1} con {2} taxis.".format(numero, list(taxi.keys())[0], list(taxi.values())[0]))
            numero += 1
        print("\nEl top {0} de compañías con más servicios es: ".format(top))
        iterador2 = it.newIterator(topServices)
        numero = 1
        while it.hasNext(iterador2):
            service = it.next(iterador2)
            print("{0}. {1} con {2} servicios.".format(numero, list(service.keys())[0], list(service.values())[0]))
            numero += 1
    elif int(opciones[0]) == 4:
        OtrasOpciones()
        Rangos = input('Seleccione una opción para continuar\n>')
        if Rangos == "1":
            fecha = input("Entre la fecha(Formato: YYYY-MM-DD): ")
            top = int(input("Ingrese la cantidad de taxis mostrados en el ranking: "))
            print("\nBuscando taxis dentro de la fecha {0}".format(fecha))
            res = controller.PUNTOS_IND(cont, fecha, top)
            if res is not None:
                iterador1 = it.newIterator(res)
                numero = 1
                while it.hasNext(iterador1):
                    taxi = it.next(iterador1)
                    print("{0}. Taxi ID: {1}\nCantidad de puntos: {2}\n".format(numero, list(taxi.keys())[0], list(taxi.values())[0]))
                    numero += 1
            else:
                print("La fecha ingresada no existe.")
        elif Rangos == "2":
            Inicial = input("Entre la fecha inicial (Formato: YYYY-MM-DD): ")
            Final = input("Entre la fecha final (Formato: YYYY-MM-DD): ")
            top = int(input("Ingrese la cantidad de taxis mostrados en el ranking: "))
            print("\nBuscando taxis dentro de la fechas {0} y {1}".format(Inicial, Final))
            res = controller.topPuntosTaxiMultiple(cont, Inicial, Final, top)
            if res is not None:
                iterador1 = it.newIterator(res)
                numero = 1
                while it.hasNext(iterador1):
                    taxi = it.next(iterador1)
                    print("{0}. Taxi ID: {1}\nTuvo una cantidad de puntos de : {2}\n".format(numero, list(taxi.keys())[0], list(taxi.values())[0]))
                    numero += 1
            else:
                print("Alguna de las fechas no existen.")

    elif int(opciones[0]) == 5:
        CAOrigen = int(input("Ingrese la 'Community Area' de origen: "))
        CADest = int(input("Ingrese la 'Community Area' de destino: "))
        horaIni = input("Entre la hora inicial Formato: HH:MM): ")
        horaFin = input("Entre la hora final (Formato: HH:MM): ")
        path, tiempo = controller.MENOR_CA(cont, CAOrigen, CADest, horaIni, horaFin)
        if path is not None:
            print("\nLa ruta encontrada es la siguiente: ")
            iterador = it.newIterator(path)
            while it.hasNext(iterador):
                element = it.next(iterador)
                vertA = element["vertexA"]
                print("'Community Area': ID {0}".format(vertA))
                if it.hasNext(iterador) is False:
                    print("'Community Area': ID {0}".format(element["vertexB"]))
            print("El tiempo estimado en viaje es de: {0} segundos o {1} minutos.".format(round(tiempo), round(tiempo/60)))
        elif path is None:
            print("No se encontró camino entre las 'Community Areas' en el horario introducido.")
        else:
            print("Alguna de las 'Community Areas' introducidas no existe.")
            
    else:
        sys.exit(0)
sys.exit(0)

