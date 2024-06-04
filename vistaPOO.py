from PyQt6.QtWidgets import *
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.uic import loadUi

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from numpy.core.numerictypes import *
import scipy.io as sio
import numpy as np
import pyqtgraph as pg

class VentanaLogin(QWidget):
    def __init__(self):
        super().__init__()
        self.__miControlador = None
        self.raiseUI()

    def setControlador(self, c):
        self.__miControlador = c

    def raiseUI(self):
        self.setGeometry(100, 100, 450, 350)
        self.setWindowTitle("Login principal")
        self.raiseFormularioLogin()
        self.show()

    def raiseFormularioLogin(self):
        #USUARIO
        user_label = QLabel(self)
        user_label.setText('Usuario: ')
        user_label.setFont(QFont('Arial', 10))
        user_label.move(30, 50)

        self.user_input = QLineEdit(self)
        self.user_input.resize(300, 40)
        self.user_input.move(120, 50)

        #CONTRASEÑA
        password_label = QLabel(self)
        password_label.setText('Contraseña: ')
        password_label.setFont(QFont('Arial', 10))
        password_label.move(30, 100)

        self.password_input = QLineEdit(self)
        self.password_input.resize(300, 40)
        self.password_input.move(120, 100)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        #CheckBOX
        self.check_ver_password = QCheckBox(self)
        self.check_ver_password.setText('Ver contraseña')
        self.check_ver_password.move(120, 150)
        self.check_ver_password.toggled.connect(self.mostrarContrasena) #toggled si está con o sin chulito

        #BOTONES
        login_button = QPushButton(self)
        login_button.setText('Iniciar Sesión')
        login_button.resize(400, 50)
        login_button.move(30, 200)
        login_button.clicked.connect(self.raiseMainView)

        register_button = QPushButton(self)
        register_button.setText('Registrarse')
        register_button.resize(400, 50)
        register_button.move(30, 260)
        register_button.clicked.connect(self.raiseRegistrarUsuario)

    def mostrarContrasena(self, clicked):
        if clicked:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
    def raiseMainView(self):
        login = self.user_input.text()
        password = self.password_input.text()
        resultado = self.__miControlador.validarUsuario(login, password)
        if resultado:
            self.pacientes_view = PacientesView(self.__miControlador)
            self.pacientes_view.show()
            self.hide()
        else:
            QMessageBox.critical(self, "Error", "Usuario o contraseña no válidos.")
    def raiseRegistrarUsuario(self):
        self.new_user_form = RegistrarUsuarioView(self)
        self.new_user_form.setControlador(self.__miControlador)
        self.new_user_form.show()
        self.hide()


class RegistrarUsuarioView(QDialog): #QDialog
    def __init__(self, login_view):
        super().__init__()
        self.__miControlador = None
        self.login_view = login_view
        self.raiseFormularioRegister()

    def setControlador(self, c):
        self.__miControlador = c

    def raiseFormularioRegister(self):
        self.setGeometry(100, 100, 450, 350)
        self.setWindowTitle("Registrar usuario")

        #USUARIO
        user_label = QLabel(self)
        user_label.setText('Usuario: ')
        user_label.setFont(QFont('Arial', 10))
        user_label.move(30, 50)
        self.user_input = QLineEdit(self)
        self.user_input.resize(300, 40)
        self.user_input.move(120, 50)

        #CONTRASEÑA
        password_label = QLabel(self)
        password_label.setText('Contraseña: ')
        password_label.setFont(QFont('Arial', 10))
        password_label.move(30, 100)
        self.password_input1 = QLineEdit(self)
        self.password_input1.resize(300, 40)
        self.password_input1.move(120, 100)
        self.password_input1.setEchoMode(QLineEdit.EchoMode.Password)

        password_label = QLabel(self)
        password_label.setText('Confirmar\ncontraseña: ')
        password_label.setFont(QFont('Arial', 10))
        password_label.move(30, 150)
        self.password_input2 = QLineEdit(self)
        self.password_input2.resize(300, 40)
        self.password_input2.move(120, 150)
        self.password_input2.setEchoMode(QLineEdit.EchoMode.Password)
        
        create_button = QPushButton(self)
        create_button.setText('Crear')
        create_button.resize(400, 50)
        create_button.move(30, 210)
        create_button.clicked.connect(self.send_usuario)

        cancel_button = QPushButton(self)
        cancel_button.setText('Cancelar')
        cancel_button.resize(400, 50)
        cancel_button.move(30, 270)
        cancel_button.clicked.connect(self.cancelar_registro)

    def cancelar_registro(self):
        self.login_view.show()
        self.close()

    def send_usuario(self):
        usuario = self.user_input.text()
        password = self.password_input1.text()
        confirm_password = self.password_input2.text()

        if password == confirm_password:
            if self.__miControlador.agregarUsuario(usuario, password):
                QMessageBox.information(self, "Éxito", "Usuario registrado correctamente.")
                self.login_view.show()
                self.close()  # Cierra la ventana de registro
            else:
                QMessageBox.critical(self, "Error", "No se pudo registrar el usuario.")
        else:
            QMessageBox.warning(self, "Advertencia", "Las contraseñas no coinciden.")


