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
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from DISClib.DataStructures import edge as ed
from DISClib.Algorithms.Graphs import bfs
from DISClib.ADT import stack
assert config
from math import radians, cos, sin, asin, sqrt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
import datetime
from DISClib.DataStructures import adjlist as alt

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------

# Funciones para agregar informacion al grafo
def TaxiAnalyzer():
    Taxis = {
                'compañias': None,
                'taxis': None,
                'fechas': None,
                'communityAreas': None, 
                'paths': None
                    }
    Taxis['compañias'] = m.newMap(numelements=150,
                                     maptype='PROBING',
                                     comparefunction=CompararCompañias)
    Taxis['fechas'] = om.newMap(omaptype="RBT", comparefunction=CompararFechas)
    Taxis['communityAreas'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=10000,
                                              comparefunction=AreaComun)
    return  Taxis

def maxDicc(diccionario: dict):
    llaves = list(diccionario.keys())
    valores = list(diccionario.values())
    mayor = max(valores)
    Max = str(llaves[valores.index(mayor)])
    return Max

def minDicc(diccionario: dict):
    llaves = list(diccionario.keys())
    valores = list(diccionario.values())
    menor = max(valores)
    Min = str(llaves[valores.index(menor)])
    return Min

def Taxi_Por_Fecha(taxitrip):
    tripstartdate = taxitrip['trip_start_timestamp']
    taxitripdatetime = datetime.datetime.strptime(tripstartdate, '%Y-%m-%dT%H:%M:%S.%f')
    return taxitripdatetime.date(), taxitripdatetime.time()
def Nueva_Compañia(trip):
    company = {"name": "", "taxis":None, "trips":1}
    company["name"] = trip["company"]
    company["taxis"] = lt.newList("ARRAY_LIST", compareTaxiIdsInt)
    lt.addLast(company["taxis"], trip["taxi_id"])
    return company
def Agregar_Compañia(Taxis, trip):
    companies = Taxis["compañias"]
    companyName = trip["company"]
    existComp = m.get(companies, companyName)
    if existComp is None:
        company = Nueva_Compañia(trip)
        m.put(companies, companyName, company)
    else:
        entry = m.get(companies, companyName)
        taxiId = trip["taxi_id"]
        info = entry["value"]
        info["trips"] += 1
        taxilst = info["taxis"]
        if lt.isPresent(taxilst, taxiId) == 0:
            lt.addLast(taxilst, taxiId)
def NuevasFechas(map, trip):
    mapa = map["fechas"]
    tripdate = trip['trip_start_timestamp']
    taxitripdatetime = datetime.datetime.strptime(tripdate, '%Y-%m-%dT%H:%M:%S.%f')
    entry = om.get(mapa, taxitripdatetime.date())
    if entry is None:
        datentry = Nueva_entrada_datos(trip)
        om.put(mapa, taxitripdatetime.date(), datentry)
    else:
        datentry = me.getValue(entry)
        Actualizar_entrada(trip, datentry)
    return mapa
def Nueva_entrada_datos(trip):
    entry = {'taxis': None}
    entry['taxis'] = m.newMap(numelements=1000, maptype="PROBING", comparefunction=compareTaxiIdsDict)
    taxidata = lt.newList("ARRAY_LIST")
    if trip["trip_miles"] == "":
        lt.addLast(taxidata, 0)
    else:
        lt.addLast(taxidata, float(trip["trip_miles"]))
    if trip["trip_total"] == "":
        lt.addLast(taxidata, 0)
    else:
        lt.addLast(taxidata, float(trip["trip_total"]))
    lt.addLast(taxidata, 1)
    m.put(entry['taxis'], trip["taxi_id"], taxidata)
    return entry
def Actualizar_entrada(trip, datentry):
    taxis = datentry["taxis"]
    existtaxi = m.get(taxis, trip["taxi_id"])
    if existtaxi is None:
        taxidata = lt.newList("ARRAY_LIST")
        if trip["trip_miles"] == "":
            lt.addLast(taxidata, 0)
        else:
            lt.addLast(taxidata, float(trip["trip_miles"]))
        if trip["trip_total"] == "":
            lt.addLast(taxidata, 0)
        else:
            lt.addLast(taxidata, float(trip["trip_total"]))
        lt.addLast(taxidata, 1)
        m.put(taxis, trip["taxi_id"], taxidata)
    else:
        entry = existtaxi["value"]
        if trip["trip_miles"] != "":
            entry["elements"][0] += float(trip["trip_miles"])
        if trip["trip_total"] != "":
            entry["elements"][1] += float(trip["trip_total"])
        entry["elements"][2] += 1
    return datentry
