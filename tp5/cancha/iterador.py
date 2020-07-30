from generador_pseudoaliatorio.generador import Generador
from grupo import GrupoFutbol,GrupoHandball,GrupoBasquet
from cancha import Cancha

class Iteracion:

    def __init__(self, desde=0, hasta=30, ultimas_filas=10, medias_llegada=[10, 12, 8], medias_ocupacion=[1.30, 1.33, 1.67], desviaciones_llegada=[0, 2, 2], desviaciones_ocupacion=[0.167, 0.33, 0.5]):
        self.tabla = []
        self.tabla_final = []
        self.cantidad_iteraciones = 1
        self.decimales = 4
        #Paso arrays para poder config los tiempos de llegada  ocup
        self.medias_llegada = medias_llegada
        self.medias_ocupacion = medias_ocupacion
        self.desviaciones_llegada = desviaciones_llegada
        self.desviaciones_ocupacion = desviaciones_ocupacion

        self.generadorFutbol = Generador(decimals=4, random=True)
        self.generadorHandball = Generador(decimals=4, random=True)
        self.generadorBasquet = Generador(decimals=4, random=True)

        self.numero = 0
        self.evento = "Inicializacion"
        self.reloj = 0

        self.desde = desde
        self.hasta = hasta
        self.ultimas_filas = ultimas_filas

        self.cancha = Cancha()
        self.acondicionando = False

        #En_todo momento van a haber 3 grupos concurrentes cada uno con su tiempo de ocupacion
        self.grupo_actual = None
        self.grupo_actual_futbol = GrupoFutbol(media=self.medias_ocupacion[0], desviacion=self.desviaciones_ocupacion[0])
        self.grupo_actual_handball = GrupoHandball(media=self.medias_ocupacion[1], desviacion=self.desviaciones_ocupacion[1])
        self.grupo_actual_basquet = GrupoBasquet(media=self.medias_ocupacion[2], desviacion=self.desviaciones_ocupacion[2])

        #Determino las primeras llegadas de cada grupo
        self.proxima_llegada_futbol = self.generadorFutbol.exponencial_next(media=self.medias_llegada[0])
        self.proxima_llegada_handball = self.generadorHandball.box_muller_next(media=self.medias_llegada[1], desviacion=self.desviaciones_llegada[1])
        self.proxima_llegada_basquet = self.generadorHandball.box_muller_next(media=self.medias_llegada[2], desviacion=self.desviaciones_llegada[2])
        """"#Las meto en un array y lo ordeno cada vez que se modifica un valor
        self.proximas_llegadas = []
        self.proximas_llegadas.append(self.proxima_llegada_futbol)
        self.proximas_llegadas.append(self.proxima_llegada_handball)
        self.proximas_llegadas.append(self.proxima_llegada_basquet)
        self.ordenar_llegadas()"""
        #Determino cual es la prox llegada
        self.set_proxima_llegada()

    #No entiendo como funciona este diccionario
    def __str__(self):
        dic = self.as_dict
        dic.pop('cancha')
        dic.pop('grupos')
        cancha = self.as_dict['cancha']
        grupos = self.as_dict['grupos']
        grupos = '\t' + '\n\t'.join([grupo for grupo in grupos])
        return f"{dic}\n{cancha}\n{grupos}\n"

    #Este tampoco
    def print_tabla(self, tabla):
        print("Tabla")
        for linea in tabla:
            dic = linea.copy()
            cancha = dic.pop('cancha')
            grupos = dic.pop('grupos')
            grupos = '\t' + '\n\t'.join([str(grupo) for grupo in grupos.items()])
            print(f"{dic}\n{cancha}\n{grupos}")
            print("-" * 20)

    def show_evento(self):
        if self.evento == "fin_ocupacion" or self.evento == "llegada":
            if self.grupo_actual:
                return self.evento + '_' + str(self.grupo_actual.nombre)
        return self.evento

    # Devuelve un diccionario con los valores actuales del objeto
    @property
    def as_dict(self):
        # Creo un diccionario con todos los atributos del objeto
        dic = {
            'numero': self.numero,
            'evento': self.show_evento(),
            'reloj': round(self.reloj, self.decimales),
            'proxima_llegada': self.proxima_llegada,
            'prox llegada futbol': self.proxima_llegada_futbol,
            'prox llegada handball': self.proxima_llegada_handball,
            'prox llegada basquet': self.proxima_llegada_basquet,
            #Cancha
            'cancha': self.cancha.as_dict(),
            'grupos': {grupo.numero : grupo.as_dict() for grupo in self.get_grupos()}
        }
        return dic

    #Igual que en otros TPs
    def guardar_iteracion(self):
        "Guarda el estado de una iteracion"
        if self.desde <= self.numero <= self.hasta:
            self.tabla.append(self.as_dict)
        else:
            self.tabla_final.append(self.as_dict)
            if len(self.tabla_final) > self.ultimas_filas:
                self.tabla_final.pop(0)
            # Actualizo el proximo elemnto a reemplazar cuidando de que se mantenga en el rango de las ultimas filas
            # self.pos_ultimo_elemento = (self.pos_ultimo_elemento + 1) % self.ultimas_filas

    def get_grupos(self):
        return self.get_grupos_en_sala() + self.get_grupos_en_cola_futbolhandball() + self.get_grupos_en_cola_basquet()

    def get_grupos_en_sala(self):
        return self.cancha.en_cancha

    def get_grupos_en_cola_futbolhandball(self):
        return self.cancha.en_cola_FutbolHandball

    def get_grupos_en_cola_basquet(self):
        return self.cancha.en_colaBasquet

    def ordenar_tabla_final(self):
        "Ordena la tabla final"
        self.tabla_final = self.tabla_final[self.pos_ultimo_elemento:] + self.tabla_final[:self.pos_ultimo_elemento]

    def set_proxima_llegada(self):
        self.proxima_llegada = min(self.proxima_llegada_futbol, self.proxima_llegada_handball, self.proxima_llegada_basquet)

    def add_proxima_llegada(self, grupo_proximo):
        if grupo_proximo.tipo == "Futbol":
            self.grupo_actual_futbol = GrupoFutbol(media=self.medias_ocupacion[0],desviacion=self.desviaciones_ocupacion[0])
            self.proxima_llegada_futbol = round(self.reloj + self.generadorFutbol.box_muller_next(media=self.medias_llegada[0]), 4)
        elif grupo_proximo.tipo == "Handball":
            self.grupo_actual_handball = GrupoHandball(media=self.medias_ocupacion[1],desviacion=self.desviaciones_ocupacion[1])
            self.proxima_llegada_handball = round(self.reloj + self.generadorHandball.box_muller_next(media=self.medias_llegada[1],desviacion=self.desviaciones_llegada[1]), 4)
        else:
            self.grupo_actual_basquet = GrupoBasquet(media=self.medias_ocupacion[2],desviacion=self.desviaciones_ocupacion[2])
            self.proxima_llegada_basquet = round(self.reloj + self.generadorBasquet.box_muller_next(media=self.medias_llegada[2],desviacion=self.desviaciones_llegada[2]), 4)
        self.set_proxima_llegada()

    """"#Ordenar array de llegadas para ver cual es la siguiente
    def ordenar_llegadas(self):
        proxima_llegada = self.proximas_llegadas[0]
        for llegada in self.proximas_llegadas[1:3]:
            if llegada < proxima_llegada:
                proxima_llegada = llegada
        return proxima_llegada
"""
    #Determina cual es el siguiente evento (falta acondicionamiento)
    def proximo_evento(self):
        grupo_proximo = self.grupo_actual
        if grupo_proximo:
            if self.cancha.acondicionando:
                self.acondicionando = False
                self.evento = "fin_acondicionamiento"
                self.reloj = round( self.reloj + self.cancha.tiempo_acondicionado, 4)
            elif self.proxima_llegada < grupo_proximo.fin_ocupacion or self.grupo_actual.finalizado:
                self.evento = "llegada"
                self.reloj = self.proxima_llegada
            else:
                self.evento = "fin_ocupacion"
                #self.evento = self.show_evento()
                self.reloj = grupo_proximo.fin_ocupacion
        else:
            self.evento = "llegada"
            self.reloj = self.proxima_llegada

    #Diferenciar entre llegada de 3 grupos
    def llegada(self):
        if self.proxima_llegada_futbol == self.proxima_llegada:
            grupo_proximo = self.grupo_actual_futbol
        elif self.proxima_llegada_handball == self.proxima_llegada:
            grupo_proximo = self.grupo_actual_handball
        else:
            grupo_proximo = self.grupo_actual_basquet
        if not self.grupo_actual:
            self.grupo_actual = grupo_proximo
        self.cancha.agregar_grupo(grupo_proximo, self.reloj)
        self.acondicionando = self.cancha.acondicionando
        self.add_proxima_llegada(grupo_proximo)
        self.guardar_iteracion()

    def fin_acondicionamiento(self):
        self.cancha.agregar_grupo(self.grupo_actual, self.reloj)
        self.reloj = self.grupo_actual.fin_ocupacion
        self.guardar_iteracion()

    def fin_ocupacion(self):
        self.cancha.agregar_grupo(self.grupo_actual, self.reloj)
        self.grupo_actual = None
        if len(self.cancha.en_cancha) > 0 :
            self.reloj = self.cancha.en_cancha[0].fin_ocupacion
        else:
            self.reloj = self.proxima_llegada
        self.guardar_iteracion()

    def calcular_iteracion(self, tiempo):
        while True:
            self.numero += 1
            self.proximo_evento()
            if self.reloj > tiempo:
                break
            if self.evento == "llegada":
                self.llegada()
            elif self.evento == "fin_ocupacion":
            #elif self.fin_ocupacion:
                self.fin_ocupacion()
            elif self.evento == "fin_acondicionamiento":
                self.fin_acondicionamiento()
            else:
                raise Exception("Evento inexistente")
            #self.print_tabla(self.tabla)

if __name__ == '__main__':
    it = Iteracion()
    it.guardar_iteracion()
    print(it)
    it.reloj = it.proxima_llegada
    it.calcular_iteracion(20)
    print(it)