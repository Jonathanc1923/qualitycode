
from flask import Flask, render_template, request, redirect, url_for, send_file
import cv2
import insightface
import shutil
import os
from os import listdir
from os.path import isfile, join
from flask import jsonify
from tkinter import Tk, filedialog
import tempfile
from datetime import datetime
import random
from flask import session
from collections import defaultdict
from pathlib import Path
import string
import secrets
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime


app = Flask(__name__)
codigouser = None



a = 1


app.secret_key = secrets.token_hex(16)
print("insightface", insightface.__version__)


# Define la ruta al directorio de modelos buffalo_l
model_dir = os.path.join('archivos', '.insightface', 'models', 'buffalo_l')
os.environ['INSIGHTFACE_HOME'] = model_dir
model_dir = os.path.join('archivos')
# Crea una instancia de FaceAnalysis y evita la descarga automática del modelo
app_insightface = insightface.app.FaceAnalysis(name="buffalo_l", model_dir=model_dir, download=False, download_zip=False)
app_insightface.prepare(ctx_id=0, det_size=(640, 640))
swapper = insightface.model_zoo.get_model("inswapper_128.onnx", download=False, download_zip=False)


def generarnumero():
    global codigouser
    
    # Generar 3 números aleatorios
    numeros = ''.join(random.choices(string.digits, k=3))

    # Generar 4 letras aleatorias
    letras = ''.join(random.choices(string.ascii_uppercase, k=4))

    # Mezclar números y letras
    codigouser = ''.join(random.sample(numeros + letras, k=7))
    print ("CODIGOUSER", codigouser)
    

    return codigouser


#############################################################
    
