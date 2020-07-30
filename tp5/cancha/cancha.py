from generador_pseudoaliatorio.generador import Generador
from grupo import Grupo,GrupoFutbol,GrupoHandball,GrupoBasquet

class Cancha:

    def __init__(self):
        self.generador = Generador(decimals=4, random=True)
        self.grupo_actual = None
        self.en_cancha = []
        self.en_cola_FutbolHandball = []
        self.en_colaBasquet = []
        self.acondicionando = False
        self.tiempo_acondicionado = 0

    def __str__(self):
        return str(self.as_dict()) + '\n'

    @property
    def estado(self):
        grupo = self.grupo_actual
        if self.acondicionando:
            return "Acondicionado"
        elif len(self.en_cancha)==0:
            return "Libre"
        else:
            if len(self.en_cancha)==1:
                if grupo.tipo == "Basquet":
                    return "Semi Ocupada"
                else:
                    return "Ocupada"
            else:
                return "Ocupada"

    def as_dict(self):
        return{
            'nombre': "Cancha",
            'estado': self.estado,
            'Cola 1': self.en_cola_FutbolHandball,
            'Cola 2': self.en_colaBasquet,
        }

    def asignar_grupo(self, grupo):
        self.grupo_actual = grupo
        self.en_cancha.append(grupo)

    def agregar_cola(self, grupo):
        if grupo.tipo == "Basquet":
            self.en_colaBasquet.append(grupo)
        else:
            self.en_cola_FutbolHandball.append(grupo)

    def agregar_grupo(self, grupo, reloj):
        estado = self.estado
        grupo.cancha = self
        if estado == "Libre":
            self.tiempo_acondicionado = self.acondicionar(grupo)
            self.asignar_grupo(grupo)
        elif estado == "Ocupada":
            self.agregar_cola(grupo)
        elif estado == "Semi Ocupada":
            #self.en_cancha.append(grupo)
            self.asignar_grupo(grupo)
        elif estado == "Acondicionando":
            if self.grupo_actual == grupo:
                grupo.fin_ocupacion = round(grupo.tiempo_ocupacion + reloj, 4)
                self.acondicionando = False
            else:
                self.agregar_cola(grupo)


    def acondicionar(self, grupo):
        self.acondicionando = True
        grupo.acondicionando = True
        #Calculo tiempo de acondicionado a mano
        if grupo.tipo == "Futbol":
            m_tipo_cancha = 60
            tiempo_acondicionamiento = 0.13
        elif grupo.tipo == "Handball":
            m_tipo_cancha = 90
            tiempo_acondicionamiento = 0.09
        elif grupo.tipo == "Basquet":
            m_tipo_cancha = 40
            tiempo_acondicionamiento = 0.18
        else:
            raise Exception("Erro tipo grupo")
        return tiempo_acondicionamiento
        # tiempo_acondicionamiento = self.calcular_acondicionamiento(m_tipo_cancha)

    #Para calcular ec dif
    """def calcular_acondicionamiento(self, m_tipo_cancha):
        h = 0.1
        t = 0
        wo = 25
        m = m_tipo_cancha
        while wo >= 0:
            dw = -0.2*m + 0.001*t - 1
            t = t + h
            w = wo + dw*h
            wo = w
        return round((t*4)/60, 4)
    """

if __name__ == '__main__':
    cancha = Cancha()
    futbol = GrupoFutbol(1.30, 0.167)
    handball = GrupoHandball(1.33, 0.33)
    basquet = GrupoBasquet(1.67, 0.5)
    basquet2 = GrupoBasquet(1.67, 0.5)
    cancha.agregar_grupo(basquet, 1.3)
    cancha.agregar_grupo(basquet2, 2.5)
    cancha.agregar_grupo(handball, 5.5)
    cancha.agregar_grupo(futbol, 8)
    print(cancha)
    print(basquet)
    print(basquet2)
    print(futbol)
    print(handball)