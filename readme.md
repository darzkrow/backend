# Nombre del Proyecto: Manuales Empresariales (o el nombre real de tu App)

## 🚀 Visión General del Proyecto

Este proyecto es un sistema integral para la gestión de manuales empresariales, compuesto por un backend robusto desarrollado en Django y una aplicación móvil intuitiva creada con Flutter. Permite a los usuarios organizar, buscar y acceder fácilmente a políticas, procedimientos, guías y otros documentos importantes de la empresa.

## 🛠️ Tecnologías Utilizadas

### Backend (Django REST Framework)
* **Lenguaje:** Python 3.x
* **Framework:** Django 5.x
* **API:** Django REST Framework
* **Base de Datos:** SQLite (desarrollo), PostgreSQL/MySQL (producción)
* **Autenticación:** JWT (JSON Web Tokens)
* **CORS:** django-cors-headers
* **Logging:** loguru (o la que uses, si aplicara)

### Frontend (Flutter)
* **Lenguaje:** Dart 3.x
* **Framework:** Flutter 3.x
* **Estado:** Provider / ChangeNotifier (o GetX/Bloc/Riverpod si usas otro)
* **Navegación:** GoRouter
* **HTTP Client:** Dio
* **Almacenamiento Seguro:** flutter_secure_storage
* **Lanzador de URLs:** url_launcher
* **Modelos de Datos:** Equatable

## ⚙️ Configuración del Entorno

### 1. Backend (Django REST Framework)

#### Requisitos
* Python 3.8+
* pip (gestor de paquetes de Python)

#### Pasos de Configuración
1.  **Clonar el Repositorio:**
    ```bash
    git clone [URL_DE_TU_REPOSITORIO_DJANGO]
    cd [nombre_de_tu_carpeta_django] # Ej: manuals_api
    ```
2.  **Crear y Activar un Entorno Virtual (recomendado):**
    ```bash
    python -m venv venv
    # En Windows:
    .\venv\Scripts\activate
    # En macOS/Linux:
    source venv/bin/activate
    ```
3.  **Instalar Dependencias:**
    ```bash
    pip install -r requirements.txt # Asegúrate de tener un archivo requirements.txt actualizado
    ```
    Si no tienes `requirements.txt`, instala manualmente:
    ```bash
    pip install Django djangorestframework django-cors-headers djangorestframework-simplejwt # y cualquier otra que uses
    ```
4.  **Configuración de Base de Datos:**
    El proyecto está configurado por defecto para usar **SQLite** en desarrollo. Si deseas usar otra base de datos (ej. PostgreSQL), modifica `DATABASES` en `manuals_api/settings.py`.
    ```python
    # manuals_api/settings.py
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    ```
5.  **Ejecutar Migraciones:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
6.  **Crear Superusuario (para acceder al panel de administración):**
    ```bash
    python manage.py createsuperuser
    ```
