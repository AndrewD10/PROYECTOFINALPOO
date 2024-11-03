Sistema de Gestión de Gimnasio
Este proyecto implementa un sistema de gestión para un gimnasio, 
compuesto por cuatro módulos principales: exceptions.py, 
gimnasio.py, usuario.py, y main.py. A continuación, 
se proporciona una explicación detallada de cada módulo y su 
función en el sistema.

Módulo: exceptions.py
Este módulo define una jerarquía de excepciones personalizadas y 
funciones de validación para manejar errores específicos del 
sistema de gimnasio.

Excepciones Personalizadas:
GimnasioError: Clase base para todas las excepciones del sistema.
UsuarioError: Clase base para excepciones relacionadas con usuarios.
UsuarioNoEncontradoError: Se lanza cuando no se encuentra un usuario específico.
UsuarioYaExisteError: Se lanza al intentar registrar un usuario que ya existe.
DatosInvalidosError: Se lanza cuando los datos proporcionados son inválidos.
MembresiaError: Para excepciones relacionadas con membresías.
ReporteError: Para excepciones relacionadas con la generación de reportes.
Funciones de Validación:
validar_datos_usuario: Valida el nombre, correo y teléfono del usuario.
validar_medidas: Valida el peso y altura del usuario.
Decorador:
handle_exception: Un decorador para manejar excepciones de manera uniforme en todo el sistema.
Módulo: gimnasio.py
Este módulo implementa la clase Gimnasio, que es el núcleo del sistema de gestión.

Características principales:
Gestión de Usuarios: Permite registrar, buscar y eliminar usuarios.
Gestión de Membresías: Maneja la asignación y renovación de membresías.
Registro de Asistencia: Registra las visitas de los usuarios al gimnasio.
Seguimiento de Progreso: Permite actualizar y consultar las medidas físicas de los usuarios.
Generación de Reportes: Crea informes sobre usuarios activos, ingresos y asistencia.
Métodos Importantes:
Registro y gestión de usuarios
Manejo de membresías
Registro de asistencias
Actualización de medidas físicas
Generación de diversos tipos de reportes
Módulo: usuario.py
Este módulo define la clase Usuario, que representa a un miembro del gimnasio.

Atributos del Usuario:
ID único
Nombre
Correo electrónico
Número de teléfono
Fecha de registro
Tipo de membresía
Fecha de vencimiento de la membresía
Historial de asistencias
Medidas físicas (peso, altura)
Métodos de Usuario:
Actualización de información personal
Registro de asistencias
Actualización de medidas físicas
Renovación de membresía
Módulo: main.py
Este es el punto de entrada principal del sistema, que integra todos los módulos y 
proporciona una interfaz para interactuar con el sistema de 
gestión del gimnasio.

Funcionalidades:
Menú Interactivo: Ofrece opciones para todas las operaciones del gimnasio.
Gestión de Usuarios: Permite registrar nuevos usuarios, buscar y actualizar información existente.
Control de Membresías: Facilita la asignación y renovación de membresías.
Registro de Asistencias: Permite registrar las visitas de los usuarios al gimnasio.
Seguimiento de Progreso: Ofrece opciones para actualizar y consultar medidas físicas.
Generación de Reportes: Permite generar y visualizar diversos tipos de informes.
Flujo de Trabajo:
Inicialización del sistema de gimnasio.
Presentación del menú principal con todas las opciones disponibles.
Manejo de la entrada del usuario y ejecución de las operaciones correspondientes.
Manejo de excepciones y presentación de mensajes de error cuando sea necesario.
Bucle continuo hasta que el usuario decida salir del sistema.