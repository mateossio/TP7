from generador_pseudoaliatorio.generador import Generador
from generador_pseudoaliatorio.tabla import Tabla, Uniforme, Exponencial, Normal, Poisson


# Uniforme
def prueba_uniforme(random):
    gen = Generador(x=12, c=40, k=27, g=14, decimals=4, random=random)
    datos = gen.uniforme(a=0, b=10, n=25)
    tabla = Uniforme(num_intervalos=5, datos=datos, decimals=4)
    # tabla.chi_uniforme()
    tabla.prueba_de_bondad()
    print(tabla)
    tabla.histogram()

# Exponencial
def prueba_exponencial(random):
    gen = Generador(x=12, c=40, k=27, g=14, decimals=4, random=random)
    datos = gen.exponencial(lam=10, n=1000)
    tabla = Exponencial(num_intervalos=10, datos=datos, decimals=4)
    tabla.prueba_de_bondad()
    print(tabla)
    tabla.histogram()

# Normal
def prueba_normal(random, box=True):
    gen = Generador(x=12, c=40, k=27, g=14, decimals=4, random=random)
    datos = gen.normal(media=0, desviacion=1, n=1000, box=box)
    tabla = Normal(num_intervalos=10, datos=datos, decimals=4)
    tabla.prueba_de_bondad()
    print(tabla)
    tabla.histogram()

# Poisson
def prueba_poisson(random):
    gen = Generador(x=12, c=40, k=27, g=14, decimals=4, random=random)
    datos = gen.poisson(lam=1, n=1000)
    tabla = Poisson(datos=datos, decimals=4)
    tabla.prueba_de_bondad()
    print(tabla)
    tabla.histogram()


random = True
prueba_uniforme(random)
prueba_exponencial(random)
prueba_normal(random)
prueba_normal(random, box=False)
prueba_poisson(random)