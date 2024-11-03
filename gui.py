import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from fpdf import FPDF

# Excepciones personalizadas
class GimnasioError(Exception):
    pass

class UsuarioNoEncontradoError(GimnasioError):
    pass

# Validación de datos
def validar_datos_usuario(usuario):
    if not usuario or not isinstance(usuario, Usuario):
        raise UsuarioNoEncontradoError("Usuario inválido o no encontrado.")

# Modelos de datos
class Usuario:
    def __init__(self, user_id, nombre, edad):
        self.user_id = user_id
        self.nombre = nombre
        self.edad = edad
        self.medidas = []
        self.asistencias = []
        self.fecha_membresia = datetime.now()
        self.activo = True

    def registrar_medidas(self, medidas):
        self.medidas.append(medidas)

    def registrar_asistencia(self):
        self.asistencias.append(datetime.now())

    def eliminar_asistencia(self):
        if self.asistencias:
            self.asistencias.pop()

    def estado_membresia(self):
        if not self.activo or (datetime.now() - self.fecha_membresia).days > 30:
            return "Expirada"
        else:
            return "Activa"

    def activar_membresia(self):
        self.activo = True
        self.fecha_membresia = datetime.now()

    def desactivar_membresia(self):
        self.activo = False

class Gimnasio:
    def __init__(self):
        self.usuarios = {}

    def registrar_usuario(self, usuario):
        if usuario.user_id in self.usuarios:
            raise GimnasioError("El usuario ya está registrado.")
        self.usuarios[usuario.user_id] = usuario

    def obtener_usuario(self, user_id):
        usuario = self.usuarios.get(user_id)
        if not usuario:
            raise UsuarioNoEncontradoError("Usuario no encontrado.")
        return usuario

class ReportePDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Reporte del Gimnasio", 0, 1, "C")

    def generar_reporte_usuario(self, usuario):
        self.add_page()
        self.set_font("Arial", "", 12)
        self.cell(0, 10, f"ID de Usuario: {usuario.user_id}", 0, 1)
        self.cell(0, 10, f"Nombre: {usuario.nombre}", 0, 1)
        self.cell(0, 10, f"Edad: {usuario.edad}", 0, 1)
        self.cell(0, 10, f"Estado de Membresía: {usuario.estado_membresia()}", 0, 1)
        self.cell(0, 10, f"Asistencias: {len(usuario.asistencias)}", 0, 1)
        for medida in usuario.medidas:
            self.cell(0, 10, f"- Peso: {medida['peso']} kg, Altura: {medida['altura']} m", 0, 1)