# Diccionario para almacenar el número de veces que un código ha sido validado
codigos_validos = {
    
  'j3zqxl8k': 0, 'd5h1o9qs': 0, '4g6tjyma': 0, 'c2h4w1vb': 0, '3dn9se2w': 0,
  'x8nby5k2': 0, 't74brj6s': 0, 'fvq94g1d': 0, 'xhjw5nqz': 0, '0lg6n1ft': 0,
  'vdhn45mi': 0, 'ql0w6vtz': 0, 'syb9nkg2': 0, 'm8cgl7fd': 0, 'vns9c5jr': 0,
  '5hql9evj': 0, 'c61s2frz': 0, '2wkxgjfq': 0, 'p6jot3aw': 0, 'q45kihfy': 0,
  'ek42g5ms': 0, '1l5b7srw': 0, 'dj2kpg3i': 0, '45k9sjmw': 0, 'ztiq6yxk': 0,
  'ofvjyxwi': 0, 'mld1azp7': 0, '8x4g2zvp': 0, 'fbtlm9xq': 0, 'n5i0yohp': 0,
  'e0yjzt8p': 0, 'gsi1zrwf': 0,
  'dAGQ9iBe': 0, '9xSYtjYA': 0, 'rn09iIz6': 0, 'JyZ5XgNW': 0, 'K0BfbkQq': 0,
  'LgQoTiDd': 0, 'eYraplTb': 0, 'JKfogLmI': 0, 'zJqnxZur': 0, 'zyGAY3LD': 0,
  'LsZQ2P5x': 0, 'XLSV6Bcr': 0, '4MyM9D0c': 0, 'K7zysqgv': 0, '11ZjruqS': 0,
  'gshEhniS': 0, 'RchTGlgY': 0, 'vQgxJGyN': 0, 'PmqwSyIq': 0, 'xxHTM9v3': 0,
  'SDX9O9xj': 0, '8BRsgXHY': 0, 'HhIgKMyo': 0, 'WdSh516h': 0, 'xJSlepn6': 0,
  'P4GwEJZ3': 0, 'lpYDpXOw': 0, 'hXgWRdQA': 0, 'NHBRMHKM': 0, '3r8o0QRH': 0,
  'XG6nF87E': 0, '9KeAMnDn': 0, 'uAVGBNuG': 0, 'IAS3Ocyx': 0, '8R0acJIf': 0,
  'svif0syb': 0, 'jk4XRc3V': 0, 'wrRKuxyp': 0, 'i1eReTxw': 0, 'yFcmAOpr': 0,
  'rHACaa3T': 0, 'foIly2y0': 0, 'NzWJSx32': 0, 'XaPoN1jw': 0, 'RiPet1VT': 0,
  'ymUCGUTm': 0, 'n4RQTvXN': 0, '4CMXTlrG': 0, 'F6pTWfhF': 0, 'bCKBUrl3': 0,
  'Fxh85mFL': 0, 'rgfX8dMB': 0, 'HKuYB9Ly': 0, 'qm1jmQPC': 0, 'Lulb7QED': 0,
  'QTWOcg9m': 0, 'w9FShtZ0': 0, 'fC3DCkuF': 0, 'IrCtV56n': 0, 'Y9bOefeT': 0,
  'WJdcnVva': 0, 'cA3yRuhY': 0, 'Po2QHdGI': 0, '5I32xi7r': 0, 'mZVEposs': 0,
  'kIXdgJkv': 0, 'n6FRO43g': 0, 'tga53Hqi': 0, 'bb8CEKVC': 0, 'P1pQUMee': 0,
  'QkAiAqId': 0, '8JY6tbBz': 0, 'K2RkrBzv': 0, 'wgAxYLkj': 0, 'es3sMeC4': 0,
  '24FdmQiH': 0, 's2GEMsto': 0, 'jYYrGXQF': 0, 'V7lWB5iP': 0, 'T5QnQtxY': 0,
  'S1CRIW1g': 0, 'tiOh0GkL': 0, 'PoYks6GJ': 0, 'yRQBe1Gj': 0, 'Y87m8qZD': 0,
  'gpCKcWRA': 0, 'XsvAnXeU': 0, 'HyOfzNEM': 0, '0mC6MJq5': 0, 'RKVi6Jpc': 0,
  'qJIW2HVM': 0, 'V1tneUyL': 0, 'bhBInqJv': 0, 'JUCD8w4q': 0, 'zvcGqPJH': 0,
  'RjtFcpUA': 0, 'YBrnkOHl': 0, 'CGVynMZ4': 0, 'fb5SiQbD': 0, 'cTGw4EMd': 0, "tefiteamo":-1000,
  '2L1dnLef': 0, 'kHoUiBed': 0, 'AInuhwpu': 0, 'D77jdrmz': 0, 'gEcRlYlT': 0, 'S7nzKkVJ': 0, 'mXtj7fB3': 0, 'yu63nx8D': 0, 'P0elYQSJ': 0, '786q3bo1': 0, 'StHp2Kk0': 0, 'v42RFd42': 0, 'uKHlRhkx': 0, '0RQM5ygn': 0, 'ZxEFa9Ws': 0, 'tuH6O4Yr': 0, 'NtAL5ZmB': 0, '55MsweXe': 0, 'aIbkRVxs': 0, 'NOBBKeQE': 0, 'FCvW1246': 0, 'TOX3wesC': 0, 'Dfp90bCy': 0, 'DIoWyAmg': 0, 'PAzDfOlS': 0, 'Du4S7DOh': 0, 'ewF4x8tk': 0, '7iSoLWXP': 0, '2rLkvNZA': 0, '3vKxOxrB': 0, 'YjSb2aDe': 0, 'z8G1mBMN': 0, 'MADA7Ri7': 0, 'sBEgWgtQ': 0, 'pLueis4f': 0, 'ODYWWk78': 0, 'Z8kq1TTe': 0, 'BkokVzPj': 0, 'OewffCH7': 0, 'PrzNSwvz': 0, 'pTAICrw6': 0, 'szoyR5Vb': 0, 'T7ZZyK2p': 0, 'M2uE7RXX': 0, 'T7W1qZuA': 0, 'BJqzPiXJ': 0, 'Gs0fFpFb': 0, '7GTNp9GY': 0, 'apohUHP5': 0, 'Y2JgUCUA': 0, 'xhWBRQUu': 0, 'dZWXF1KF': 0, '31Reg4YY': 0, 'KZlVeOF4': 0, '4F7GE9Hz': 0, 'RCVmo5kp': 0, '8ZW1227u': 0, 'xpNv3ND2': 0, 'SiFbjGjf': 0, 'p4pZ57Ht': 0, 'qh55WNbP': 0, 'gpAsNzY7': 0, 'e6lrhFFo': 0, 'y4DM2lfp': 0, 'WKVRh87v': 0, 'DF2WwYiB': 0, 'c6JSzIwT': 0, 'yWwgPUe5': 0, 'S1PdZFmg': 0, 'MuiK6H2l': 0, 'pkqSFtyV': 0, 'C8m9uJ5q': 0, 'GsnICDKX': 0, 'OFmTMwzn': 0, '7Ewh5L1q': 0, 'PwaqszDb': 0, '0YWKtASR': 0, 'JONATm9D': 0, 'Z7n2AfR4': 0, 'cSZL94ee': 0, 'xU0GNfcs': 0, 'xuQaodNx': 0, 'FQFVPEae': 0, 'U8wEg70x': 0, 'z6TREyiD': 0, '9GrlBKeD': 0, 'clkMV3W2': 0, 'S6coUIYQ': 0, 'TLDZfoMy': 0, 'qffNYGOl': 0, 'zlbqsMmI': 0, 'nCGiaWXI': 0, '4yqjxmZf': 0, 'tCQDk6C7': 0, 'TpZlBRaX': 0, 'zrmDjCRK': 0, 'JvQcwsbP': 0, 'ZLBzyMjH': 0, 'A8XIHZMR': 0, 'BOIpiVwz': 0
  }
