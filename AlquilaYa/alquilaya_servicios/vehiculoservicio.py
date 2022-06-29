'''
    Clase Servicio para Vehiculo
    @author Bulos
'''
# ------------------------------------------------------------------------------
import datetime
# ------------------------------------------------------------------------------
class VehiculoServicio():

    '''
        Función que valida si una cadena esta vacía.
        Retorna un bool.
    '''
    def esStringVacio(self, cadena):
        return (cadena.isspace() or cadena == "")

    '''
        Función que valida si una cadena es alfanumerica.
        Retorna un bool.
    '''
    def esStringAlfaNumerico(self, cadena):
        return cadena.isalnum()

    '''
        Función que valida que un número entero sea positivo.
        Retorna un bool.
    '''
    def esEnteroPositivo(self, numero):
        try:
            numero = int(numero)
        except ValueError:
            return False
        else:
            return numero > 1

    '''
        Función que valida que un número decimal sea positivo.
        Retorna un bool.
    '''
    def esDecimalPositivo(self, numero, maximo):
        try:
            numero = float(numero)
        except ValueError:
            return False
        else:
            return (numero > 1.0) and (numero < maximo)

    '''
        Función que valida que el año ingresado no sea mayor al año actual.
        Retorna un bool
    '''
    def esAnioValido(self, numero):
        currentDateTime = datetime.datetime.now()
        fecha = currentDateTime.date()
        anio = fecha.strftime("%Y")

        return self.esEnteroPositivo(numero) and numero <= anio

    '''
        Función que valida que una cadena sea del tipo 'AAA111' o 'AA111AA'
        Retorna un bool.
    '''
    def esMatricula(self, cadena, generacion):
        cadena = cadena.replace(" ", "")

        if(self.esEnteroPositivo(generacion)):
            if(int(generacion) >= 2016):
                if(len(cadena) == 7):
                    return (cadena[0:2].isalpha() and cadena[2:5].isdigit() and cadena[5:].isalpha())
            else:
                if(len(cadena) == 6):
                    return (cadena[0:3].isalpha() and cadena[3:].isdigit())
        return False

    '''
        Función que valida la edicion de kilometros de un Vehiculo.
        Retorna un bool.
    '''
    def validarEditKilometros(self, km, kmActuales):
        return (self.esDecimalPositivo(kmActuales, 320000)) and (kmActuales > km)
