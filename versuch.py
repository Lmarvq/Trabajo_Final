import scipy.io as sio
import numpy as np

archivo = r"C:\Users\Daniel\Documents\DANIEL\udea\semestre3\Informatica 2\TallerpreQuiz2\E00001.mat"
archivo1 = r"C:\Users\Daniel\Documents\DANIEL\udea\semestre3\Informatica 2\quiz2prac\P005_EP_reposo.mat"
archivo2 = r"C:\Users\Daniel\Documents\DANIEL\udea\semestre3\Informatica 2\quiz2prac\S0539.mat"
# data = sio.loadmat(archivo)
# print(data)

def cargar_mat(file_path):
    try:
        mat_data = sio.loadmat(file_path)
        for key, value in mat_data.items():
            if isinstance(value, np.ndarray):
                print(f"Clave encontrada: {key}")
                return value
        raise ValueError("No se encontró ningún array en el archivo .mat")
    except Exception as e:
        print("Error al cargar el archivo .mat:", e)
        return None

# Ejemplo de uso
file_path = 'ruta/al/archivo.mat'
array = cargar_mat(archivo1)
if array is not None:
    print("Array cargado correctamente:", array)
else:
    print("No se pudo cargar el array")