limite_validaciones = 16  # Establece el límite de validaciones permitidas

# Diccionario para almacenar la lista negra de códigos
lista_negra = defaultdict(int)

@app.route('/validar_codigo/<codigo>', methods=['GET'])
def validar_codigo(codigo):
    global codigos_validos, lista_negra

    codigouser = generarnumero()
    print ("MI CODIGOUSER ES", codigouser)
    session['user'] = codigouser
    session['codigouser'] = codigouser
    if os.path.join('uploads', codigouser):
        # Si el directorio existe, lo eliminamos.
        try:
            shutil.rmtree(os.path.join('uploads', codigouser))
            print(f"Carpeta eliminada exitosamente.")
        except OSError as e:
            print(f"No se pudo eliminar la carpeta . Error: {e}")
    else:
        print(f"La carpeta {os.path.join('uploads', codigouser)} no existe aun.")
    if codigo in codigos_validos:
        if codigos_validos[codigo] < limite_validaciones:
            # Incrementa el contador
            codigos_validos[codigo] += 1
            # Imprime el estado actual de la cuenta
            print(f"Código {codigo} validado {codigos_validos[codigo]} veces.")
            # Devuelve éxito
            return jsonify({'status': 'success', 'message': 'Código válido'})
        else:
            # Excede el límite de validaciones
            if codigo not in lista_negra:
                lista_negra[codigo] = 1
                # Imprime el estado actual de la cuenta
                print(f"Código {codigo} agregado a la lista negra.")
            return jsonify({'status': 'error', 'message': 'Código ha alcanzado el límite de validaciones'})
    else:
        # Código no válido
        return jsonify({'status': 'error', 'message': 'Código no válido'})






##########################################################################

def rename_images():
    
    
    codigouser = session['codigouser']
    # Obtén la lista de archivos en la carpeta
    ip_folder_path = os.path.join("uploads", codigouser)
    ip_folder_path = session['ip_folder_path']
    files = os.listdir(ip_folder_path)

    # Filtra solo los archivos de imagen (puedes ajustar las extensiones según tus necesidades)
    image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # Ordena los archivos por fecha de creación
    image_files.sort(key=lambda x: os.path.getctime(os.path.join(ip_folder_path, x)))

    # Recorre la lista de archivos y renombra cada uno con un número
    for i, file_name in enumerate(image_files, start=1):
        file_path = os.path.join(ip_folder_path, file_name)
        new_name = f"{i}{Path(file_name).suffix}"  # Nuevo nombre con número de orden y extensión
        new_path = os.path.join(ip_folder_path, new_name)
        os.rename(file_path, new_path)
        