7.  **Cargar Datos de Prueba (Categorías, Manuales, Procedimientos):**
    Si no usas fixtures de Django, puedes insertar los datos manualmente usando `dbshell`. Asegúrate de que los `category_id` y `manual_id` en tus sentencias SQL sean válidos.

    * **Acceder a la shell de la DB:**
        ```bash
        python manage.py dbshell
        ```
    * **Insertar Categorías:**
        ```sql
        -- Usar el SQL corregido de la conversación (ej. incluyendo created_at y updated_at):
        INSERT INTO categorias (name, created_at, updated_at) VALUES
        ('Administración', datetime('now'), datetime('now')),
        ('Recursos Humanos (RRHH)', datetime('now'), datetime('now')),
        ('Finanzas', datetime('now'), datetime('now')),
        ('Legal', datetime('now'), datetime('now')),
        ('Marketing y Ventas', datetime('now'), datetime('now')),
        ('Compras / Adquisiciones', datetime('now'), datetime('now')),
        ('Logística', datetime('now'), datetime('now')),
        ('Contabilidad', datetime('now'), datetime('now')),
        ('Operaciones', datetime('now'), datetime('now')),
        ('Producción', datetime('now'), datetime('now')),
        ('Mantenimiento', datetime('now'), datetime('now')),
        ('Calidad', datetime('now'), datetime('now')),
        ('Seguridad y Salud Ocupacional (SSO)', datetime('now'), datetime('now')),
        ('Tecnología de la Información (TI)', datetime('now'), datetime('now')),
        ('Desarrollo de Producto', datetime('now'), datetime('now')),
        ('Ingeniería', datetime('now'), datetime('now')),
        ('Investigación y Desarrollo (I+D)', datetime('now'), datetime('now')),
        ('Atención al Cliente', datetime('now'), datetime('now')),
        ('Políticas', datetime('now'), datetime('now')),
        ('Procedimientos', datetime('now'), datetime('now')),
        ('Manuales de Usuario', datetime('now'), datetime('now')),
        ('Manuales Técnicos', datetime('now'), datetime('now')),
        ('Reglamentos', datetime('now'), datetime('now')),
        ('Formularios', datetime('now'), datetime('now')),
        ('Reportes', datetime('now'), datetime('now')),
        ('Guías', datetime('now'), datetime('now')),
        ('Contratos', datetime('now'), datetime('now')),
        ('Acuerdos', datetime('now'), datetime('now')),
        ('Planes', datetime('now'), datetime('now')),
        ('Certificaciones', datetime('now'), datetime('now')),
        ('Auditorías', datetime('now'), datetime('now'));
        ```
    * **Insertar Manuales:**
        ```sql
        -- Usar el SQL corregido de la conversación (ej. incluyendo created_at y updated_at):
        INSERT INTO manuales (title, description, category_id, created_at, updated_at) VALUES
        ('Manual de Incorporación de Empleados', 'Guía completa para el proceso de onboarding de nuevos talentos.', 1, datetime('now'), datetime('now')),
        ('Procedimiento de Gestión de Gastos', 'Detalla el proceso para solicitar y aprobar reembolsos de gastos.', 3, datetime('now'), datetime('now')),
        ('Manual de Seguridad Informática', 'Directrices y políticas para proteger los sistemas y datos de la empresa.', 14, datetime('now'), datetime('now')),
        ('Guía de Primeros Auxilios en la Oficina', 'Instrucciones básicas para emergencias médicas en el lugar de trabajo.', 13, datetime('now'), datetime('now')),
        ('Política de Teletrabajo', 'Normativa y condiciones para la modalidad de trabajo remoto.', 1, datetime('now'), datetime('now')),
        ('Manual de Uso del Sistema CRM', 'Instrucciones paso a paso para operar la plataforma de gestión de clientes.', 18, datetime('now'), datetime('now')),
        ('Procedimiento de Control de Calidad de Producto X', 'Pasos para asegurar la calidad en la producción del Producto X.', 12, datetime('now'), datetime('now')),
        ('Manual de Mantenimiento Preventivo de Equipos', 'Programa y checklist para el mantenimiento periódico de maquinaria.', 11, datetime('now'), datetime('now')),
        ('Políticas de Privacidad de Datos (RGPD)', 'Documento legal sobre el manejo y protección de datos personales.', 4, datetime('now'), datetime('now')),
        ('Guía de Marketing Digital para Nuevos Proyectos', 'Estrategias y herramientas para la promoción online de lanzamientos.', 5, datetime('now'), datetime('now')),
        ('Manual de Integración de Nuevos Desarrolladores', 'Pasos para configurar el entorno y empezar a contribuir al código base.', 14, datetime('now'), datetime('now')),
        ('Procedimiento de Cierre Contable Mensual', 'Pasos detallados para el cierre de cuentas y generación de informes financieros.', 8, datetime('now'), datetime('now')),
        ('Manual de Gestión de Proyectos Ágiles', 'Metodologías y buenas prácticas para la gestión de proyectos con Scrum.', 16, datetime('now'), datetime('now')),
        ('Guía Rápida para Entrevistas de Selección', 'Consejos y preguntas clave para los reclutadores.', 2, datetime('now'), datetime('now')),
        ('Reglamento Interno de Trabajo', 'Normas que rigen las relaciones laborales dentro de la empresa.', 23, datetime('now'), datetime('now'));
        ```
    * **Insertar Procedimientos:**
        ```sql
        -- Usar el SQL corregido de la conversación (ej. incluyendo version, last_reviewed, created_at, updated_at):
        INSERT INTO procedimientos (manual_id, title, content, version, last_reviewed, created_at, updated_at) VALUES
        (1, 'Paso 1: Bienvenida al Nuevo Empleado', 'Descripción detallada de la bienvenida y entrega de documentos iniciales.', '1.0', date('now'), datetime('now'), datetime('now')),
        (1, 'Paso 2: Configuración de Entorno de Trabajo', 'Guía para la instalación de software y acceso a sistemas.', '1.0', date('now'), datetime('now'), datetime('now')),
        (1, 'Paso 3: Inducción a la Cultura Organizacional', 'Charlas y materiales sobre valores y misión de la empresa.', '1.0', date('now'), datetime('now'), datetime('now')),
        (2, 'Envío de Solicitud de Reembolso', 'Proceso para completar y enviar el formulario de reembolso.', '1.0', date('now'), datetime('now'), datetime('now')),
        (2, 'Aprobación de Reembolso por Gerencia', 'Pasos que sigue la gerencia para revisar y aprobar las solicitudes.', '1.0', date('now'), datetime('now'), datetime('now')),
        (3, 'Directriz de Contraseñas Seguras', 'Cómo crear y gestionar contraseñas robustas y seguras para proteger la información.', '1.0', date('now'), datetime('now'), datetime('now')),
        (3, 'Identificación de Phishing y Malware', 'Guía para reconocer y reportar intentos de fraude o software malicioso.', '1.0', date('now'), datetime('now'), datetime('now')),
        (3, 'Copia de Seguridad de Datos Sensibles', 'Procedimiento para realizar backups periódicos de información crítica.', '1.0', date('now'), datetime('now'), datetime('now')),
        (4, 'Manejo de Cortes y Heridas Menores', 'Instrucciones para la limpieza y vendaje de heridas pequeñas.', '1.0', date('now'), datetime('now'), datetime('now')),
        (4, 'Actuación ante Quemaduras Leves', 'Protocolo de primeros auxilios para quemaduras de primer grado.', '1.0', date('now'), datetime('now'), datetime('now')),
        (5, 'Requisitos Técnicos para Conexión Remota', 'Lista de hardware, software y velocidad de internet recomendada.', '1.0', date('now'), datetime('now'), datetime('now')),
        (6, 'Creación de Nuevo Cliente en CRM', 'Pasos para el registro de un nuevo cliente y sus datos de contacto en el sistema.', '1.0', date('now'), datetime('now'), datetime('now')),
        (6, 'Registro de Interacciones con Clientes', 'Cómo documentar llamadas, correos y reuniones en el historial del cliente.', '1.0', date('now'), datetime('now'), datetime('now')),
        (7, 'Inspección Visual del Producto Terminado', 'Criterios y puntos de control para la inspección visual del Producto X.', '1.0', date('now'), datetime('now'), datetime('now')),
        (8, 'Chequeo Semanal de Maquinaria Pesada', 'Lista de verificación de componentes y lubricación para mantenimiento preventivo.', '1.0', date('now'), datetime('now'), datetime('now')),
        (9, 'Manejo de Solicitudes de Derechos de Datos', 'Proceso para atender solicitudes de acceso, rectificación o eliminación de datos personales.', '1.0', date('now'), datetime('now'), datetime('now')),
        (10, 'Creación de Contenido para Redes Sociales', 'Estrategias y ejemplos para desarrollar publicaciones efectivas en plataformas digitales.', '1.0', date('now'), datetime('now'), datetime('now')),
        (11, 'Configuración del Entorno de Desarrollo', 'Pasos detallados para instalar herramientas, IDE y repositorios de código.', '1.0', date('now'), datetime('now'), datetime('now')),
        (12, 'Reconciliación de Cuentas Bancarias', 'Proceso para comparar y ajustar los registros contables con los extractos bancarios.', '1.0', date('now'), datetime('now'), datetime('now'));
        ```
    * **Salir de la shell de la DB:** `CTRL+D` (Linux/macOS) o `CTRL+Z` y Enter (Windows).

