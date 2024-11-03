import logging
import re
from typing import Any, Dict, Callable
from functools import wraps
from datetime import datetime

# Configuración del logging
logging.basicConfig(
    filename='gimnasio.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GimnasioError(Exception):
    """Clase base para excepciones del gimnasio"""
    def __init__(self, message: str):
        self.message = message
        self.timestamp = datetime.now()
        logger.error(f"{self.__class__.__name__}: {message}")
        super().__init__(self.message)

class UsuarioError(GimnasioError):
    """Clase base para excepciones relacionadas con usuarios"""
    pass

class UsuarioNoEncontradoError(UsuarioError):
    """Se lanza cuando no se encuentra un usuario"""
    def __init__(self, id_usuario: str):
        super().__init__(f"Usuario con ID {id_usuario} no encontrado")

class UsuarioYaExisteError(UsuarioError):
    """Se lanza cuando se intenta registrar un usuario que ya existe"""
    def __init__(self, id_usuario: str):
        super().__init__(f"Usuario con ID {id_usuario} ya está registrado")

class DatosInvalidosError(GimnasioError):
    """Se lanza cuando los datos proporcionados son inválidos"""
    def __init__(self, campo: str, razon: str):
        super().__init__(f"Datos inválidos para {campo}: {razon}")

class MembresiaError(GimnasioError):
    """Excepciones relacionadas con membresías"""
    def __init__(self, mensaje: str):
        super().__init__(mensaje)

class ReporteError(GimnasioError):
    """Excepciones relacionadas con la generación de reportes"""
    def __init__(self, mensaje: str):
        super().__init__(mensaje)

class AsistenciaError(GimnasioError):
    """Excepciones relacionadas con el registro de asistencia"""
    def __init__(self, mensaje: str):
        super().__init__(mensaje)

class MedidasError(GimnasioError):
    """Excepciones relacionadas con el registro de medidas"""
    def __init__(self, mensaje: str):
        super().__init__(mensaje)

def validar_datos_usuario(nombre: str, correo: str, telefono: str) -> None:
    """
    Valida los datos del usuario
    Args:
        nombre: Nombre del usuario
        correo: Correo electrónico
        telefono: Número de teléfono
    Raises:
        DatosInvalidosError: Si algún dato es inválido
    """
    # Validación del nombre
    if not nombre or len(nombre.strip()) < 3:
        raise DatosInvalidosError("nombre", "debe tener al menos 3 caracteres")
    
    if not all(c.isalpha() or c.isspace() for c in nombre):
        raise DatosInvalidosError("nombre", "solo debe contener letras y espacios")

    # Validación del correo
    patron_correo = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(patron_correo, correo):
        raise DatosInvalidosError("correo", "formato de correo inválido")
    
    # Validación del teléfono
    patron_telefono = r'^\+?1?\d{9,15}$'
    if not re.match(patron_telefono, telefono):
        raise DatosInvalidosError("teléfono", "formato de teléfono inválido")

def validar_medidas(peso: float, altura: float) -> None:
    """
    Valida las medidas físicas
    Args:
        peso: Peso en kilogramos
        altura: Altura en metros
    Raises:
        DatosInvalidosError: Si las medidas están fuera de rango
    """
    if not isinstance(peso, (int, float)) or not isinstance(altura, (int, float)):
        raise DatosInvalidosError("medidas", "deben ser valores numéricos")

    if peso <= 0 or peso > 300:
        raise DatosInvalidosError("peso", "debe estar entre 0 y 300 kg")
    
    if altura <= 0 or altura > 3:
        raise DatosInvalidosError("altura", "debe estar entre 0 y 3 metros")

def validar_fecha(fecha: datetime) -> None:
    """
    Valida una fecha
    Args:
        fecha: Fecha a validar
    Raises:
        DatosInvalidosError: Si la fecha es inválida
    """
    if not isinstance(fecha, datetime):
        raise DatosInvalidosError("fecha", "debe ser un objeto datetime válido")
    
    if fecha > datetime.now():
        raise DatosInvalidosError("fecha", "no puede ser futura")

def handle_exception(func: Callable) -> Callable:
    """
    Decorador para manejar excepciones de manera uniforme
    Args:
        func: Función a decorar
    Returns:
        Dict con información sobre el resultado de la operación
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Dict[str, Any]:
        try:
            resultado = func(*args, **kwargs)
            return {
                "error": False,
                "resultado": resultado,
                "mensaje": "Operación exitosa"
            }
        except (UsuarioError, MembresiaError, DatosInvalidosError, 
                ReporteError, AsistenciaError, MedidasError) as e:
            logger.error(f"{e.__class__.__name__}: {str(e)}")
            return {
                "error": True,
                "tipo_error": e.__class__.__name__,
                "mensaje": str(e)
            }
        except Exception as e:
            logger.critical(f"Error inesperado: {str(e)}", exc_info=True)
            return {
                "error": True,
                "tipo_error": "Error interno",
                "mensaje": "Error interno del sistema"
            }
    return wrapper