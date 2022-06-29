'''
    Métodos de Servicio para Reconocimiento Facial
    @author Bulos
'''
# ------------------------------------------------------------------------------
import os
import cv2
from matplotlib import pyplot as plt
from mtcnn.mtcnn import MTCNN
from entidades.usuario import Usuario
from servicios.vehiculoservicio_basedatos import mensajeInfo, mensajeError
from servicios.usuarioservicios_basedatos import agregar_usuario, obtener_usuario
# ------------------------------------------------------------------------------
'''
    Función que convierte una imágen a formato binario.
'''
def convertirABinario(filename):
    try:
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData
    except:
        return 0

'''
    Función que convierte de formato binario a imágen.
'''
def escribirArchivo(data, path):
    with open(path, 'wb') as file:
        file.write(data)
# --------------------------------REGISTRO--------------------------------------
'''
    Procedimiento que detecta el rostro de la imágen.
'''
def rostro(img, faces):
    data = plt.imread(img)
    for i in range(len(faces)):
        x1, y1, ancho, alto = faces[i]["box"]
        x2, y2 = x1 + ancho, y1 + alto
        plt.subplot(1,len(faces), i + 1)
        plt.axis("off")
        face = cv2.resize(data[y1:y2, x1:x2],(150,200), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(img, face)
        plt.imshow(data[y1:y2, x1:x2])

'''
    Procedimiento que llama al método para cargar el usuario a la base de datos.
    Envía un Usuario y la imágen (ya convertida en binario).
'''
def registrarUsuario(usuario, img):
    path = os.getcwd().replace("\\", "/") + "/"
    agregar_usuario(usuario, path + img)

    os.remove(img)
'''
    Procedimiento que captura la imágen de registro.
'''
def capturarImagenRegistro(usuario):
    cap = cv2.VideoCapture(0)       #Windows
    #cap = cv2.VideoCapture(0)      #Linux
    user_reg_img = usuario.getCuil()
    img = f"{user_reg_img}.jpg"

    while True:
        ret, frame = cap.read()
        cv2.imshow("Registro Facial", frame)
        if cv2.waitKey(1) == 27:
            break

    cv2.imwrite(img, frame)
    cap.release()
    cv2.destroyAllWindows()

    pixels = plt.imread(img)
    faces = MTCNN().detect_faces(pixels)
    rostro(img, faces)
    registrarUsuario(usuario, img)
# --------------------------------LOGIN-----------------------------------------
'''
    Función para obtener la compatibilidad entre imágenes.
'''
def compatibilidad(img1, img2):
    orb = cv2.ORB_create()

    kpa, dac1 = orb.detectAndCompute(img1, None)
    kpa, dac2 = orb.detectAndCompute(img2, None)

    comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    matches = comp.match(dac1, dac2)

    similar = [x for x in matches if x.distance < 70]
    if len(matches) == 0:
        return 0
    return len(similar)/len(matches)

'''
    Procedimiento para capturar imágen de login.
'''
def capturarImagenIngreso(cuil):
    cap = cv2.VideoCapture(0)       #Windows
    #cap = cv2.VideoCapture(0)      #Linux
    user_login = cuil
    img = f"{user_login}_login.jpg"                                             # Imágen que capturamos
    img_user = f"{user_login}.jpg"                                              # Imágen que recuperamos de la db

    while True:
        ret, frame = cap.read()
        cv2.imshow("Login Facial", frame)
        if cv2.waitKey(1) == 27:
            break

    cv2.imwrite(img, frame)
    cap.release()
    cv2.destroyAllWindows()

    pixels = plt.imread(img)
    faces = MTCNN().detect_faces(pixels)

    rostro(img, faces)

    path = os.getcwd().replace("\\", "/") + "/"
    res_db = obtener_usuario(user_login, path + img_user)
    if(res_db):
        my_files = os.listdir()
        if (img_user in my_files):
            face_reg = cv2.imread(img_user, 0)
            face_log = cv2.imread(img, 0)

            comp = compatibilidad(face_reg, face_log)

            if (comp >= 0.94):
                mensajeInfo("¡Éxito!", "Bienvenido", None)
                os.remove(img)
                os.remove(img_user)
                return 1
            else:
                mensajeError("¡Error!", "No se ha encontrado coincidencia entre las imágenes")
                os.remove(img)
                os.remove(img_user)
                return 0

        else:
            mensajeError("¡Error!", "Usuario no encontrado")
            os.remove(img)
            os.remove(img_user)
            return 0
    else:
        mensajeError("¡Error!", "Usuario no encontrado")
        os.remove(img)
        os.remove(img_user)
        return 0