8.  **Configuración de CORS:**
    Asegúrate de que `django-cors-headers` esté en `INSTALLED_APPS` y `MIDDLEWARE`.
    Modifica `CORS_ALLOWED_ORIGINS` en `manuals_api/settings.py` para permitir conexiones desde tu aplicación Flutter (especialmente para desarrollo):
    ```python
    # manuals_api/settings.py
    CORS_ALLOWED_ORIGINS = [
        "http://localhost",        # Para desarrollo local (cualquier puerto)
        "[http://127.0.0.1](http://127.0.0.1)",        # Para desarrollo local (cualquier puerto)
        # Agrega la IP de tu máquina si usas un dispositivo físico en la misma red
        # "[http://192.168.](http://192.168.)X.X",
        # Para emuladores Android que se conectan al localhost de tu PC
        # "[http://10.0.2.2](http://10.0.2.2)",
    ]
    # MUY IMPORTANTE: Solo para desarrollo. Comentar o poner a False en producción.
    CORS_ALLOW_ALL_ORIGINS = True
    ```
9.  **Servir Archivos de Medios en Desarrollo:**
    Asegúrate de que tus `MEDIA_URL` y `MEDIA_ROOT` estén definidos y que se sirvan en `urls.py` para poder acceder a los archivos adjuntos.
    ```python
    # manuals_api/settings.py
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

    # manuals_api/urls.py (principal)
    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns = [
        # ... tus otras urls ...
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    ```
10. **Iniciar el Servidor de Desarrollo:**
    ```bash
    python manage.py runserver
    # O para que sea accesible desde otros dispositivos/emuladores:
    # python manage.py runserver 0.0.0.0:8000
    ```
    El API estará disponible en `http://127.0.0.1:8000/` (o la IP que uses).

