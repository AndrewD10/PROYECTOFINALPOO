import unittest
from datetime import datetime
from models import Usuario, Gimnasio
from exceptions import *

class TestGimnasio(unittest.TestCase):
    def setUp(self):
        """Se ejecuta antes de cada prueba"""
        self.gimnasio = Gimnasio()
        self.usuario_prueba = Usuario(
            id_usuario="U001",
            nombre="Juan Pérez",
            correo="juan@ejemplo.com",
            direccion="Calle Principal 123",
            telefono="1234567890"
        )

    def test_registro_usuario(self):
        """Prueba el registro de usuarios"""
        self.gimnasio.agregar_usuario(self.usuario_prueba)
        self.assertIn(self.usuario_prueba.id_usuario, self.gimnasio.usuarios)
        
        # Prueba registro duplicado
        with self.assertRaises(ValueError):
            self.gimnasio.agregar_usuario(self.usuario_prueba)

    def test_validacion_datos_usuario(self):
        """Prueba la validación de datos de usuario"""
        # Prueba nombre inválido
        with self.assertRaises(DatosInvalidosError):
            validar_datos_usuario("", "correo@ejemplo.com", "1234567890")
        
        # Prueba correo inválido
        with self.assertRaises(DatosInvalidosError):
            validar_datos_usuario("Juan Pérez", "correo_invalido", "1234567890")
        
        # Prueba teléfono inválido
        with self.assertRaises(DatosInvalidosError):
            validar_datos_usuario("Juan Pérez", "correo@ejemplo.com", "abc")

    def test_registro_medidas(self):
        """Prueba el registro de medidas"""
        self.usuario_prueba.registrar_medidas(70.5, 1.75)
        self.assertEqual(len(self.usuario_prueba.medidas), 1)
        
        # Prueba medidas inválidas
        with self.assertRaises(ValueError):
            self.usuario_prueba.registrar_medidas(-70, 1.75)

    def test_membresia(self):
        """Prueba las operaciones de membresía"""
        # Prueba congelar membresía
        self.usuario_prueba.congelar_membresia()
        self.assertEqual(self.usuario_prueba.membresia, "Congelada")
        
        # Prueba activar membresía
        self.usuario_prueba.activar_membresia()
        self.assertEqual(self.usuario_prueba.membresia, "Activa")

    def test_registro_asistencia(self):
        """Prueba el registro de asistencia"""
        self.gimnasio.agregar_usuario(self.usuario_prueba)
        fecha_actual = datetime.now()
        
        self.gimnasio.registrar_ingreso(
            self.usuario_prueba.id_usuario,
            fecha_actual.date(),
            fecha_actual,
            fecha_actual.replace(hour=fecha_actual.hour + 1)
        )
        
        self.assertEqual(len(self.usuario_prueba.registro_ingreso), 1)

    def test_busqueda_usuarios(self):
        """Prueba la búsqueda de usuarios"""
        self.gimnasio.agregar_usuario(self.usuario_prueba)
        
        # Búsqueda por nombre
        resultados = self.gimnasio.buscar_usuarios('nombre', 'Juan')
        self.assertEqual(len(resultados), 1)
        
        # Búsqueda por membresía
        resultados = self.gimnasio.buscar_usuarios('membresia', 'Activa')
        self.assertEqual(len(resultados), 1)

    def test_estadisticas(self):
        """Prueba la generación de estadísticas"""
        self.gimnasio.agregar_usuario(self.usuario_prueba)
        stats = self.gimnasio.obtener_estadisticas()
        
        self.assertEqual(stats['total_usuarios'], 1)
        self.assertEqual(stats['usuarios_activos'], 1)
        self.assertEqual(stats['usuarios_congelados'], 0)

    def test_eliminar_usuario(self):
        """Prueba la eliminación de usuarios"""
        self.gimnasio.agregar_usuario(self.usuario_prueba)
        self.gimnasio.eliminar_usuario(self.usuario_prueba.id_usuario)
        
        self.assertNotIn(self.usuario_prueba.id_usuario, self.gimnasio.usuarios)
        
        # Prueba eliminar usuario inexistente
        with self.assertRaises(ValueError):
            self.gimnasio.eliminar_usuario("usuario_inexistente")

if __name__ == '__main__':
    unittest.main()