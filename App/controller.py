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

import config as cf
from App import model
import csv
import os
import datetime

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________
def init():
    Taxis = model.TaxiAnalyzer()
    return Taxis

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________
def loadTrips(Taxis):
    for filename in os.listdir(cf.data_dir):
        if filename.endswith('.csv'):
            print('Cargando archivo: ' + filename)
            loadFile(Taxis, filename)
    return Taxis
def loadFile(Taxis, tripfile):
    tripfile = cf.data_dir + tripfile
    input_file = csv.DictReader(open(tripfile, encoding="utf-8"),
                                delimiter=",")
    for trip in input_file:
        model.Agregar_Compañia(Taxis, trip)
        model.NuevasFechas(Taxis, trip)
        model.Agregar_viaje(Taxis, trip)
    return Taxis
# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def Cantidad_Taxis(Taxis):
    return model.Cantidad_Taxis(Taxis)
def Cantidad_compañias(Taxis):
    return model.Cantidad_compañias(Taxis)
def TOP_TAXI(Taxis, top):
    return model.TOP_TAXI(Taxis, top)
def PUNTOS_IND(Taxis, date, top):
    fecha = datetime.datetime.strptime(date, '%Y-%m-%d')
    return model.PUNTOS_IND(Taxis, fecha.date(), top)
def topPuntosTaxiMultiple(Taxis, dateIni, dateFin, top):
    fechaIni = datetime.datetime.strptime(dateIni, '%Y-%m-%d')
    fechaFin = datetime.datetime.strptime(dateFin, '%Y-%m-%d')
    return model.topPuntosTaxiMultiple(Taxis, fechaIni.date(), fechaFin.date(), top)
def MENOR_CA(Taxis, initCA, destCA, horaIni, horaFin):
    horaI = datetime.datetime.strptime(horaIni, "%H:%M")
    horaF = datetime.datetime.strptime(horaFin, "%H:%M")
    return model.MENOR_CA(Taxis, initCA, destCA, horaI.time(), horaF.time())