def Agregar_viaje(Taxis, trip):
    origin = trip['pickup_community_area']
    destination = trip['dropoff_community_area']
    if origin == "":
        origin = "-1"
    else:
       origin = round(float(origin))
    if destination == "":
        destination = "-1"
    else:
        destination = round(float(destination))
    if trip['trip_seconds'] == "":
        duration = 0
    else:
        duration = float(trip['trip_seconds'])
    horaIni = trip["trip_start_timestamp"]
    horaFin = trip["trip_end_timestamp"]
    if horaIni == "" or horaFin == "":
        pass
    else:
        timeSt = datetime.datetime.strptime(horaIni, '%Y-%m-%dT%H:%M:%S.%f')
        timeEnd = datetime.datetime.strptime(horaFin, '%Y-%m-%dT%H:%M:%S.%f')
        vertOrigen = str(origin)+" - "+str(timeSt.time())
        vertDestino = str(destination)+" - "+str(timeEnd.time())
        Añadir_comunity_area(Taxis, vertOrigen)
        Añadir_comunity_area(Taxis, vertDestino)
        Añadir_conexion(Taxis, vertOrigen, vertDestino, duration)
        return Taxis
def Añadir_comunity_area(Taxis, CAid):
    if not gr.containsVertex(Taxis["communityAreas"], CAid):
            gr.insertVertex(Taxis["communityAreas"], CAid)
    return Taxis
def Añadir_conexion(Taxis, origin, destination, duration):
    edge = gr.getEdge(Taxis["communityAreas"], origin, destination)
    if edge is None:
        splitOrig = origin.split(" - ")
        splitDest = destination.split(" - ")
        if splitOrig[0] != splitDest[0]:
            gr.addEdge(Taxis["communityAreas"], origin, destination, duration)
        else:
            pass
    else:
        ed.updateAverageWeight(edge, duration) 
    return Taxis   
# ==============================
# Funciones de consulta
# ==============================
def Cantidad_Taxis(Taxis):
    companies = m.keySet(Taxis["compañias"])
    iterador = it.newIterator(companies)
    cantTax = 0
    while it.hasNext(iterador):
        company = it.next(iterador)
        data = m.get(Taxis["compañias"], company)
        cantTax += lt.size(data["value"]["taxis"])
    return cantTax
def Cantidad_compañias(Taxis):
    companies = m.keySet(Taxis["compañias"])
    num = lt.size(companies)
    return num
def TOP_TAXI(Taxis, top):
    companies = m.keySet(Taxis["compañias"])
    iterador = it.newIterator(companies)
    dicc1 = {}
    dicc2 = {}
    topTaxis = lt.newList("ARRAY_LIST")
    topServices = lt.newList("ARRAY_LIST")
    num = 1
    while it.hasNext(iterador):
        company = it.next(iterador)
        data = m.get(Taxis["compañias"], company)
        cantTax = lt.size(data["value"]["taxis"])
        dicc1[company] = cantTax
        dicc2[company] = data["value"]["trips"]
    while num <= top:
        resultado1 = maxDicc(dicc1)
        resultado2 = maxDicc(dicc2)
        inp1 = {resultado1: dicc1[resultado1]}
        inp2 = {resultado2: dicc2[resultado1]}
        lt.addLast(topTaxis, inp1)
        lt.addLast(topServices, inp2)
        dicc1.pop(resultado1)
        dicc2.pop(resultado2)
        num +=1
    return topTaxis, topServices
def PUNTOS_IND(Taxis, fecha, top):
    dateanalyzed = om.get(['fechas'], fecha)
    if dateanalyzed["key"] is not None:
        entry = dateanalyzed["value"]["taxis"]
        llaves = m.keySet(entry)
        iterador = it.newIterator(llaves)
        dicc = {}
        num = 1
        topTaxis = lt.newList("ARRAY_LIST")
        while it.hasNext(iterador):
            taxi = it.next(iterador)
            valor = m.get(entry, taxi)
            data = valor["value"]
            if data["elements"][1] == 0:
                puntos = 0
            else:
                puntos = (data["elements"][0]/data["elements"][1])*data["elements"][2]
            dicc[taxi] = puntos
        while num <= top:
            resultado = maxDicc(dicc)
            inp = {resultado: dicc[resultado]}
            lt.addLast(topTaxis, inp)
            dicc.pop(resultado)
            num += 1
        return topTaxis
    else:
        return None
