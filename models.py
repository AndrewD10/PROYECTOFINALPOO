from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

class Usuario:
    """Clase que representa un usuario del gimnasio"""
    def __init__(self, id_usuario: str, nombre: str, correo: str, 
                 direccion: str, telefono: str):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.correo = correo
        self.direccion = direccion
        self.telefono = telefono
        self.membresia = 'Activa'
        self.medidas: List[Dict[str, Any]] = []
        self.registro_ingreso: List[Dict[str, Any]] = []
        self.tiempo_entrenamiento_total: float = 0
        self.fecha_registro = datetime.now()
        self.ultima_actualizacion = datetime.now()

    def registrar_medidas(self, peso: float, altura: float) -> None:
        """Registra las medidas del usuario"""
        if peso <= 0 or altura <= 0:
            raise ValueError("El peso y la altura deben ser valores positivos")
        
        imc = peso / (altura ** 2)
        medida = {
            'fecha': datetime.now(),
            'peso': peso,
            'altura': altura,
            'imc': round(imc, 2)
        }
        self.medidas.append(medida)
        self.ultima_actualizacion = datetime.now()

    def congelar_membresia(self) -> None:
        """Congela la membresía del usuario"""
        if self.membresia == "Activa":
            self.membresia = "Congelada"
            self.ultima_actualizacion = datetime.now()
        else:
            raise ValueError("La membresía no se puede congelar porque no está activa")

    def activar_membresia(self) -> None:
        """Activa la membresía del usuario"""
        if self.membresia == "Congelada":
            self.membresia = "Activa"
            self.ultima_actualizacion = datetime.now()
        else:
            raise ValueError("La membresía ya está activa o no se puede activar")

    def obtener_historial_medidas(self) -> List[Dict[str, Any]]:
        """Retorna el historial de medidas del usuario"""
        return sorted(self.medidas, key=lambda x: x['fecha'], reverse=True)

    def obtener_ultima_medida(self) -> Optional[Dict[str, Any]]:
        """Retorna la última medida registrada"""
        if self.medidas:
            return self.medidas[-1]
        return None

    def calcular_tiempo_total_entrenamiento(self) -> float:
        """Calcula el tiempo total de entrenamiento en minutos"""
        return sum(registro['tiempo_entrenamiento'] for registro in self.registro_ingreso)

    def to_dict(self) -> Dict[str, Any]:
        """Convierte el usuario a un diccionario"""
        return {
            'id_usuario': self.id_usuario,
            'nombre': self.nombre,
            'correo': self.correo,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'membresia': self.membresia,
            'medidas': self.medidas,
            'tiempo_total': self.tiempo_entrenamiento_total,
            'fecha_registro': self.fecha_registro,
            'ultima_actualizacion': self.ultima_actualizacion
        }

class Gimnasio:
    """Clase que gestiona el gimnasio"""
    def __init__(self):
        self.usuarios: Dict[str, Usuario] = {}
        self.fecha_inicio = datetime.now()

    def agregar_usuario(self, usuario: Usuario) -> None:
        """Agrega un usuario al gimnasio"""
        if usuario.id_usuario in self.usuarios:
            raise ValueError(f"El usuario con ID {usuario.id_usuario} ya existe")
        self.usuarios[usuario.id_usuario] = usuario

    def obtener_usuario(self, id_usuario: str) -> Usuario:
        """Obtiene un usuario por su ID"""
        usuario = self.usuarios.get(id_usuario)
        if not usuario:
            raise ValueError(f"Usuario con ID {id_usuario} no encontrado")
        return usuario

    def eliminar_usuario(self, id_usuario: str) -> None:
        """Elimina un usuario del gimnasio"""
        if id_usuario not in self.usuarios:
            raise ValueError(f"Usuario con ID {id_usuario} no encontrado")
        del self.usuarios[id_usuario]

    def registrar_ingreso(self, id_usuario: str, fecha: datetime, 
                         hora_ingreso: datetime, hora_salida: Optional[datetime] = None) -> None:
        """Registra el ingreso y salida de un usuario"""
        usuario = self.obtener_usuario(id_usuario)
        
        if usuario.membresia != "Activa":
            raise ValueError("No se puede registrar ingreso con membresía inactiva")

        tiempo_entrenamiento = 0
        if hora_salida:
            if hora_salida < hora_ingreso:
                raise ValueError("La hora de salida no puede ser menor a la hora de ingreso")
            tiempo_entrenamiento = (hora_salida - hora_ingreso).total_seconds() / 60

        registro = {
            'fecha': fecha,
            'hora_ingreso': hora_ingreso,
            'hora_salida': hora_salida,
            'tiempo_entrenamiento': tiempo_entrenamiento
        }
        
        usuario.registro_ingreso.append(registro)
        usuario.tiempo_entrenamiento_total += tiempo_entrenamiento

    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Obtiene estadísticas generales del gimnasio"""
        total_usuarios = len(self.usuarios)
        usuarios_activos = sum(1 for u in self.usuarios.values() if u.membresia == "Activa")
        usuarios_congelados = total_usuarios - usuarios_activos
        
        return {
            'total_usuarios': total_usuarios,
            'usuarios_activos': usuarios_activos,
            'usuarios_congelados': usuarios_congelados,
            'fecha_inicio': self.fecha_inicio
        }

    def buscar_usuarios(self, criterio: str, valor: str) -> List[Usuario]:
        """Busca usuarios según un criterio específico"""
        resultados = []
        for usuario in self.usuarios.values():
            if criterio == 'nombre' and valor.lower() in usuario.nombre.lower():
                resultados.append(usuario)
            elif criterio == 'membresia' and valor.lower() == usuario.membresia.lower():
                resultados.append(usuario)
        return resultados

# Instancia global del gimnasio
gimnasio = Gimnasio()