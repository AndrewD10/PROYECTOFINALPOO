from models import Usuario, Gimnasio
from exceptions import *
from datetime import datetime
from typing import Dict, Any
from fpdf import FPDF

gimnasio = Gimnasio()

def handle_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except GimnasioError as e:
            return {"error": True, "mensaje": str(e)}
        except Exception as e:
            return {"error": True, "mensaje": f"Error inesperado: {str(e)}"}
    return wrapper

@handle_exception
def registrar_usuario(id_usuario: str, nombre: str, correo: str, direccion: str, telefono: str) -> Dict[str, Any]:
    if id_usuario in gimnasio.usuarios:
        raise UsuarioYaExisteError(id_usuario)
    
    nuevo_usuario = Usuario(id_usuario, nombre, correo, direccion, telefono)
    gimnasio.agregar_usuario(nuevo_usuario)
    return {"error": False, "mensaje": f"Usuario {nombre} registrado exitosamente."}

@handle_exception
def ver_estado_membresia(id_usuario: str) -> Dict[str, Any]:
    if id_usuario not in gimnasio.usuarios:
        raise UsuarioNoEncontradoError(id_usuario)
    
    usuario = gimnasio.usuarios[id_usuario]
    return {"error": False, "mensaje": f"Estado de membresía: {usuario.membresia}"}

@handle_exception
def registrar_peso_medidas(id_usuario: str, peso: float, altura: float) -> Dict[str, Any]:
    if id_usuario not in gimnasio.usuarios:
        raise UsuarioNoEncontradoError(id_usuario)
    
    usuario = gimnasio.usuarios[id_usuario]
    usuario.peso = peso
    usuario.altura = altura
    return {"error": False, "mensaje": f"Peso y medidas registrados para {usuario.nombre}"}

@handle_exception
def registrar_ingreso_salida(id_usuario: str, hora_ingreso: datetime, hora_salida: datetime) -> Dict[str, Any]:
    if id_usuario not in gimnasio.usuarios:
        raise UsuarioNoEncontradoError(id_usuario)
    
    usuario = gimnasio.usuarios[id_usuario]
    if usuario.membresia == 'cancelada':
        raise MembresiaError("La membresía está cancelada")
    
    tiempo_entrenamiento = (hora_salida - hora_ingreso).total_seconds() / 60
    usuario.registrar_ingreso(hora_ingreso, hora_salida, tiempo_entrenamiento)
    return {"error": False, "mensaje": f"Ingreso y salida registrados. Tiempo: {tiempo_entrenamiento:.2f} minutos"}

@handle_exception
def congelar_membresia(id_usuario: str) -> Dict[str, Any]:
    if id_usuario not in gimnasio.usuarios:
        raise UsuarioNoEncontradoError(id_usuario)
    
    usuario = gimnasio.usuarios[id_usuario]
    if usuario.membresia == 'congelada':
        raise MembresiaError("La membresía ya está congelada")
    
    usuario.membresia = 'congelada'
    return {"error": False, "mensaje": f"Membresía de {usuario.nombre} congelada"}

@handle_exception
def activar_membresia(id_usuario: str) -> Dict[str, Any]:
    if id_usuario not in gimnasio.usuarios:
        raise UsuarioNoEncontradoError(id_usuario)
    
    usuario = gimnasio.usuarios[id_usuario]
    if usuario.membresia == 'activa':
        raise MembresiaError("La membresía ya está activa")
    
    usuario.membresia = 'activa'
    return {"error": False, "mensaje": f"Membresía de {usuario.nombre} activada"}

@handle_exception
def ingresar_invitado(nombre_invitado: str) -> Dict[str, Any]:
    id_invitado = f'invitado_{len(gimnasio.usuarios) + 1}'
    invitado = Usuario(id_invitado, nombre_invitado, 'invitado@ejemplo.com', 'N/A', 'N/A')
    gimnasio.agregar_usuario(invitado)
    return {"error": False, "mensaje": f"Invitado {nombre_invitado} registrado con ID: {id_invitado}"}

@handle_exception
def eliminar_usuario(id_usuario: str) -> Dict[str, Any]:
    if id_usuario not in gimnasio.usuarios:
        raise UsuarioNoEncontradoError(id_usuario)
    
    nombre_usuario = gimnasio.usuarios[id_usuario].nombre
    del gimnasio.usuarios[id_usuario]
    return {"error": False, "mensaje": f"Usuario {nombre_usuario} eliminado exitosamente"}

@handle_exception
def generar_reporte_pdf(id_usuario: str, mes: int, anio: int) -> Dict[str, Any]:
    if id_usuario not in gimnasio.usuarios:
        raise UsuarioNoEncontradoError(id_usuario)
    
    usuario = gimnasio.usuarios[id_usuario]
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Reporte de Actividad - {usuario.nombre}", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Mes: {mes}, Año: {anio}", ln=True)
    pdf.cell(200, 10, txt=f"Estado de Membresía: {usuario.membresia}", ln=True)
    
    for registro in usuario.registro_ingresos:
        if registro['fecha'].month == mes and registro['fecha'].year == anio:
            pdf.cell(200, 10, txt=f"Fecha: {registro['fecha']}, Tiempo: {registro['tiempo_entrenamiento']:.2f} min", ln=True)
    
    filename = f"reporte_{usuario.id_usuario}_{mes}_{anio}.pdf"
    pdf.output(filename)
    return {"error": False, "mensaje": f"Reporte generado: {filename}"}