@app.route('/static_images')
def static_images():
    estilos_path = os.path.join(app.static_folder, 'estilos')
    files = [f for f in os.listdir(estilos_path) if os.path.isfile(os.path.join(estilos_path, f))]
    return jsonify({'files': files})

def construir_imfondo(imagefilename):
    b = session["b"]
    static_dir = os.path.join('static')
    # Construir la ruta de la imagen de fondo en el directorio 'grandes'
    imfondo_path = os.path.join(static_dir, b, 'grandes', imagefilename)
    session ["imfondo_path"] = imfondo_path
    # Verificar si el archivo existe
    if not os.path.exists(imfondo_path):
        print(f"El archivo no existe en la ruta: {imfondo_path}")
        # Puedes manejar el error de alguna manera, por ejemplo, retornar None
        return None

    return imfondo_path



@app.route('/select_image', methods=['POST'])
def select_image():
    
    
    codigouser = session['codigouser']
    if 'user' in session:
    
        if 'file' not in request.files:
            return jsonify({'error': 'No se encontró ningún archivo'}), 400

        file = request.files['file']

        # 1. Obtener user del cliente
        user_address = codigouser

        # 2. Crear una subcarpeta con el nombre de la dirección IP si no existe
        ip_folder_path = os.path.join("uploads", user_address)
        session['ip_folder_path'] = ip_folder_path
        if not os.path.exists(ip_folder_path):
            os.makedirs(ip_folder_path)

        # 3. Guardar la imagen en la subcarpeta
        img_persona_path = os.path.join(ip_folder_path, file.filename)
        file.save(img_persona_path)
        print("SE GUARDÓ EN", img_persona_path)
        session['img_persona_path'] = img_persona_path
    
        return img_persona_path
    else:
        # El usuario no ha iniciado sesión, redirige al formulario de inicio de sesión
        return redirect(url_for('seleccion_estilo'))



@app.route('/check_a')
def check_a():
    global a
    if a == 1:
        return jsonify({'a': 1})
        
    else:
        return jsonify({'a': 0})
    

@app.route('/')
def seleccion():
    
    return redirect(url_for('seleccion_estilo'))








@app.route('/imagen_final', methods=['GET'])
def imagen_final():
    global a
    a = 1
    
    codigouser = session['codigouser']

    # Obtén la dirección IP del usuario
    user_ip = codigouser

    # Obtiene la lista de archivos en el directorio 'static'
    static_dir = 'static'
    files = [f for f in listdir(static_dir) if isfile(join(static_dir, f))]

    # Filtra los archivos que contienen el valor de 'user_ip'
    filtered_files = [f for f in files if user_ip in f]

    # Ordena la lista de archivos por fecha de modificación
    filtered_files.sort(key=lambda x: os.path.getmtime(os.path.join(static_dir, x)))

    # Toma el archivo más reciente de la lista (si hay alguno)
    if filtered_files:
        latest_file = filtered_files[-1]
        result_image_name = latest_file  # Solo el nombre del archivo
        result_image = os.path.join(static_dir, latest_file)
        return render_template('imagen_final.html', result_image=result_image_name)
    else:
        return "No cierres esta página - Recargue esta pagina en 30 segundos, Aún es muy pronto! No se encontraron imágenes para mostrar -  Estamos creando tus diseños!"
    
    
    
    
    
    
    
    
    
    
    
    
    

