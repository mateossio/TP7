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

    def __str__(self):
        return str(self.as_dict()) + '\n'

    @property
    def estado(self):
        grupo = self.grupo_actual
        if self.acondicionando:
            return "Siendo Acondicionada"
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

    def agregar_grupo(self, grupo):
        estado = self.estado
        if estado == "Libre":
            self.asignar_grupo(grupo)
        elif estado == "Ocupada":
            self.agregar_cola(grupo)
        elif estado == "Semi Ocupada":
            self.en_cancha.append(grupo)

if __name__ == '__main__':
    cancha = Cancha()
    futbol = GrupoFutbol(1.30, 0.167, 10)
    handball = GrupoHandball(1.33, 0.33, 12, 2)
    basquet = GrupoBasquet(1.67, 0.5, 8, 2)
    basquet2 = GrupoBasquet(1.67, 0.5, 8, 2)
    cancha.agregar_grupo(basquet)
    cancha.agregar_grupo(basquet2)
    cancha.agregar_grupo(handball)
    cancha.agregar_grupo(futbol)
    print(cancha)
    print(basquet)
    print(basquet2)
    print(futbol)
    print(handball)