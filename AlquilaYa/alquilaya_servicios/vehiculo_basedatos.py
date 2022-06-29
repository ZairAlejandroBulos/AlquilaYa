'''
    Métodos de Servicio para Vehiculo (Base de Datos)
    @author Bulos
'''
# ------------------------------------------------------------------------------
import sqlite3

from alquilaya_entidades.vehiculo import Vehiculo
from alquilaya_servicios.vehiculoservicio import VehiculoServicio
from tkinter import Toplevel, Label, Entry, Button, StringVar, messagebox
# ------------------------------------------------------------------------------
'''
    Función para consulta a base de datos.
'''
def ejecutarConsulta(consulta, parametros=()):
    dbNombre = "alquilaya_database/database.db"

    try:
        with sqlite3.connect(dbNombre) as conn:
            cursor = conn.cursor()
            result = cursor.execute(consulta, parametros)
            conn.commit()
    except sqlite3.OperationalError:
        mensajeError("¡Error!", "No se pudo ingresar a la base de datos")
    else:
        return result

'''
    Procedimiento que obtiene los vehiculos de la base de datos.
'''
def obtenerVehiculos(tree):
    elementos = tree.get_children()
    for elemento in elementos:
        tree.delete(elemento)

    consulta = "SELECT * FROM vehiculos"
    vehiculos = ejecutarConsulta(consulta, ())

    if (vehiculos != None):
        for vehiculo in vehiculos:
            if (vehiculo[7] == 0):
                values = (vehiculo[1], vehiculo[2], vehiculo[3], vehiculo[4], vehiculo[5], vehiculo[6], "No")
            else:
                values = (vehiculo[1], vehiculo[2], vehiculo[3], vehiculo[4], vehiculo[5], vehiculo[6], "Si")
            tree.insert("", 0, text=vehiculo[0], values=values)

'''
    Procedimiento que ingresa un Vehiculo a la base de datos.
'''
def agregarVehiculo(vehiculo, root):
    consulta = "INSERT INTO vehiculos VALUES(?, ?, ?, ?, ?, ?, ?, ?)"
    parametros = (vehiculo.getClasificacion(),
        vehiculo.getMarca(),
        vehiculo.getModelo().upper(),
        vehiculo.getGeneracion(),
        vehiculo.getMatricula().replace(" ", "").upper(),
        vehiculo.getKm(),
        vehiculo.getPrecio(),
        vehiculo.isEstaAlquilado())
    result = ejecutarConsulta(consulta, parametros)
    if (result != None):
        mensajeInfo("¡Éxito!", "Se ha añadido el vehículo exitosamente", root)

'''
    Procedimiento que elimina un Vehiculo de la base de datos.
'''
def eliminarVehiculo(tree, root):
    try:
        matricula = tree.item(tree.selection())["values"][3]
    except IndexError:
        mensajeAdvertencia("¡Error!", "Debe seleccionar un vehículo para eliminar", root)
    else:
        consulta = "DELETE FROM vehiculos WHERE matricula = ?"
        result = ejecutarConsulta(consulta, (matricula, ))
        if (result != None):
            mensajeInfo("¡Éxito!", "Se ha eliminado el vehículo {}".format(matricula), root)
        obtenerVehiculos(tree)

'''
    Función que valida si un Vehiculo ya se ha ingresado.
    La verificación se realiza por matricula.
    Retorna un bool.
'''
def esVehiculoIngresado(matricula):
    consulta = "SELECT * FROM vehiculos"
    vehiculos = ejecutarConsulta(consulta, ())

    for vehiculo in vehiculos:
        if (vehiculo[4] == matricula.upper()):
            return True

    return False

'''
    Procedimiento que edita un Vehiculo.
    La modificación es sobre los atributos kilometros y precio.
'''
def editarVehiculo(tree, root):
    try:
        km = tree.item(tree.selection())["values"][4]
        precio = tree.item(tree.selection())["values"][5]
    except IndexError:
        mensajeAdvertencia("¡Error!", "Debe seleccionar un vehículo para editar", root)
    else:
        ventanaEdit(km, precio)

'''
    Procedimiento que crea una ventana para ingresar los datos a modificar.
'''
def ventanaEdit(km, precio):
    root = Toplevel()
    root.title("Editar Vehiculo")
    root.geometry("350x250")
    root.resizable(False, False)

    # Label
    Label(root, text="Kilometros anteriores:").place(x=10,y=10)
    Label(root, text="Kilometros actuales:").place(x=10,y=50)
    Label(root, text="Precio anterior:").place(x=10,y=90)
    Label(root, text="Precio actual:").place(x=10,y=130)

    # Label (Salida)
    labelKm = Label(root, text="", fg="red")
    labelKm.place(x=275, y=50)
    labelPrecio = Label(root, text="", fg="red")
    labelPrecio.place(x=275, y=130)

    # Entry
    Entry(root, textvariable=StringVar(root, km), state="readonly").place(x=150, y=10)
    kmIngresados = Entry(root)
    kmIngresados.place(x=150, y=50)
    Entry(root, textvariable=StringVar(root, precio), state="readonly").place(x=150, y=90)
    precioIngresado = Entry(root)
    precioIngresado.place(x=150, y=130)

    # Button
    Button(root, text="Aceptar", command=lambda: validarEdit(root,
        km, precio, kmIngresados, precioIngresado, labelKm, labelPrecio)
        ).place(x=275, y=200)

'''
    Procedimiento que valida los datos ingresados en la ventanaEdit.
    Si la validacion es correcta modifica el Vehiculo en la base de datos.
'''
def validarEdit(root, km, precio, kmIngresados, precioIngresado, labelKm, labelPrecio):
    vs = VehiculoServicio()
    band = True

    # Validación Kilómetros
    if (not vs.validarEditKilometros(km, kmIngresados.get())):
        labelKm["text"] = "Incorrecto"
        band = False
    else:
        labelKm["text"] = ""

    # Validación Precio
    if (not vs.esDecimalPositivo(precioIngresado.get(), 30000)):
        labelPrecio["text"] = "Incorrecto"
        band = False
    else:
        labelPrecio["text"] = ""

    if (band):
        consulta = "UPDATE vehiculos SET kilometros = ?, precio = ? WHERE kilometros = ? AND precio = ?"
        parametros = (kmIngresados.get(), precioIngresado.get(), km, precio)
        result = ejecutarConsulta(consulta, parametros)
        if (result != None):
            mensajeInfo("¡Éxito!", "El vehiculo ha sido modificado exitosamente", root)
    else:
        mensajeAdvertencia("¡Error!", "No se pudo modificar el vehiculo. Revise los datos ingresados", root)

'''
    Procedimiento para mostrar un cuadro de diálogo de información.
'''
def mensajeInfo(titulo, mensaje, root):
    messagebox.showinfo(title=titulo, message=mensaje, parent=root)

'''
    Procedimiento para mostrar un cuadro de diálogo de advertencia.
'''
def mensajeAdvertencia(titulo, mensaje, root):
    messagebox.showwarning(title=titulo, message=mensaje, parent=root)

'''
    Procedimiento para mostrar un cuadro de diálogo de error.
'''
def mensajeError(titulo, mensaje):
    messagebox.showerror(title=titulo, message=mensaje)
