import os
import shutil
import cv2
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog
import zipfile

# Cambiar al directorio deseado
target_directory = "D:/blinkear"  # Cambia la ruta según tu preferencia
os.chdir(target_directory)

# Eliminar el directorio CodeFormer si existe
if os.path.exists("CodeFormer"):
    shutil.rmtree("CodeFormer")

# Clonar el repositorio
os.system("git clone https://github.com/Jonathanc1923/mejoradorhd.git")
os.chdir("CodeFormer")

# Instalar las dependencias de Python
os.system("pip install -r requirements.txt")

# Instalar basicsr
os.system("python basicsr/setup.py develop")

# Descargar el modelo preentrenado
os.system("python scripts/download_pretrained_models.py facelib")
os.system("python scripts/download_pretrained_models.py CodeFormer")

# Crear directorio de carga
upload_folder = 'inputs/user_upload'
os.makedirs(upload_folder, exist_ok=True)

# Usar tkinter para seleccionar archivos
root = Tk()
root.withdraw()  # Ocultar la ventana principal de tkinter

# Sube tus propias imágenes (puedes seleccionar manualmente en tu máquina)
uploaded_files = filedialog.askopenfilenames(
    title="Seleccione archivos",
    filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.bmp")]
)

for file_path in uploaded_files:
    filename = os.path.basename(file_path)
    dst_path = os.path.join(upload_folder, filename)
    print(f'Moviendo {filename} a {dst_path}')
    shutil.copy(file_path, dst_path)
    print(f'Archivo movido con éxito a: {dst_path}')

root.destroy()  # Cerrar la ventana de tkinter

# Visualizar resultados (preview)
input_folder = 'inputs/user_upload'
result_folder = 'results/user_upload_final/final_results'

# Asumiendo que CODEFORMER_FIDELITY está definido en algún lugar
# Puedes ajustar la ruta según tus necesidades
result_folder_with_fidelity = f'results/user_upload_{CODEFORMER_FIDELITY}/final_results'

input_list = sorted(os.listdir(input_folder))
for filename in input_list:
    input_path = os.path.join(input_folder, filename)
    img_input = cv2.imread(input_path)

    basename = os.path.splitext(filename)[0]
    output_path = os.path.join(result_folder_with_fidelity, f'{basename}.png')
    img_output = cv2.imread(output_path)

    # Visualizar las imágenes
    fig, axes = plt.subplots(1, 2, figsize=(25, 10))
    axes[0].imshow(cv2.cvtColor(img_input, cv2.COLOR_BGR2RGB))
    axes[0].set_title('Input', fontsize=16)
    axes[0].axis('off')

    axes[1].imshow(cv2.cvtColor(img_output, cv2.COLOR_BGR2RGB))
    axes[1].set_title('CodeFormer', fontsize=16)
    axes[1].axis('off')

    plt.show()

# Crear el archivo zip
zip_filename = 'results.zip'
zip_path = os.path.join('results', zip_filename)

with zipfile.ZipFile(zip_path, 'w') as zip_file:
    for foldername, subfolders, filenames in os.walk(result_folder):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            arcname = os.path.relpath(file_path, result_folder)
            zip_file.write(file_path, arcname)

# Descargar el archivo zip
try:
    from IPython.display import FileLink
    display(FileLink(zip_path))
except ImportError:
    print(f'Descarga manual: {zip_path}')
