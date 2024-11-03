import sys
from datetime import datetime
from fpdf import FPDF
from models import Usuario, Gimnasio
from exceptions import (
    handle_exception, 
    UsuarioNoEncontradoError, 
    validar_datos_usuario, 
    validar_medidas
)

class Console:
    def __init__(self):
        self.gimnasio = Gimnasio()
        self.opciones = {
            "1": self.registrar_usuario,
            "2": self.registrar_medidas,
            "3": self.registrar_asistencia,
            "4": self.ver_estado_membresia,
            "5": self.generar_reporte,
            "6": self.congelar_membresia,
            "7": self.activar_membresia,
            "8": self.salir
        }

    def mostrar_menu(self):
        print("\n--- SISTEMA DE GESTIÓN DE GIMNASIO ---")
        print("1. Registrar nuevo usuario")
        print("2. Registrar medidas")
        print("3. Registrar asistencia")
        print("4. Ver estado de membresía")
        print("5. Generar reporte")
        print("6. Congelar membresía")
        print("7. Activar membresía")
        print("8. Salir")

    def ejecutar(self):
        while True:
            self.mostrar_menu()
            opcion = input("Seleccione una opción: ")
            accion = self.opciones.get(opcion)
            if accion:
                accion()
            else:
                print("Opción no válida. Intente nuevamente.")

    @handle_exception
    def registrar_usuario(self):
        print("\n--- Registro de Usuario ---")
        id_usuario = input("ID de usuario: ")
        nombre = input("Nombre: ")
        correo = input("Correo: ")
        direccion = input("Dirección: ")
        telefono = input("Teléfono: ")
        
        validar_datos_usuario(nombre, correo, telefono)
        nuevo_usuario = Usuario(id_usuario, nombre, correo, direccion, telefono)
        self.gimnasio.agregar_usuario(nuevo_usuario)
        print("Usuario registrado exitosamente.")

    @handle_exception
    def registrar_medidas(self):
        print("\n--- Registro de Medidas ---")
        id_usuario = input("ID de usuario: ")
        peso = float(input("Peso (kg): "))
        altura = float(input("Altura (m): "))
        
        validar_medidas(peso, altura)
        usuario = self.gimnasio.obtener_usuario(id_usuario)
        usuario.registrar_medidas(peso, altura)
        print("Medidas registradas exitosamente.")

    @handle_exception
    def registrar_asistencia(self):
        print("\n--- Registro de Asistencia ---")
        id_usuario = input("ID de usuario: ")
        hora_ingreso = datetime.now()
        hora_salida_str = input("Hora de salida (HH:MM) o presione Enter si aún no sale: ")
        
        usuario = self.gimnasio.obtener_usuario(id_usuario)
        if hora_salida_str:
            try:
                hora, minuto = map(int, hora_salida_str.split(':'))
                hora_salida = datetime.now().replace(hour=hora, minute=minuto)
            except ValueError:
                raise ValueError("Formato de hora inválido. Use HH:MM")
        else:
            hora_salida = None
        self.gimnasio.registrar_ingreso(id_usuario, datetime.now().date(), hora_ingreso, hora_salida)
        print("Asistencia registrada exitosamente.")

    @handle_exception
    def ver_estado_membresia(self):
        print("\n--- Estado de Membresía ---")
        id_usuario = input("ID de usuario: ")
        usuario = self.gimnasio.obtener_usuario(id_usuario)
        print(f"Estado de membresía: {usuario.membresia}")

    @handle_exception
    def generar_reporte(self):
        print("\n--- Generación de Reporte ---")
        id_usuario = input("ID de usuario: ")
        mes = int(input("Mes (1-12): "))
        anio = int(input("Año: "))
        
        usuario = self.gimnasio.obtener_usuario(id_usuario)
        self._generar_reporte_pdf(usuario, mes, anio)

    def _generar_reporte_pdf(self, usuario, mes, anio):
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        pdf.set_font('DejaVu', '', 12)
        
        pdf.cell(200, 10, txt="Reporte de Actividad", ln=True, align='C')
        pdf.cell(200, 10, txt=f"Usuario: {usuario.nombre}", ln=True)
        pdf.cell(200, 10, txt=f"Mes: {mes}, Año: {anio}", ln=True)
        
        asistencias = [a for a in usuario.registro_ingreso if a['fecha'].month == mes and a['fecha'].year == anio]
        pdf.cell(200, 10, txt=f"Total de asistencias: {len(asistencias)}", ln=True)
        
        for asistencia in asistencias:
            pdf.cell(200, 10, txt=f"Fecha: {asistencia['fecha'].strftime('%d/%m/%Y')}", ln=True)
            pdf.cell(200, 10, txt=f"Hora de ingreso: {asistencia['hora_ingreso'].strftime('%H:%M')}", ln=True)
            if asistencia['hora_salida']:
                pdf.cell(200, 10, txt=f"Hora de salida: {asistencia['hora_salida'].strftime('%H:%M')}", ln=True)
            pdf.cell(200, 10, txt=f"Tiempo de entrenamiento: {asistencia['tiempo_entrenamiento']:.2f} minutos", ln=True)
            pdf.cell(200, 10, txt="--------------------", ln=True)
        
        filename = f"reporte_{usuario.id_usuario}_{mes}_{anio}.pdf"
        pdf.output(filename)
        print(f"Reporte generado: {filename}")

    @handle_exception
    def congelar_membresia(self):
        print("\n--- Congelar Membresía ---")
        id_usuario = input("ID de usuario: ")
        usuario = self.gimnasio.obtener_usuario(id_usuario)
        usuario.congelar_membresia()
        print("Membresía congelada exitosamente.")

    @handle_exception
    def activar_membresia(self):
        print("\n--- Activar Membresía ---")
        id_usuario = input("ID de usuario: ")
        usuario = self.gimnasio.obtener_usuario(id_usuario)
        usuario.activar_membresia()
        print("Membresía activada exitosamente.")

    def salir(self):
        print("Gracias por usar el Sistema de Gestión de Gimnasio. ¡Hasta pronto!")
        sys.exit(0)

if __name__ == "__main__":
    console = Console()
    console.ejecutar()