'''
    Contiene metodos para el ingreso y obtencion del usuario
    @author Araya
'''
# ------------------------------------------------------------------------------
import sqlite3
import interfaces.iUsuario
from interfaces.ESTANDARES import *
from entidades.usuario import Usuario

'''
AGREGAR USUARIO
'''
def agregar_usuario(usuario, imagen):
        try:
            consulta = "INSERT INTO Usuarios VALUES(?, ?, ?, ?, ?, ?, ?)"
            from servicios.reconocimientoFacial import convertirABinario
            imagenBinario = convertirABinario(imagen)
            if(imagenBinario != 0):
                print(usuario.getNombre(),usuario.getApellido(),usuario.getCarnetConducir(),usuario.getFechaNacimiento(),usuario.getCorreo(),usuario.getCuil())
                parametros = (usuario.getNombre(),usuario.getApellido(),usuario.getCarnetConducir(),usuario.getFechaNacimiento(),usuario.getCorreo(),usuario.getCuil(), imagenBinario)

                resultado = ejecutar_consulta(consulta, parametros)

                if (resultado != None):
                    MENSAJE_INFO("EL USUARIO FUE GUARDADO EN LA BASE DE DATOS ", visible)

            else:
                MENSAJE_INFO("Return 0, it won't save the user.", visible)
        except Exception:
            pass

'''
PETICION A LA BASE DE DATOS
'''
def ejecutar_consulta(consulta, parametros = ()):

    try:
        with sqlite3.connect(direccion_base_datos) as conn:
            cursor = conn.cursor()
            resultado = cursor.execute(consulta, parametros)
            conn.commit()
    except sqlite3.OperationalError:
        MENSAJE_INFO("No se pudo acceder a la base de datos!")
    return resultado

'''
    Función para obtener la imágen de la base de datos.
    Retorna un bool.
    @author Bulos
'''
def obtener_usuario(cuil, path):
    from servicios.reconocimientoFacial import escribirArchivo
    consulta = "SELECT * FROM Usuarios WHERE Cuil = ?"

    try:
        with sqlite3.connect(direccion_base_datos) as conn:
            cursor = conn.cursor()
            cursor.execute(consulta, (cuil,))

            if (results:= cursor.fetchone()) is not None:
                for result in results:
                    escribirArchivo(results[6], path)
                    return 1
    except sqlite3.OperationalError:
        return 0
