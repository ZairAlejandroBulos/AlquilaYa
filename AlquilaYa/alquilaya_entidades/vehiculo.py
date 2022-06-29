'''
    Clase Vehiculo
    @author Bulos
'''
# ------------------------------------------------------------------------------
class Vehiculo():

    '''
        Método Constructor.
    '''
    def __init__(self, clasificacion, marca, modelo, generacion, matricula, km, precio, estaAlquilado):
        self.__clasificacion = clasificacion
        self.__marca = marca
        self.__modelo = modelo
        self.__generacion = generacion
        self.__matricula = matricula
        self.__km = km
        self.__precio = precio
        self.__estaAlquilado = estaAlquilado

    '''
        Métodos Getters.
    '''
    def getClasificacion(self):
        return self.__clasificacion

    def getMarca(self):
        return self.__marca

    def getModelo(self):
        return self.__modelo

    def getGeneracion(self):
        return self.__generacion

    def getMatricula(self):
        return self.__matricula

    def getKm(self):
        return self.__km

    def getPrecio(self):
        return self.__precio

    def isEstaAlquilado(self):
        return self.__estaAlquilado

    '''
        Métodos Setters.
    '''
    def setClasificacion(self, clasificacion):
        self.__clasificacion = clasificacion

    def setMarca(self, marca):
        self.__marca = marca

    def setModelo(self, modelo):
        self.__modelo = modelo

    def setGeneracion(self, modeloAnio):
        self.__generacion = generacion

    def setMatricula(self, matricula):
        self.__matricula = matricula

    def serKm(self, km):
        self.__km = km

    def setPrecio(self, precio):
        self.__precio = precio

    def setEstaAlquilado(self, estaAlquilado):
        self.__estaAlquilado = estaAlquilado
