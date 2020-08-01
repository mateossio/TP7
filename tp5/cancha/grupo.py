from generador_pseudoaliatorio.generador import Generador

class Grupo:
    nro=0
    instances=set()

    def __init__(self):
        self.nombre = "Grupo"
        self.generador_ocupacion = Generador(decimals=4, random=True)
        self.generador_llegada = Generador(decimals=4, random=True)
        self.cola = False
        self.acondicionando = False
        self.fin_ocupacion = 0
        self.cancha = None
        self.tipo = ""
        self.finalizado = False

    def __str__(self):
        return str(self.as_dict()) + '\n'

    @property
    def tiempo_ocupacion(self):
        pass

    @property
    def estado(self):
        if self.acondicionando:
            return "Finalizado"
        elif self.cola:
            return "Esperando Cancha"
        elif self.cancha.acondicionando and self.acondicionando:
            return "Esperando Acondicionamiento"
        else:
            return "Jugando en cancha"

    def as_dict(self):
        return {
            'nombre':self.nombre,
            'estado':self.estado,
            'fin_ocupacion':self.fin_ocupacion,
            'tiempo_ocupacion': self.tiempo_ocupacion,
        }

    @classmethod
    def resetear_lote(cls):
        cls.nro = 0

class GrupoFutbol(Grupo):
    def __init__(self, media, desviacion):
        super(GrupoFutbol, self).__init__()
        self.media = media
        self.desviacion = desviacion
        self.numero=GrupoFutbol.get_nro()
        self.nombre = self.nombre + "_Futbol_" + str(self.numero)
        self.tipo = "Futbol"


    @classmethod
    def get_nro(cls):
        "Devuelve el nº de grupo q se asigna al crearse"
        cls.nro+=1
        return  cls.nro

    @property
    def tiempo_ocupacion(self):
        return self.generador_ocupacion.box_muller_next(media=self.media, desviacion=self.desviacion)

class GrupoHandball(Grupo):
    def __init__(self, media, desviacion):
        super(GrupoHandball, self).__init__()
        self.media = media
        self.desviacion = desviacion
        self.numero=GrupoHandball.get_nro()
        self.nombre = self.nombre + "_Handball_" + str(self.numero)
        self.tipo = "Handball"

    @classmethod
    def get_nro(cls):
        "Devuelve el nº de grupo q se asigna al crearse"
        cls.nro+=1
        return  cls.nro

    @property
    def tiempo_ocupacion(self):
        return self.generador_ocupacion.box_muller_next(media=self.media, desviacion=self.desviacion)

class GrupoBasquet(Grupo):
    def __init__(self, media, desviacion):
        super(GrupoBasquet, self).__init__()
        self.media = media
        self.desviacion = desviacion
        self.numero=GrupoBasquet.get_nro()
        self.nombre = self.nombre + "_Basquet_" + str(self.numero)
        self.tipo = "Basquet"

    @classmethod
    def get_nro(cls):
        "Devuelve el nº de grupo q se asigna al crearse"
        cls.nro+=1
        return  cls.nro

    @property
    def tiempo_ocupacion(self):
        return self.generador_ocupacion.box_muller_next(media=self.media, desviacion=self.desviacion)

"""if __name__ == '__main__':
    #futbol = GrupoFutbol(1.30, 0.167, 10)
    handball = GrupoHandball(1.33, 0.33)
    basquet = GrupoBasquet(1.67, 0.5)
    for i in range(20):
        futbol = GrupoFutbol(1.30, 0.167)
        print(futbol.as_dict())
    #print(handball.as_dict())
    #print(basquet.as_dict())"""