### 2. Frontend (Flutter)

#### Requisitos
* Flutter SDK instalado (versión 3.x recomendada)
* Android Studio / VS Code con los plugins de Flutter/Dart

#### Pasos de Configuración
1.  **Clonar el Repositorio:**
    ```bash
    git clone [URL_DE_TU_REPOSITORIO_FLUTTER]
    cd [nombre_de_tu_carpeta_flutter] # Ej: manual_app_flutter
    ```
2.  **Obtener Dependencias:**
    ```bash
    flutter pub get
    ```
3.  **Configurar la URL Base de la API:**
    Abre `lib/core/services/api_service.dart` (o donde definas tu URL base) y asegúrate de que `_baseUrl` apunte a tu servidor Django.
    ```dart
    // lib/core/services/api_service.dart
    const String _baseUrl = '[http://192.168.30.106:8000/api/v1](http://192.168.30.106:8000/api/v1)'; // <-- Ajusta a la IP real de tu servidor Django
    // O para emuladores Android:
    // const String _baseUrl = '[http://10.0.2.2:8000/api/v1](http://10.0.2.2:8000/api/v1)';
    ```
4.  **Configuración de `url_launcher` (Android):**
    Para Android 11+ (`API 30+`), necesitas añadir `queries` en tu `AndroidManifest.xml` para que `url_launcher` pueda abrir otras apps (navegadores, visores de documentos).

    ```xml
    <manifest ...>
        <queries>
            <intent>
                <action android:name="android.intent.action.VIEW" />
                <category android:name="android.intent.category.BROWSABLE" />
                <data android:scheme="https" />
            </intent>
            <intent>
                <action android:name="android.intent.action.VIEW" />
                <data android:mimeType="*/*" />
            </intent>
        </queries>
        <application android:usesCleartextTraffic="true" ...> </application>
    </manifest>
    ```
