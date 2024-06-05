import mysql.connector
import mysql.connector.cursor
import numpy as np
import scipy.io as sio

# Hola


class DataAccesObject:
    def __init__(self, data=None) -> None:
        self.__host = ""
        self.__usuario = ""
        self.__password = ""
        self.conexion = None
        self.pacientes = {}
        if data is not None:
            self.asignarDatos(data)
        else:
            self.data = []
            self.canales = 0
            self.puntos = 0

    def cargar_mat(self, file_path):
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

    def asignarDatos(self, data):
        self.data = data  # Matriz 2D
        self.canales = data.shape[0]  # 8 canales
        self.puntos = data.shape[1]  # 360000 puntos

    def devolver_segmento(self, x_min, x_max):
        if x_min >= x_max:
            return None
        return self.data[:, x_min:x_max]

    def escalar_senal(self, x_min, x_max, escala):
        if x_min >= x_max:
            return None
        copia_data = self.data[:, x_min:x_max].copy()
        return copia_data * escala

    def promedio(self, c, xmax, xmin):
        return np.mean(self.data[c, xmin:xmax], 0)

    def set_parametros_conexion(self, host, usuario, password):
        self.__host = host
        self.__usuario = usuario
        self.__password = password

    def conectarDB(self):
        try:
            self.conexion = mysql.connector.connect(
                host=self.__host, user=self.__usuario, password=self.__password
            )
            self.conexion.cursor().execute("USE PruebaLOGIN")
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def cerrarDB(self):
        if self.conexion:
            self.conexion.close()

    def crear_DB(self):
        if self.conectarDB():
            cursor = self.conexion.cursor()
            try:
                cursor.execute("CREATE DATABASE IF NOT EXISTS PruebaLOGIN")
                cursor.execute("USE PruebaLOGIN")
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS Usuarios (
                        ID int AUTO_INCREMENT PRIMARY KEY AUTO_INCREMENT,
                        Usuario VARCHAR(60) UNIQUE,
                        Password VARCHAR(60)
                    )
                """
                )
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS Pacientes (
                        Nombre VARCHAR(60),
                        Cedula int PRIMARY KEY,
                        Ruta VARCHAR(200)
                    )
                """
                )
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS Imagenes (
                        ID_cedula int PRIMARY KEY,
                        FOREIGN KEY(ID_Cedula) REFERENCES Pacientes(Cedula),
                        Ruta VARCHAR(200)
                    )
                """
                )
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS Biosenales (
                        ID_Cedula int PRIMARY KEY,
                        FOREIGN KEY(ID_Cedula) REFERENCES Pacientes(Cedula),
                        Ruta VARCHAR(200)
                    )
                """
                )
                self.conexion.commit()
                return True
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                return False
            finally:
                cursor.close()
                self.cerrarDB()
        return False

    def set_usuario(self, u, p):
        if self.conectarDB():
            cursor = self.conexion.cursor()
            try:
                query = "INSERT INTO Usuarios (Usuario, Password) VALUES (%s, %s)"
                cursor.execute(query, (u, p))
                self.conexion.commit()
                # cursor.execute("""GRANT ALL PRIVILEGES ON DB* TO %s@'localhost' WITH GRANT OPTION;""", tupla)
                return True
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                return False
            finally:
                cursor.close()
                self.cerrarDB()
        return False

    def validar_usuario(self, u, p):
        if self.conectarDB():
            cursor = self.conexion.cursor()
            try:
                query = "SELECT * FROM Usuarios WHERE Usuario = %s AND Password = %s"
                cursor.execute(query, (u, p))
                if cursor.fetchone():
                    return True
                return False
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                return False
            finally:
                cursor.close()
                self.cerrarDB()
        return False

    def obtener_pacientes(self):
        if self.conectarDB():
            cursor = self.conexion.cursor(
                dictionary=True
            )  # Esto hará que el cursor devuelva los resultados como diccionarios
            try:
                cursor.execute("SELECT * FROM Pacientes")
                resultados = cursor.fetchall()
                return resultados
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                return []
            finally:
                cursor.close()
                self.cerrarDB()
        return []

    def agregar_paciente(self, nombre, cedula, ruta):
        if self.conectarDB():
            cursor = self.conexion.cursor()
            try:
                cursor.execute("USE PruebaLOGIN")
                cursor.execute(
                    "INSERT INTO Pacientes (Nombre, Cedula, Ruta) VALUES (%s, %s, %s)",
                    (nombre, cedula, ruta),
                )
                self.conexion.commit()
                return True
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                return False
            finally:
                cursor.close()
                self.cerrarDB()
        return False

    def eliminar_paciente(self, cedula_paciente):
        if self.conectarDB():
            cursor = self.conexion.cursor()
            try:
                cursor.execute("USE PruebaLOGIN")
                cursor.execute(
                    "DELETE FROM Pacientes WHERE Cedula = %s", (cedula_paciente,)
                )
                self.conexion.commit()
                return True
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                return False
            finally:
                cursor.close()
                self.cerrarDB()
        return False

    def editar_paciente(self, nombre, ruta, cedula):
        if self.conectarDB():
            cursor = self.conexion.cursor()
            try:
                cursor.execute("USE PruebaLOGIN")
                cursor.execute(
                    "UPDATE Pacientes SET Nombre = %s, Ruta = %s WHERE Cedula = %s",
                    (nombre, ruta, cedula),
                )
                self.conexion.commit()
                return True
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                return False
            finally:
                cursor.close()
                self.cerrarDB()
        return False

    def obtener_biosenal(self, cedula):
        if self.conectarDB():
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Biosenales WHERE ID_Cedula = %s", (cedula,))
            resultado = cursor.fetchone()
            cursor.close()
            self.cerrarDB()
            return resultado
        
    def agregar_bioseñal(self, cedula, ruta):
        if self.conectarDB():
            cursor = self.conexion.cursor()
            try:
                query = "INSERT INTO Biosenales (ID_Cedula, Ruta) VALUES (%s, %s)"
                cursor.execute(query, (cedula, ruta))
                self.conexion.commit()
                return True
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                return False
            finally:
                cursor.close()
                self.cerrarDB()
        return False

    def agregar_imagen(self, cedula, ruta):
        if self.conectarDB():
            cursor = self.conexion.cursor()
            try:
                query = "INSERT INTO Imagenes (ID_Cedula, Ruta) VALUES (%s, %s)"
                cursor.execute(query, (cedula, ruta))
                self.conexion.commit()
                return True
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                return False
            finally:
                cursor.close()
                self.cerrarDB()
        return False
