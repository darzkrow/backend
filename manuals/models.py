from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver 
from django.db import models
from django.utils import timezone
from auditlog.registry import auditlog

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Categoría")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['name']
    def __str__(self):
        return self.name
auditlog.register(Category)

class Manual(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título del Manual")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción General")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='manuals', verbose_name="Categoría")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Manual"
        verbose_name_plural = "Manuales"
        ordering = ['title']

    def __str__(self):
        return self.title    
auditlog.register(Manual)

class Procedure(models.Model):
    manual = models.ForeignKey(Manual, on_delete=models.CASCADE, related_name='procedures', verbose_name="Manual Asociado")
    title = models.CharField(max_length=200, verbose_name="Título del Procedimiento")
    content = models.TextField(verbose_name="Contenido del Procedimiento")
    version = models.CharField(max_length=50, default="1.0", verbose_name="Versión")
    last_reviewed = models.DateField(default=timezone.now, verbose_name="Última Revisión")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Procedimiento"
        verbose_name_plural = "Procedimientos"
        unique_together = ('manual', 'title', 'version') 
        ordering = ['manual__title', 'title', '-version']

    def __str__(self):
        return f"{self.title} (v{self.version}) - {self.manual.title}"
auditlog.register(Procedure)


class DocumentFile(models.Model):

    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE, related_name='document_files')
    title = models.CharField(max_length=255, help_text="Título del documento (constante a través de versiones)")
    file = models.FileField(upload_to='document_files/')
    description = models.CharField(max_length=255, blank=True, null=True, 
                                   help_text="Descripción de esta versión específica")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='uploaded_document_files')
    version_number = models.PositiveIntegerField(default=1)
    is_latest = models.BooleanField(default=True)
    previous_version = models.OneToOneField('self', on_delete=models.SET_NULL, null=True, blank=True, 
                                            related_name='next_version', help_text="Versión anterior en el historial")
    class Meta:
        ordering = ['-version_number', '-uploaded_at'] 
        verbose_name = "Archivo Adjunto"
        verbose_name_plural = "Archivos Adjuntos"     
    def __str__(self):
        return f"{self.procedure.title} - {self.title} (v{self.version_number})"
auditlog.register(DocumentFile)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return f'Perfil de {self.user.username}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
auditlog.register(Profile)