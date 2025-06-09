from django.contrib import admin

# Register your models here.
# manuals/admin.py
from django.utils.html import mark_safe
from .models import Category, Manual, Procedure, DocumentFile, Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group # Importa Group


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name',)

class ProcedureInline(admin.TabularInline):
    model = Procedure
    extra = 0 # Number of empty forms to display

class DocumentFileInline(admin.TabularInline):
    model = DocumentFile
    extra = 0

@admin.register(Manual)
class ManualAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'description', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('category',)
    inlines = [ProcedureInline] # Permite gestionar procedimientos directamente desde el manual

@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = ('title', 'manual', 'version', 'last_reviewed', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('manual', 'version')
    inlines = [DocumentFileInline] # Permite gestionar archivos adjuntos directamente desde el procedimiento
    fieldsets = (
        (None, {
            'fields': ('manual', 'title', 'content')
        }),
        ('Información de Versión y Revisión', {
            'fields': ('version', 'last_reviewed')
        }),
    )




@admin.register(DocumentFile)
class DocumentFileAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'procedure', 'file_name', 'version_number', 
        'is_latest', 'uploaded_by', 'uploaded_at', 'previous_version_link'
    )
    list_filter = ('procedure', 'uploaded_at', 'is_latest')
    search_fields = ('title', 'description', 'procedure__title', 'uploaded_by__username')
    raw_id_fields = ('procedure', 'uploaded_by', 'previous_version') # Útil para buscar IDs

    fields = (
        'procedure', 'title', 'description', 'file', 
        'uploaded_by', 
        'version_number', 'is_latest', 'previous_version'
    )
    
    readonly_fields = (
        'uploaded_by', 'version_number', 'is_latest', 'previous_version', 
        'uploaded_at', 'file_name'
    )

    def file_name(self, obj):
        return obj.file.name.split('/')[-1] if obj.file else "No file"
    file_name.short_description = 'File Name'

    def previous_version_link(self, obj):
        if obj.previous_version:
            from django.urls import reverse
            url = reverse("admin:manuals_documentfile_change", args=[obj.previous_version.id])
            return mark_safe(f'<a href="{url}">v{obj.previous_version.version_number}</a>')
        return "-"
    previous_version_link.short_description = 'Previous Version'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('uploaded_by', 'procedure')


    def save_model(self, request, obj, form, change):
        if not change and not obj.uploaded_by:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

class DocumentFileInline(admin.TabularInline):
    model = DocumentFile

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_latest=True) 
    extra = 1
    fields = ('title', 'description', 'file', 'uploaded_by', 'version_number', 'is_latest', 'previous_version')
    readonly_fields = ('uploaded_by', 'version_number', 'is_latest', 'previous_version')



# --- Definir el Inline para el Perfil ---
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Información de Perfil'
    fields = (
        'avatar',
        'avatar_preview',
        'bio',
        ('phone_number', 'address'),
    )
    readonly_fields = ('avatar_preview',) 

    def avatar_preview(self, obj):
        if obj.avatar:
            return mark_safe(f'<img src="{obj.avatar.url}" width="100" height="100" />')
        return "No hay avatar"
    avatar_preview.short_description = 'Previsualización del Avatar'

admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    
    list_display = BaseUserAdmin.list_display + ('get_groups',)
    filter_horizontal = BaseUserAdmin.filter_horizontal + ('groups', 'user_permissions',)
    inlines = (ProfileInline,)

    # --- CAMPOS PARA LA PÁGINA DE EDICIÓN DE USUARIOS EXISTENTES ---
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}), 
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # --- CAMPOS PARA LA PÁGINA DE AGREGAR NUEVOS USUARIOS ---
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', 'password2'), 
        }),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
    )

    def get_groups(self, obj):
        return ", ".join([g.name for g in obj.groups.all()])
    get_groups.short_description = 'Grupos'