from vistaPOO import *
from modeloPOO import *
import sys

class Coordinador:
    def __init__(self, vista, modelo) -> None:
        self.__miVista = vista
        self.__miModelo = modelo

    def agregarUsuario(self, u, p):
        return self.__miModelo.set_usuario(u, p)

    def validarUsuario(self, u, p):
        return self.__miModelo.validar_usuario(u, p)
    
    def obtenerPacientes(self):
        return self.__miModelo.obtener_pacientes()
    
    def agregarPaciente(self, nombre, cedula, ruta):
        return self.__miModelo.agregar_paciente(nombre, cedula, ruta)

    def eliminarPaciente(self, cedula_paciente):
        return self.__miModelo.eliminar_paciente(cedula_paciente)

    def editarPaciente(self, nombre, cedula):
        return self.__miModelo.editar_paciente(self, nombre, cedula)
    
    def recibirSenal(self, cedula):
        return self.__miModelo.obtener_biosenal(cedula)

    def recibirDatosSenal(self,data):
        self.__miModelo.asignarDatos(data)
    def devolverDatosSenal(self, x_min, x_max):
        return self.__miModelo.devolver_segmento(x_min, x_max)
    
    def escalarSenal(self,x_min,x_max, escala):
        return self.__miModelo.escalar_senal(x_min, x_max, escala)

    def calcularProm(self):
        self.__miModelo.promedio()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    miVista = VentanaLogin()
    miModelo = DataAccesObject()
    miModelo.set_parametros_conexion('localhost', 'root', 'daniel1305')
    miModelo.crear_DB()
    miCoordinador = Coordinador(miVista, miModelo)
    miVista.setControlador(miCoordinador)

    sys.exit(app.exec())