@app.route('/index', methods=['GET', 'POST'])
def index():
    global a
    result_image_path = None
    
     # Debes obtener el valor real de 'a' según tus necesidades

    result_image_path = None  # Inicializa la variable result_image_path fuera del bloque condicional

    if request.method == 'POST':
        # Lógica para manejar solicitudes POST
        imagefilename = request.form.get('imagefilename', '')
        print("Nombre de la imagen de fondo recibido en Flask:", imagefilename)
        imfondo_path = session ["imafondo_path"]
        imfondo_path = construir_imfondo(imagefilename)
        
        static_dir = os.path.join('static')
        image_files = [f for f in os.listdir(static_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]

        if image_files:
            last_image = max(image_files, key=lambda x: os.path.getctime(os.path.join(static_dir, x)))
            result_image_path = os.path.join('static', last_image)
        
            print("Result Image Path:", result_image_path)

        
        else:
            result_image_path = None
        imagen_final
        result_image=result_image_path
        session["result_image"] = result_image
        return render_template('index.html' ,a=a)

    # Lógica para manejar solicitudes GET
    imagefilename = str(request.args.get('imagefilename', ''))
    imfondo_path = construir_imfondo(imagefilename)
    return render_template('index.html', imfondo=imfondo_path)



@app.route('/seleccion_estilo')
def seleccion_estilo():
    return render_template('seleccion_estilo.html')






@app.route('/disenos_una_persona')
def disenos_una_persona():
    
    b = "individuales"
    session["b"] = b
    # Ruta a la carpeta de imágenes para 1 persona
    folder_path = os.path.join('static', "individuales", 'reducido')
    # Obtener la lista de nombres de archivos en la carpeta
    image_files = os.listdir(folder_path)
    # Construir la ruta completa para cada imagen
    image_paths = [filename for filename in image_files]
    imagefilename = request.args.get('imagefilename', '')
    imfondo_path = construir_imfondo(imagefilename)
    return render_template('galeria.html', image_paths=image_paths, imfondo=imfondo_path)

@app.route('/disenos2personas')
def disenos_una_persona2():
    
    
    b = "dobles"
    session["b"] = b
    # Ruta a la carpeta de imágenes para 1 persona
    folder_path = os.path.join('static', "dobles", 'reducido')
    # Obtener la lista de nombres de archivos en la carpeta
    image_files = os.listdir(folder_path)
    # Construir la ruta completa para cada imagen
    image_paths = [filename for filename in image_files]
    imagefilename = request.args.get('imagefilename', '')
    imfondo_path = construir_imfondo(imagefilename)
    return render_template('galeria2.html', image_paths=image_paths, imfondo=imfondo_path)

@app.route('/disenos3personas')
def disenos_una_persona3():
    
  
    b = "triples"
    session["b"] = b
    # Ruta a la carpeta de imágenes para 1 persona
    folder_path = os.path.join('static', "triples", 'reducido')
    # Obtener la lista de nombres de archivos en la carpeta
    image_files = os.listdir(folder_path)
    # Construir la ruta completa para cada imagen
    image_paths = [filename for filename in image_files]
    imagefilename = request.args.get('imagefilename', '')
    imfondo_path = construir_imfondo(imagefilename)
    return render_template('galeria3.html', image_paths=image_paths, imfondo=imfondo_path)



@app.route('/disenos4personas')
def disenos_una_persona4():
    
   
    b = "cuadruples"
    session["b"] = b
    # Ruta a la carpeta de imágenes para 1 persona
    folder_path = os.path.join('static', "cuadruples", 'reducido')
    # Obtener la lista de nombres de archivos en la carpeta
    image_files = os.listdir(folder_path)
    # Construir la ruta completa para cada imagen
    image_paths = [filename for filename in image_files]
    imagefilename = request.args.get('imagefilename', '')
    imfondo_path = construir_imfondo(imagefilename)
    return render_template('galeria4.html', image_paths=image_paths, imfondo=imfondo_path)

@app.route('/disenos5personas')
def disenos_una_persona5():
    
   
    b = "quintuples"
    session["b"] = b
    # Ruta a la carpeta de imágenes para 1 persona
    folder_path = os.path.join('static', "quintuples", 'reducido')
    # Obtener la lista de nombres de archivos en la carpeta
    image_files = os.listdir(folder_path)
    # Construir la ruta completa para cada imagen
    image_paths = [filename for filename in image_files]
    imagefilename = request.args.get('imagefilename', '')
    imfondo_path = construir_imfondo(imagefilename)
    return render_template('galeria5.html', image_paths=image_paths, imfondo=imfondo_path)




@app.route('/procesar', methods=['POST'])
def procesar():
   
    
    codigouser = session['codigouser']
    
    rename_images()
    data = request.get_json()
    imagefilename_from_form = data.get('imagefilename', '')
    
    imfondo_path = construir_imfondo(imagefilename_from_form)
    carpeta_destino = os.path.join("uploads", codigouser)
    imfondo_path = session["imfondo_path"]
    print("Ruta de la imagen de fondo:", imfondo_path)

    nombre_deseado = "imagenfondo"
    nombre_archivo = os.path.basename(imfondo_path)
    ruta_destino = os.path.join(carpeta_destino, f"{nombre_deseado}.txt")
    
    
    shutil.copy2(imfondo_path, ruta_destino)
    
    
    
    
    img = cv2.imread(imfondo_path)

    if img is None:
        print("Error al cargar la imagen.")
        return jsonify({'status': 'error', 'message': 'Error al cargar la imagen'})

    faces = app_insightface.get(img)
    user_ip = codigouser
    # Ordenar las caras por la posición del cuadro delimitador
    faces = sorted(faces, key=lambda x: x['bbox'][0])
    
    # Almacena los datos de los rostros en una lista
    folder_path = os.path.join('uploads', user_ip)
    # Obtener la lista de nombres de archivos ordenada
    file_names = sorted(os.listdir(folder_path))

    # Almacena los datos de los rostros en una lista
    faces_data = []
    faces_data.sort(key=lambda x: x['source_face']['bbox'][0])
    for i, source_face in enumerate(faces):
        bbox = source_face["bbox"]
        bbox = [int(b) for b in bbox]

        # Si hay un archivo correspondiente en la carpeta, usa su información
        if i < len(file_names):
            file_name = file_names[i]
            img_persona_path = os.path.join('uploads', user_ip, file_name)
        else:
            # En caso de que no haya suficientes archivos en la carpeta
            img_persona_path = None
        
        # Almacena los datos del rostro actual en la lista faces_data
        current_face_data = {
            'source_face': source_face,
            'img_persona_path': img_persona_path
        }
        faces_data.append(current_face_data)
    faces_data.sort(key=lambda x: os.path.basename(x['img_persona_path']))
    
    
    # Procesa los datos almacenados para generar las imágenes finales
    for i, face_data in enumerate(faces_data):
        source_face = face_data['source_face']
        img_persona_path = face_data['img_persona_path']
        
        img_persona = cv2.imread(img_persona_path)
        remp_faces = app_insightface.get(img_persona)
        remp_faces = remp_faces[0]
        img = swapper.get(img, source_face, remp_faces, paste_back=True)
        
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_number = str(random.randint(100000000, 999999999))
        
        print("Valor de user_ip:", user_ip)
        unique_name = f"output_image_{timestamp}_{random_number}_{user_ip}_{i}.jpg"
        
        
        print("Nombre de archivo único:", unique_name)
        output_path = os.path.join('static', unique_name)
        
    
        
        cv2.imwrite(output_path, img)
        print("UNIQUE NAME ES", unique_name)
        print(session)
    

    # Devuelve la última imagen generada como resultado
    unique_name = unique_name
    print ("dasdasfavaa", unique_name)
    result_image = output_path
    session['unique_name'] = unique_name
    session["result_image"] = result_image
    shutil.rmtree(os.path.join('uploads', codigouser))
    print(f"Carpeta eliminada exitosamente.")
    print(session)
    

    # Pasar la variable unique_number al template
    return render_template('imagen_final.html', result_image=unique_name, unique_name=unique_name)




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))










