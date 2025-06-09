# manuals/signals.py

from django.contrib.auth.signals import user_login_failed
from django.dispatch import receiver
from auditlog.models import LogEntry # Para poder registrarlo como una entrada de log si lo deseas
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
import json # Para guardar detalles del error

@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, **kwargs):
    """
    Registra un intento de login fallido en LogEntry.
    """
    username = credentials.get('username', 'N/A')
    
    # Intenta encontrar el usuario, si existe
    user = None
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        pass 
    action = LogEntry.Action.ACCESS 
    message = f"Failed login attempt for username: '{username}'"
    
    # Detalle adicional si lo quieres más específico
    change_json = json.dumps({'details': 'Incorrect username or password'})

    LogEntry.objects.create(
        content_type=ContentType.objects.get_for_model(User),
        object_pk=str(user.pk) if user else None, 
        object_repr=str(user) if user else username, 
        action=action,
        timestamp=kwargs.get('timestamp'),
        actor=None, 
        changes=change_json,
        remote_addr=kwargs.get('request').META.get('REMOTE_ADDR') if 'request' in kwargs and kwargs.get('request') else None,

    )
    print(f"AUDITLOG: Failed login attempt for username: {username}") 