def topPuntosTaxiMultiple(Taxis, dateIni, dateFin, top):
    dateanalyzed1 = om.get(Taxis['fechas'], dateIni)
    dateanalyzed2 = om.get(Taxis['fechas'], dateFin)
    if dateanalyzed1["key"] is not None and dateanalyzed2["key"]:
        valor = om.keys(Taxis["fechas"], dateIni, dateFin)
        iterador = it.newIterator(valor)
        taxis = {}
        topRangoTaxis = lt.newList("ARRAY_LIST")
        num = 1
        while it.hasNext(iterador):
            fecha = it.next(iterador)
            lista = PUNTOS_IND(Taxis, fecha, top)
            iterador2 = it.newIterator(lista)
            while it.hasNext(iterador2):
                taxi = it.next(iterador2)
                if str(taxi.keys()) in str(taxis.keys()):
                    taxis[str(taxi.keys())] += float(taxi.values())
                else:
                    taxis.update(taxi)
        while num <= top:
            resultado = maxDicc(taxis)
            inp = {resultado: taxis[resultado]}
            lt.addLast(topRangoTaxis, inp)
            taxis.pop(resultado)
            num += 1
        return topRangoTaxis
    else:
        return None
def totalEdges(Taxis):
    return gr.numEdges(Taxis['communityAreas'])
def Estaciones_totales(Taxis):
    return gr.numVertices(Taxis['communityAreas'])
def Caminos_menor_costo(Taxis, initialStation):
    if gr.containsVertex(Taxis["communityAreas"], initialStation) == True:
        Taxis['paths'] = djk.Dijkstra(Taxis['communityAreas'], initialStation)
        return Taxis
    else:
        return "0"
def minimumCostPath(Taxis, destStation):
    path = djk.pathTo(Taxis['paths'], destStation)
    return path
def MENOR_CA(Taxis, initCA, destCA, hourStart, hourEnd):
    if hourStart.minute >= 0 and hourStart.minute <= 15:
        horaIni = hourStart.replace(minute=0, second=0, microsecond=0)
    elif hourStart.minute > 15 and hourStart.minute <= 30:
        horaIni = hourStart.replace(minute=15, second=0, microsecond=0)
    elif hourStart.minute > 30 and hourStart.minute <= 45:
        horaIni = hourStart.replace(minute=45, second=0, microsecond=0)
    elif hourStart.minute > 45 and hourStart.minute <= 59:
        horaIni = hourStart.replace(minute=0, second=0, microsecond=0)    
        if hourStart.hour == 23:
            hora = 0
        else:
            hora = hourStart.hour + 1
        horaIni = hourStart.replace(hour=hora, minute=0, second=0, microsecond=0)
    if hourEnd.minute >= 0 and hourEnd.minute <= 15:
        horaFin = hourEnd.replace(minute=0, second=0, microsecond=0)
    elif hourEnd.minute > 15 and hourEnd.minute <= 30:
        horaFin = hourEnd.replace(minute=15, second=0, microsecond=0)
    elif hourEnd.minute > 30 and hourEnd.minute <= 45:
        horaFin = hourEnd.replace(minute=45, second=0, microsecond=0)
    elif hourEnd.minute > 45 and hourEnd.minute <= 59:
        horaFin = hourEnd.replace(minute=0, second=0, microsecond=0)    
        if hourEnd.hour == 23:
            hora = 0
        else:
            hora = hourEnd.hour + 1
        horaFin = hourEnd.replace(hour=hora, minute=0, second=0, microsecond=0)
    vertIni = str(initCA)+ " - " + str(horaIni)
    vertDest = str(destCA) + " - " + str(horaFin)
    if gr.containsVertex(Taxis["communityAreas"], vertIni) == True and gr.containsVertex(Taxis["communityAreas"], vertDest) == True:
        Caminos_menor_costo(Taxis, vertIni)
        path = minimumCostPath(Taxis, vertDest)
        if path is not None:
            tiempo = 0
            iterador2 = it.newIterator(path)
            while it.hasNext(iterador2):
                camino = it.next(iterador2)
                tiempo += camino["weight"]
            return path, tiempo
        else:
            return None, None
    else:
        return False, False
# ==============================
# Funciones Helper
# ==============================

# ==============================
# Funciones de Comparacion
# ==============================
def CompararFechas(date1, date2):
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1
def compareTaxiIdsInt(id1, id2):
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1
def compareTaxiIdsDict(id1, id2):
    tax = id2['key']
    if (id1 == tax):
        return 0
    elif id1 > tax:
        return 1
    else:
        return -1
def CompararCompañias(comp1, comp2):
    est = comp2['key']
    if (comp1 == est):
        return 0
    elif (comp1 > est):
        return 1
    else:
        return -1
def AreaComun(id1, id2):
    id1 = id1
    CA2 = id2['key']
    
    if (id1 == CA2):
        return 0
    elif id1 > CA2:
        return 1
    else:
        return -1
def compareint(int1, int2):
    if (int1 == int2):
        return 0
    else:
        pass
# Funciones de Comparacion
# ==============================