class PacientesView(QWidget):
    def __init__(self, controlador):
        super().__init__()
        self.__miControlador = controlador
        self.initUI()

    def setControlador(self, c):
        self.__miControlador = c

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Pacientes')

        layout = QVBoxLayout()
        self.table_view = QTableView()
        layout.addWidget(self.table_view)

        button_layout = QHBoxLayout()
        
        add_button = QPushButton("Añadir Paciente")
        add_button.clicked.connect(self.add_patient)
        button_layout.addWidget(add_button)
        
        edit_button = QPushButton("Editar Paciente")
        edit_button.clicked.connect(self.add_patient)
        button_layout.addWidget(edit_button)
        
        delete_button = QPushButton("Eliminar Paciente")
        delete_button.clicked.connect(self.delete_patient)
        button_layout.addWidget(delete_button)
        
        refresh_button = QPushButton("Refrescar")
        refresh_button.clicked.connect(self.load_data)
        button_layout.addWidget(refresh_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)
        self.load_data()

        self.table_view.doubleClicked.connect(self.open_patient_details)

        self.editarButton = QPushButton("Editar Paciente", self)
        self.editarButton.clicked.connect(self.editar_paciente)

        layout = QVBoxLayout()
        layout.addWidget(self.editarButton)
        self.setLayout(layout)

    def open_patient_details(self, index):
        row = index.row()
        model = self.table_view.model()
        nombre = model.item(row, 0).text()
        cedula = model.item(row, 1).text()
        ruta = model.item(row, 2).text()
        paciente = {'Nombre': nombre, 'Cedula': cedula, 'Ruta': ruta}
        self.atributos_view = AtributosPaciente(self, paciente)
        self.atributos_view.setControlador(self.__miControlador)
        self.atributos_view.show()
        self.hide()

    def load_data(self):
        pacientes = self.__miControlador.obtenerPacientes()
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['Nombre', 'Cédula', 'Ruta'])

        for paciente in pacientes:
            nombre_item = QStandardItem(paciente['Nombre'])
            cedula_item = QStandardItem(str(paciente['Cedula']))
            ruta_item = QStandardItem(str(paciente['Ruta']))
            model.appendRow([nombre_item, cedula_item, ruta_item])

        self.table_view.setModel(model)


    def add_patient(self):
        nombre, ok = QInputDialog.getText(self, 'Añadir Paciente', 'Nombre:')
        if ok:
            cedula, ok = QInputDialog.getInt(self, 'Añadir Paciente', 'Cédula:')
            if ok:
                ruta, ok = QInputDialog.getText(self, 'Añadir Paciente', 'Ruta:')
                if ok:
                    self.__miControlador.agregarPaciente(nombre, cedula, ruta)
                    self.load_data()

    def editar_paciente(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            cedula_paciente = self.table.item(selected_row, 1).text()
            self.controlador.mostrarVentanaEditarPaciente(cedula_paciente)

    def delete_patient(self):
        selected = self.table_view.selectionModel().selectedRows()
        if selected:
            row = selected[0].row()
            cedula_paciente = self.table_view.model().item(row, 1).text()
            confirm = QMessageBox.question(self, 'Eliminar Paciente', 
                                    f'¿Estás seguro de eliminar al paciente con cédula {cedula_paciente}?',
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            if confirm == QMessageBox.StandardButton.Yes:  # Comparar con valores enteros
                self.__miControlador.eliminarPaciente(int(cedula_paciente))
                self.load_data()

class AtributosPaciente(QDialog):
    def __init__(self, pacientes_view, paciente):
        super().__init__()
        self.__miControlador = None
        self.pacientes_view = pacientes_view
        self.paciente = paciente
        self.raiseAtributosPaciente()

    def setControlador(self, c):
        self.__miControlador = c

    def log_out(self):
        self.pacientes_view.show()
        self.close()

    def raiseAtributosPaciente(self):
        self.setGeometry(100, 100, 450, 400)
        self.setWindowTitle("Atributos Paciente")

        self.atributos_label = QLabel(self)
        self.atributos_label.setGeometry(50, 50, 400, 180)
        self.atributos_label.move(30,20)

        imagen = QPixmap(r"C:\Users\Daniel\Documents\DANIEL\udea\semestre3\Informatica 2\PRAC_MVC\Imagenes\figura atributos.png")
        self.atributos_label.setPixmap(imagen)
        self.atributos_label.setScaledContents(True)


        biosignal_button = QPushButton(self)
        biosignal_button.setText('Ver Bioseñal')
        biosignal_button.resize(400, 50)
        biosignal_button.move(30, 210)
        biosignal_button.clicked.connect(self.mostrar_biosignal)

        imagen_button = QPushButton(self)
        imagen_button.setText('Ver Imágen')
        imagen_button.resize(400, 50)
        imagen_button.move(30, 270)
        imagen_button.clicked.connect(self.mostrar_imagen)

        regresar_button = QPushButton(self)
        regresar_button.setText('Regresar')
        regresar_button.resize(400, 50)
        regresar_button.move(30, 330)
        regresar_button.clicked.connect(self.mostrar_imagen)
        regresar_button.clicked.connect(self.log_out)

    def mostrar_biosignal(self):
        cedula = self.paciente['Cedula']
        self.graf_view = InterfazGrafico(self, cedula)
        self.graf_view.setControlador(self.__miControlador)
        self.graf_view.show()
        self.hide()
    def mostrar_imagen(self):
        cedula = self.paciente['Cedula']
        pass
    def regresar(self):
        pass

class VentanaEditarPaciente(QDialog):
    def __init__(self, cedula, controlador):
        super().__init__()
        self.cedula = cedula
        self.controlador = controlador
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Editar Paciente")
        
        self.label = QLabel(f"Cédula: {self.cedula}")
        
        self.bioseñalButton = QPushButton("Añadir Bioseñal", self)
        self.bioseñalButton.clicked.connect(self.añadirBioseñal)

        self.imagenButton = QPushButton("Añadir Imágen Médica", self)
        self.imagenButton.clicked.connect(self.añadirImagen)

        layout = QVBoxLayout()
        layout.addWidget(self.label)

        layout.addWidget(self.bioseñalButton)
        layout.addWidget(self.imagenButton)
        self.setLayout(layout)

    def añadirBioseñal(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Seleccionar Bioseñal", "", "MAT Files (*.mat);;All Files (*)", options=options)
        if filePath:
            self.controlador.agregarBioseñal(self.cedula, filePath)

    def añadirImagen(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Seleccionar Imágen Médica", "", "DICOM Files (*.dcm);;NIFTI Files (*.nii);;All Files (*)", options=options)
        if filePath:
            self.controlador.agregarImagen(self.cedula, filePath)


class MyGraphCanvas(FigureCanvas):
    def __init__(self, parent= None,width=6, height=5, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.compute_initial_figure()
        FigureCanvas.__init__(self,self.fig)

    def compute_initial_figure(self):
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2*np.pi*t)
        self.axes.plot(t,s)
        self.axes.set_xlabel('Radianes')
        self.axes.set_ylabel('Y')
        self.axes.set_title('Señal Seno Base')

    def graficar_senal(self, datos):
        self.axes.clear()
        for c in range(datos.shape[0]):
            self.axes.plot(datos[c,:] + c*10)
        
        self.axes.set_xlabel('Muestras')
        self.axes.set_ylabel('Voltaje (uV)')
        self.axes.set_title('Señales EEG')
        self.draw()  

    def graficaProme(self,datos):
        self.axes.clear()
        self.axes.stem(datos)
        self.axes.set_xlabel('Muestras')
        self.axes.set_ylabel('Voltaje (uV)')
        self.axes.set_title('Señales EEG')
        self.draw()

class InterfazGrafico(QMainWindow):
    def __init__(self, atributos_view, cedula):
        super(InterfazGrafico,self).__init__()
        self.atributos_view = atributos_view
        self.__miControlador = None
        self.__cedula = cedula
        loadUi('interfaz_signal.ui',self)
        self.setup()

    def setControlador(self, c):
        self.__miControlador = c

    def setup(self):
        self.layout = QVBoxLayout()
        self.campo_grafico.setLayout(self.layout)
        self.sc = MyGraphCanvas(self.campo_grafico, width=5, height=4, dpi=100)
        self.layout.addWidget(self.sc)

        #self.boton_cargar.clicked.connect(self.log_out)
        self.boton_cargar.clicked.connect(self.cargar_signal)
        self.boton_adelante.clicked.connect(self.adelantar_senal)
        self.boton_atras.clicked.connect(self.atrasar_senal)
        self.mostrar.clicked.connect(self.mostrarSeg)
        self.boton_regresar.clicked.connect(self.log_out)

        self.boton_adelante.setEnabled(False)
        self.boton_atras.setEnabled(False)
        # self.boton_aumentar.setEnabled(False)
        # self.boton_disminuir.setEnabled(False)

    def log_out(self):
       self.atributos_view.show()
       self.close()

    def cargar_signal(self):
        archivo = self.__miControlador.recibirSenal(self.__cedula)['Ruta']
        data = sio.loadmat(archivo) # Diccionario
        data = data["data"] ##revisar
        sensores, puntos, ensayos = data.shape
        senal_continua = np.reshape(data,(sensores,puntos*ensayos),order = 'F') # Conveirte de 3D a 2D
        self.__miControlador.recibirDatosSenal(senal_continua)
        self.x_min = 0
        self.x_max = 2000
        self.sc.graficar_senal(self.__miControlador.devolverDatosSenal(self.x_min, self.x_max))
        self.boton_adelante.setEnabled(True)
        self.boton_atras.setEnabled(True)
  
    def mostrarSeg(self):
        self.x_max = int(self.maximo.text())
        self.x_min = int(self.minimo.text())
        self.sc.graficar_senal(self.__miControlador.devolverDatosSenal(self.x_min, self.x_max))   

    def atrasar_senal(self):
        if self.x_min < 2000:
            return
        self.x_min = self.x_min - 2000
        self.x_max = self.x_max - 2000
        self.sc.graficar_senal(self.__miControlador.devolverDatosSenal(self.x_min, self.x_max))

    def adelantar_senal(self):
        self.x_min = self.x_min + 2000
        self.x_max = self.x_max + 2000
        self.sc.graficar_senal(self.__miControlador.devolverDatosSenal(self.x_min, self.x_max))

    def promedio(self):
        self.sc.graficaProme(self.__miControlador.calcularProm(self.x_min, self.x_max))