5.  **Instalar Visor de Documentos (Emulador/Dispositivo de Prueba):**
    Para abrir archivos `.docx`, `.pdf`, etc., asegúrate de tener una aplicación de oficina (ej. Google Docs, WPS Office) instalada en tu emulador o dispositivo físico.

6.  **Ejecutar la Aplicación:**
    ```bash
    flutter run
    ```
    Si tienes varios dispositivos/emuladores, especifica uno:
    ```bash
    flutter run -d [nombre_del_dispositivo]
    ```

## 🔐 Autenticación

El sistema utiliza autenticación basada en JWT.

* **Inicio de Sesión:** Los usuarios pueden iniciar sesión con sus credenciales.
* **"Recordar Credenciales":** La aplicación implementa una funcionalidad de "recordar credenciales" utilizando `flutter_secure_storage` para almacenar de forma segura el token JWT del usuario. Esto permite un inicio de sesión automático en futuras aperturas de la aplicación, si el usuario opta por ello.
* **Cierre de Sesión:** Al cerrar sesión, el token almacenado localmente es eliminado.

## 📦 Estructura de la API (Endpoints Principales)

Aquí se describen los endpoints más relevantes de la API de Django:

### Autenticación
* `POST /api/v1/auth/login/`: Iniciar sesión.
    * **Parámetros:** `username` (string), `password` (string).
    * **Respuesta:** `{"access": "jwt_token", "refresh": "refresh_token"}`.

### Categorías
* `GET /api/v1/categories/`: Obtener una lista de todas las categorías.
    * **Respuesta:** `[{"id": 1, "name": "Recursos Humanos"}, ...]`

### Manuales
* `GET /api/v1/manuals/`: Obtener una lista de todos los manuales. Incluye la categoría anidada.
    * **Respuesta:** `[{"id": 1, "title": "Manual de RRHH", "description": "...", "category": {"id": 1, "name": "Recursos Humanos"}, "procedures": [{"id": 101, "title": "...", ...}], ...}, ...]`
* `GET /api/v1/manuals/<id>/`: Obtener los detalles de un manual específico, incluyendo sus procedimientos anidados.
    * **Respuesta:** `{"id": 1, "title": "...", "procedures": [{"id": 101, "title": "...", "document_files": [...], ...}], ...}`

### Procedimientos
* `GET /api/v1/procedures/`: Obtener una lista de todos los procedimientos (puede ser útil para búsquedas generales).
* `GET /api/v1/procedures/<id>/`: Obtener los detalles de un procedimiento específico, incluyendo sus archivos adjuntos.
    * **Respuesta:** `{"id": 101, "title": "...", "manual": 1, "document_files": [{"id": 1, "title": "Acta", "file": "http://...", ...}], ...}`

### Archivos de Documentos
* `GET /api/v1/document_files/<id>/`: Obtener los detalles de un archivo adjunto.
    * **Respuesta:** `{"id": 1, "title": "Acta de Reunión", "file": "http://127.0.0.1:8000/media/document_files/acta.pdf", "uploaded_at": "...", "version_number": 1, "procedure": 101}`
    * **Nota:** La URL del archivo (`file`) es absoluta para permitir su descarga/visualización directa.

---

## 🤝 Contribución

Si deseas contribuir a este proyecto, por favor, sigue las siguientes pautas:
1.  Haz un "fork" del repositorio.
2.  Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3.  Realiza tus cambios y commitea (`git commit -m 'feat: Añadir nueva funcionalidad X'`).
4.  Haz un "push" a tu rama (`git push origin feature/nueva-funcionalidad`).
5.  Abre un "Pull Request" en el repositorio original.

## 📧 Contacto

Para cualquier pregunta o sugerencia, puedes contactar a:

* [Tu Nombre/Email o el del Equipo]