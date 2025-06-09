# manuals_api/manuals_api/middleware.py

from django.conf import settings
from django.http import JsonResponse
import re # Necesario para expresiones regulares, para eximir rutas

class AppKeyMiddleware:
    """
    Middleware personalizado para validar una 'App Key' en los encabezados de la solicitud.
    Asegura que solo las aplicaciones autorizadas puedan acceder a la API REST.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Obtener la clave requerida de las configuraciones de Django
        self.required_app_key = getattr(settings, 'REQUIRED_APP_KEY', None)

        # Rutas que no requieren la App Key.
        # Es crucial eximir los endpoints de autenticación y registro.
        # También el admin de Django, archivos estáticos y de medios.
        self.exempt_paths = [
            # re.compile(r'^/api/v1/token/'),       # Endpoint para obtener tokens (login)
            # re.compile(r'^/api/v1/register/'),    # Endpoint de registro de usuarios
            re.compile(r'^/admin/'),           # Panel de administración de Django
            re.compile(r'^/static/'),          # Servidor de archivos estáticos (para desarrollo)
            re.compile(r'^/media/'),           # Servidor de archivos de medios (para desarrollo)
            re.compile(r'^/api/schema/'),      # Si tienes documentación OpenAPI/Swagger
        ]

    def __call__(self, request):
        # 1. Manejar solicitudes OPTIONS (preflight de CORS)
        # Las solicitudes OPTIONS no suelen llevar el encabezado de autenticación
        # y deben ser respondidas sin validación de App Key para que CORS funcione.
        if request.method == 'OPTIONS':
            return self.get_response(request)

        # 2. Excluir rutas exentas de la verificación de App Key
        for pattern in self.exempt_paths:
            if pattern.match(request.path):
                return self.get_response(request)

        # 3. Aplicar la verificación de App Key solo a las rutas /api/ (no exentas)
        # Esto previene que el middleware intente validar la clave para rutas no API.
        if request.path.startswith('/api/'):
            provided_app_key = request.headers.get('X-App-Key') # El encabezado que tu APK enviará

            # Comprobar si la clave requerida está configurada en settings.py
            if not self.required_app_key:
                # Esto es un error de configuración.
                # En producción, esto debería ser un error fatal o un log muy visible.
                print("ADVERTENCIA: REQUIRED_APP_KEY no está definida en settings.py. El middleware de App Key es ineficaz.")
                return JsonResponse(
                    {"detail": "Error de configuración del servidor: clave de aplicación no definida."},
                    status=500
                )

            # Validar si la clave proporcionada coincide con la clave requerida
            if not provided_app_key or provided_app_key != self.required_app_key:
                return JsonResponse(
                    {"detail": "Acceso no autorizado. Clave de aplicación inválida o faltante."},
                    status=401 # 401 Unauthorized es una respuesta estándar para credenciales faltantes/inválidas
                )
        
        # Si la clave es válida o la ruta está exenta, pasar la solicitud al siguiente middleware/vista
        response = self.get_response(request)
        return response