'''
    Interfaz Administrador para agregar Vehiculo
    @author Bulos
'''
# ------------------------------------------------------------------------------
from tkinter import Tk, Frame, Label, Button, Entry, ttk, messagebox

from alquilaya_entidades.vehiculo import Vehiculo
from alquilaya_servicios.vehiculoservicio import VehiculoServicio
from alquilaya_servicios.vehiculo_basedatos import agregarVehiculo, esVehiculoIngresado, mensajeAdvertencia
# ------------------------------------------------------------------------------
class VentanaAgregarVehiculo():

    '''
        Procedimiento para el Button Cancelar.
        Destuye la ventana actual.
    '''
    def actionCancelar(self):
        self.root.withdraw()

    '''
        Procedimiento que limpia la pantalla (Combobox y Entry).
    '''
    def limpiar(self):
        self.comboClasificacion.set("")
        self.comboMarca.set("")
        self.entryModelo.delete(0, "end")
        self.entryGeneracion.delete(0, "end")
        self.entryMatricula.delete(0, "end")
        self.entryKm.delete(0, "end")
        self.entryPrecio.delete(0, "end")

    '''
        Función que valida los campos ingresados.
        Coloca un Label a todos aquellos campos incorrectos.
        Retorna un bool.
    '''
    def validar(self):
        vs = VehiculoServicio()
        band = True

        # Validación Clasifiación
        if (vs.esStringVacio(self.comboClasificacion.get())):
            self.labelClasificacion["text"] = "Incorrecto"
            band = False
        else:
            self.labelClasificacion["text"] = ""

        # Validación Marca
        if (vs.esStringVacio(self.comboMarca.get())):
            self.labelMarca["text"] = "Incorrecto"
            band = False
        else:
            self.labelMarca["text"] = ""

        # Validación Modelo
        if (vs.esStringVacio(self.entryModelo.get()) or
            (not vs.esStringAlfaNumerico(self.entryModelo.get()))):
            self.labelModelo["text"] = "Incorrecto"
            band = False
        else:
            self.labelModelo["text"] = ""

        # Validación Generación
        if (not vs.esAnioValido(self.entryGeneracion.get())):
            self.labelGeneracion["text"] = "Incorrecto"
            band = False
        else:
            self.labelGeneracion["text"] = ""

        # Validación Matricula
        if (not vs.esMatricula(self.entryMatricula.get(), self.entryGeneracion.get())):
            self.labelMatricula["text"] = "Incorrecto"
            band = False
        else:
            self.labelMatricula["text"] = ""

        # Validación Kilómetros
        if (not vs.esDecimalPositivo(self.entryKm.get(), 320000)):
            self.labelKm["text"] = "Incorrecto"
            band = False
        else:
            self.labelKm["text"] = ""

        # Validación Precio
        if (not vs.esDecimalPositivo(self.entryPrecio.get(), 30000)):
            self.labelPrecio["text"] = "Incorrecto"
            band = False
        else:
            self.labelPrecio["text"] = ""

        return band

    '''
        Procedimiento para el Button Aceptar.
        Si la validacion es correcta, crea un Vehiculo y lo ingresa a la db, en
            caso contrario avisa mediante un mensaje.
    '''
    def actionAceptar(self):
        if (self.validar()):
            if (not esVehiculoIngresado(self.entryMatricula.get())):
                agregarVehiculo(Vehiculo(self.comboClasificacion.get(),
                    self.comboMarca.get(),
                    self.entryModelo.get(),
                    self.entryGeneracion.get(),
                    self.entryMatricula.get(),
                    self.entryKm.get(),
                    self.entryPrecio.get(),
                    False),
                    self.root)
                self.limpiar()
            else:
                mensajeAdvertencia("¡Error!",
                    "La matricula {} ya ha sido ingresada".format(self.entryMatricula.get().upper()),
                     self.root )
        else:
            mensajeAdvertencia("¡Error!", "No se pudo ingresar el vehículo. Revise los datos ingresados", self.root)

    '''
        Método Constructor.
    '''
    def __init__(self, root):
        # Ventana
        self.root = root
        screenWidth = root.winfo_screenwidth()                                  # Obtiene ancho del área de visualización.
        screenHeight = root.winfo_screenheight()                                # Obtiene altura del área de visualización.
        width = 600                                                             # Establece ancho de la ventana.
        height = 400                                                            # Establece altura de la ventana.
        left = (screenWidth - width) / 2
        top = (screenHeight - height) / 2
        self.root.geometry("%dx%d+%d+%d" % (width, height, left, top))          # Ancho x Alto + Desplazamiento x + Desplazamiento y
        self.root.title("Agregar Vehiculo")
        self.root.resizable(False, False)

        self.initComponents(root)

    '''
        Procedimiento que inicializa los componentes gráficos.
    '''
    def initComponents(self, root):
        # Frame
        frame1 = Frame(root, width="100", height="50")
        frame1.pack(expand=False, fill="both")

        frame2 = Frame(root, width="100", height="400")
        frame2.pack(expand=False, fill="both")

        # Label
        Label(frame1, text="Introducir los siguientes datos:", font=("Bahnschrift SemiLight", 20)).place(x=300, y=25, anchor="center")
        Label(frame2, text="CLASIFICACIÓN: ", font=("Bahnschrift Light", 10)).place(x=50, y=30)
        Label(frame2, text="MARCA: ", font=("Bahnschrift Light", 10)).place(x=50, y=70)
        Label(frame2, text="MODELO: ", font=("Bahnschrift Light", 10)).place(x=50, y=110)
        Label(frame2, text="GENERACIÓN: ", font=("Bahnschrift Light", 10)).place(x=50, y=150)
        Label(frame2, text="MATRICULA: ", font=("Bahnschrift Light", 10)).place(x=50, y=190)
        Label(frame2, text="KILÓMETROS: ", font=("Bahnschrift Light", 10)).place(x=50, y=230)
        Label(frame2, text="PRECIO DE ALQUILER: ", font=("Bahnschrift Light", 10)).place(x=50, y=270)

        # Label (Salida)
        self.labelClasificacion = Label(frame2, text="", fg="red")
        self.labelClasificacion.place(x=350, y=30)

        self.labelMarca = Label(frame2, text="", fg="red")
        self.labelMarca.place(x=350, y=70)

        self.labelModelo = Label(frame2, text="", fg="red")
        self.labelModelo.place(x=350, y=110)

        self.labelGeneracion = Label(frame2, text="", fg="red")
        self.labelGeneracion.place(x=350, y=150)

        self.labelMatricula = Label(frame2, text="", fg="red")
        self.labelMatricula.place(x=350, y=190)

        self.labelKm = Label(frame2, text="", fg="red")
        self.labelKm.place(x=350, y=230)

        self.labelPrecio = Label(frame2, text="", fg="red")
        self.labelPrecio.place(x=350, y=270)

        # Conmbobox
        self.comboClasificacion = ttk.Combobox(frame2, state="readonly",
            values=["SUV", "COUPE", "SEDAN", "PICKUP", "URBANO", "DEPORTIVO",
                    "FURGONETA", "TODOTERRENO", "DESCAPOTABLE", "MONOVOLUMEN"])
        self.comboClasificacion.place(x=200, y=30, height=24)

        self.comboMarca = ttk.Combobox(frame2, state="readonly",
            values=["FIAT","AUDI","BMW","FORD","NISSAN","TOYOTA","RENAULT",
                    "PEUGEOT", "PORSCHE","CHEVROLET","VOLKSWAGEN","MERCEDES-BENZ"])
        self.comboMarca.place(x=200, y=70, height=24)

        # Entry
        self.entryModelo = Entry(frame2, width=23)
        self.entryModelo.place(x=200, y=110, height=22)

        self.entryGeneracion = Entry(frame2, width=23)
        self.entryGeneracion.place(x=200, y=150, height=22)

        self.entryMatricula = Entry(frame2, width=23)
        self.entryMatricula.place(x=200, y=190, height=22)

        self.entryKm = Entry(frame2, width=23)
        self.entryKm.place(x=200, y=230, height=22)

        self.entryPrecio = Entry(frame2, width=23)
        self.entryPrecio.place(x=200, y=270, height=22)

        # Button
        Button(frame2, text="Cancelar", width=10, height=1, command=self.actionCancelar).place(x=400, y=315)
        Button(frame2, text="Aceptar", width=10, height=1, command=self.actionAceptar).place(x=500, y=315)

        root.mainloop()