# Interfaz gráfica con Tkinter
class GimnasioApp:
    def __init__(self, root):
        self.root = root
        self.gimnasio = Gimnasio()
        
        root.title("Gimnasio - Gestión de Usuarios")
        root.geometry("400x600")
        
        # Campos de entrada
        tk.Label(root, text="ID de Usuario:").pack(pady=5)
        self.entry_id = tk.Entry(root)
        self.entry_id.pack(pady=5)
        
        tk.Label(root, text="Nombre:").pack(pady=5)
        self.entry_nombre = tk.Entry(root, state="disabled")
        self.entry_nombre.pack(pady=5)

        tk.Label(root, text="Edad:").pack(pady=5)
        self.entry_edad = tk.Entry(root, state="disabled")
        self.entry_edad.pack(pady=5)
        
        tk.Label(root, text="Peso (kg):").pack(pady=5)
        self.entry_peso = tk.Entry(root, state="disabled")
        self.entry_peso.pack(pady=5)

        tk.Label(root, text="Altura (m):").pack(pady=5)
        self.entry_altura = tk.Entry(root, state="disabled")
        self.entry_altura.pack(pady=5)

        # Botones
        tk.Button(root, text="Registrar Usuario", command=self.mostrar_registro_usuario).pack(pady=5)
        
        # Botones para acciones que requieren ID y nombre
        self.boton_asistencia = tk.Button(root, text="Registrar Asistencia", command=self.mostrar_registrar_asistencia)
        self.boton_asistencia.pack(pady=5)

        self.boton_eliminar_asistencia = tk.Button(root, text="Eliminar Asistencia", command=self.mostrar_eliminar_asistencia)
        self.boton_eliminar_asistencia.pack(pady=5)

        self.boton_ver_estado = tk.Button(root, text="Ver Estado de Membresía", command=self.mostrar_ver_estado)
        self.boton_ver_estado.pack(pady=5)

        self.boton_activar_membresia = tk.Button(root, text="Activar Membresía", command=self.mostrar_activar_membresia)
        self.boton_activar_membresia.pack(pady=5)

        self.boton_desactivar_membresia = tk.Button(root, text="Desactivar Membresía", command=self.mostrar_desactivar_membresia)
        self.boton_desactivar_membresia.pack(pady=5)

        self.boton_generar_reporte = tk.Button(root, text="Generar Reporte PDF", command=self.mostrar_generar_reporte)
        self.boton_generar_reporte.pack(pady=5)

        # Botón para guardar tanto usuario como medidas
        tk.Button(root, text="Guardar Usuario y Medidas", command=self.guardar_usuario_y_medidas).pack(pady=5)

        # Text area para mostrar resultados
        self.text_area = tk.Text(root, height=10, width=40)
        self.text_area.pack(pady=5)

    def limpiar_campos(self):
        # Solo limpia los campos de nombre, edad, peso y altura
        self.entry_nombre.delete(0, tk.END)
        self.entry_edad.delete(0, tk.END)
        self.entry_peso.delete(0, tk.END)
        self.entry_altura.delete(0, tk.END)

    def mostrar_campos(self, campos):
        self.limpiar_campos()
        # Deshabilitar todos los campos
        self.entry_nombre.config(state="disabled")
        self.entry_edad.config(state="disabled")
        self.entry_peso.config(state="disabled")
        self.entry_altura.config(state="disabled")
        # Habilitar los necesarios
        if "nombre" in campos: 
            self.entry_nombre.config(state="normal")
        if "edad" in campos: 
            self.entry_edad.config(state="normal")
        if "peso" in campos: 
            self.entry_peso.config(state="normal")
        if "altura" in campos: 
            self.entry_altura.config(state="normal")

    def mostrar_registro_usuario(self):
        self.mostrar_campos(["nombre", "edad", "peso", "altura"])  # Habilitar todos los campos
        self.entry_id.config(state="normal")
        self.entry_id.delete(0, tk.END)
        self.text_area.delete(1.0, tk.END)

    def guardar_usuario_y_medidas(self):
        user_id = self.entry_id.get().strip()
        nombre = self.entry_nombre.get().strip()
        edad = self.entry_edad.get().strip()
        peso = self.entry_peso.get().strip()
        altura = self.entry_altura.get().strip()

        if not user_id or not nombre or not edad or not peso or not altura:
            messagebox.showwarning("Error", "Debe ingresar todos los datos del usuario y medidas.")
            return

        try:
            # Convertimos la edad, peso y altura a los tipos apropiados
            edad = int(edad)
            peso = float(peso)
            altura = float(altura)

            # Verificar si el usuario ya está registrado
            if user_id in self.gimnasio.usuarios:
                usuario = self.gimnasio.obtener_usuario(user_id)
                usuario.nombre = nombre  # Actualizar nombre
                usuario.edad = edad      # Actualizar edad
                usuario.registrar_medidas({'peso': peso, 'altura': altura})  # Registrar medidas
                self.text_area.insert(tk.END, f"Datos actualizados para {user_id}.\n")
            else:
                usuario = Usuario(user_id, nombre, edad)
                usuario.registrar_medidas({'peso': peso, 'altura': altura})  # Registrar medidas
                self.gimnasio.registrar_usuario(usuario)
                self.text_area.insert(tk.END, f"Usuario {user_id} registrado exitosamente.\n")

            # Deshabilitar los campos después de guardar
            self.entry_id.config(state="disabled")
            self.entry_nombre.config(state="disabled")
            self.entry_edad.config(state="disabled")
            self.entry_peso.config(state="disabled")
            self.entry_altura.config(state="disabled")

        except ValueError:
            messagebox.showwarning("Error", "Datos inválidos. Asegúrese de ingresar números en edad, peso y altura.")

    def mostrar_registrar_asistencia(self):
        self.mostrar_campos(["nombre"])
        self.entry_id.config(state="normal")
        if self.boton_asistencia['text'] == "Registrar Asistencia":
            self.boton_asistencia['text'] = "Confirmar Asistencia"
        else:
            user_id = self.entry_id.get().strip()
            if not user_id:
                messagebox.showwarning("Error", "Debe ingresar el ID de usuario.")
                return
            try:
                usuario = self.gimnasio.obtener_usuario(user_id)
                usuario.registrar_asistencia()
                self.text_area.insert(tk.END, f"Asistencia registrada para {user_id}.\n")
            except UsuarioNoEncontradoError:
                messagebox.showerror("Error", "Usuario no encontrado.")
            self.boton_asistencia['text'] = "Registrar Asistencia"
            self.entry_id.config(state="disabled")

    def mostrar_eliminar_asistencia(self):
        self.mostrar_campos(["nombre"])
        self.entry_id.config(state="normal")
        if self.boton_eliminar_asistencia['text'] == "Eliminar Asistencia":
            self.boton_eliminar_asistencia['text'] = "Confirmar Eliminación"
        else:
            user_id = self.entry_id.get().strip()
            if not user_id:
                messagebox.showwarning("Error", "Debe ingresar el ID de usuario.")
                return
            try:
                usuario = self.gimnasio.obtener_usuario(user_id)
                usuario.eliminar_asistencia()
                self.text_area.insert(tk.END, f"Asistencia eliminada para {user_id}.\n")
            except UsuarioNoEncontradoError:
                messagebox.showerror("Error", "Usuario no encontrado.")
            self.boton_eliminar_asistencia['text'] = "Eliminar Asistencia"
            self.entry_id.config(state="disabled")

    def mostrar_ver_estado(self):
        self.mostrar_campos(["nombre"])
        self.entry_id.config(state="normal")
        if self.boton_ver_estado['text'] == "Ver Estado de Membresía":
            self.boton_ver_estado['text'] = "Confirmar Estado"
        else:
            user_id = self.entry_id.get().strip()
            if not user_id:
                messagebox.showwarning("Error", "Debe ingresar el ID de usuario.")
                return
            try:
                usuario = self.gimnasio.obtener_usuario(user_id)
                estado = usuario.estado_membresia()
                self.text_area.insert(tk.END, f"Estado de membresía para {user_id}: {estado}.\n")
            except UsuarioNoEncontradoError:
                messagebox.showerror("Error", "Usuario no encontrado.")
            self.boton_ver_estado['text'] = "Ver Estado de Membresía"
            self.entry_id.config(state="disabled")

    def mostrar_activar_membresia(self):
        self.mostrar_campos(["nombre"])
        self.entry_id.config(state="normal")
        if self.boton_activar_membresia['text'] == "Activar Membresía":
            self.boton_activar_membresia['text'] = "Confirmar Activación"
        else:
            user_id = self.entry_id.get().strip()
            if not user_id:
                messagebox.showwarning("Error", "Debe ingresar el ID de usuario.")
                return
            try:
                usuario = self.gimnasio.obtener_usuario(user_id)
                usuario.activar_membresia()
                self.text_area.insert(tk.END, f"Membresía activada para {user_id}.\n")
            except UsuarioNoEncontradoError:
                messagebox.showerror("Error", "Usuario no encontrado.")
            self.boton_activar_membresia['text'] = "Activar Membresía"
            self.entry_id.config(state="disabled")

    def mostrar_desactivar_membresia(self):
        self.mostrar_campos(["nombre"])
        self.entry_id.config(state="normal")
        if self.boton_desactivar_membresia['text'] == "Desactivar Membresía":
            self.boton_desactivar_membresia['text'] = "Confirmar Desactivación"
        else:
            user_id = self.entry_id.get().strip()
            if not user_id:
                messagebox.showwarning("Error", "Debe ingresar el ID de usuario.")
                return
            try:
                usuario = self.gimnasio.obtener_usuario(user_id)
                usuario.desactivar_membresia()
                self.text_area.insert(tk.END, f"Membresía desactivada para {user_id}.\n")
            except UsuarioNoEncontradoError:
                messagebox.showerror("Error", "Usuario no encontrado.")
            self.boton_desactivar_membresia['text'] = "Desactivar Membresía"
            self.entry_id.config(state="disabled")

    def mostrar_generar_reporte(self):
        self.mostrar_campos(["nombre"])
        self.entry_id.config(state="normal")
        if self.boton_generar_reporte['text'] == "Generar Reporte PDF":
            self.boton_generar_reporte['text'] = "Confirmar Generación"
        else:
            user_id = self.entry_id.get().strip()
            if not user_id:
                messagebox.showwarning("Error", "Debe ingresar el ID de usuario.")
                return
            try:
                usuario = self.gimnasio.obtener_usuario(user_id)
                pdf = ReportePDF()
                pdf.generar_reporte_usuario(usuario)
                pdf_file_name = f"reporte_{user_id}.pdf"
                pdf.output(pdf_file_name)
                self.text_area.insert(tk.END, f"Reporte PDF generado para {user_id}.\n")
            except UsuarioNoEncontradoError:
                messagebox.showerror("Error", "Usuario no encontrado.")
            self.boton_generar_reporte['text'] = "Generar Reporte PDF"
            self.entry_id.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = GimnasioApp(root)
    root.mainloop()
