from generador_pseudoaliatorio.generador import Generador

class Grupo:
    nro=0
    instances=set()

    @classmethod
    def get_nro(cls):
        "Devuelve el nº de grupo q se asigna al crearse"
        cls.nro+=1
        return  cls.nro

    def __init__(self):
        self.numero=Grupo.get_nro()
        self.generador = Generador(decimals=decimales, random=True)
        self.cola = False
        self.fin_ocupacion = 0
        self.cancha = None

    def __str__(self):
        return str(self.as_dict()) + '\n'

    @property
    def tiempo_ocupacion(self):
        pass

    @property
    def proxima_llegada(self):
        pass

    @property
    def estado(self):
        if self.cola:
            return "Esperando Cancha"
        elif self.cancha.acondicionando:
            return "Esperando Acondicionamiento"
        else:
            return "Jugando en cancha"

    def as_dict(self):
        return {
            'numero':self.numero,
            'estado':self.estado,
            'fin_ocupacion':self.fin_ocupacion,
        }

    @classmethod
    def resetear_lote(cls):
        cls.nro = 0

class GrupoFutbol(Grupo):
    def __init__(self, media, desviacion, media_llegada):
        super(GrupoFutbol, self).__init__(self)
        self.media_llegada = media_llegada
        self.media = media
        self.desviacion = desviacion

    @property
    def tiempo_ocupacion(self):
        return self.generador.box_muller_next(media=self.media, desviacion=self.desviacion)

    @property
    def proxima_llegada(self):
        return self.generador.exponencial_next(media=self.media_llegada)


class GrupoHandball(Grupo):
    def __init__(self, media, desviacion, media_llegada, desviacion_llegada):
        super(GrupoHandball, self).__init__(self)
        self.desviacion_llegada = desviacion_llegada
        self.media_llegada = media_llegada
        self.media = media
        self.desviacion = desviacion

    @property
    def tiempo_ocupacion(self):
        return self.generador.box_muller_next(media=self.media, desviacion=self.desviacion)

    @property
    def proxima_llegada(self):
        return self.generador.box_muller_next(media=self.media_llegada, desviacion=self.desviacion_llegada)

class GrupoBasquet(Grupo):
    def __init__(self, media, desviacion, media_llegada, desviacion_llegada):
        super(GrupoBasquet, self).__init__(self)
        self.desviacion_llegada = desviacion_llegada
        self.media_llegada = media_llegada
        self.media = media
        self.desviacion = desviacion

    @property
    def tiempo_ocupacion(self):
        return self.generador.box_muller_next(media=self.media, desviacion=self.desviacion)

    @property
    def proxima_llegada(self):
        return self.generador.box_muller_next(media=self.media_llegada, desviacion=self.desviacion_llegada)

if __name__ == '__main__':
    futbol = GrupoFutbol(1.30, 0.167, 10)
    handball = GrupoHandball(1.33, 0.33, 12, 2)
    basquet = GrupoBasquet(1.67, 0.5, 8, 2)
    