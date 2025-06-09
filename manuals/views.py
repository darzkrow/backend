# manuals/views.py
from rest_framework.throttling import UserRateThrottle
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny # Importa IsAuthenticated y AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Manual, Procedure, DocumentFile
from .permissions import IsAdminOrReadOnly, IsEditor, IsViewer # Importa tus permisos personalizados
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import CategorySerializer, ManualSerializer,ManualListSerializer, UserProfileSerializer,ProcedureSerializer, DocumentFileSerializer, UserRegisterSerializer # Importa tu nuevo serializador

from rest_framework.parsers import MultiPartParser, FormParser # Para manejar subida de archivos
from rest_framework.decorators import action

from rest_framework import filters


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()   
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly] # Solo admins pueden crear/editar, otros solo leer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']

class ManualViewSet(viewsets.ModelViewSet):
    throttle_classes = [UserRateThrottle]
   # queryset = Manual.objects.all()
    queryset = Manual.objects.all().select_related('category')
    def get_serializer_class(self):
        if self.action == 'list':
            return ManualListSerializer
        return ManualSerializer
    serializer_class = ManualSerializer
    permission_classes = [IsAdminOrReadOnly] # Solo admins pueden crear/editar, otros solo leer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'created_at']
   

class ProcedureViewSet(viewsets.ModelViewSet):
    # queryset = Procedure.objects.all()
    queryset = Procedure.objects.all().select_related('manual').prefetch_related('document_files')
    serializer_class = ProcedureSerializer
    # Solo editores pueden crear/editar/eliminar, admins también, visualizadores solo leer.
    # El orden importa: se evalúan en orden. Si IsEditor falla, IsAdminOrReadOnly se evalúa.
    permission_classes = [IsEditor | IsAdminOrReadOnly] # O IsAdminUser para simplificar el admin
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['manual', 'version', 'last_reviewed']
    search_fields = ['title', 'content']
    ordering_fields = ['title', 'version', 'last_reviewed', 'created_at']

# class DocumentFileViewSet(viewsets.ModelViewSet):
#     queryset = DocumentFile.objects.all()
#     serializer_class = DocumentFileSerializer
#     permission_classes = [IsEditor | IsAdminOrReadOnly] # Similares a ProcedureViewSet
#     filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
#     filterset_fields = ['procedure']
#     search_fields = ['description', 'file__name']
#     ordering_fields = ['uploaded_at']








class DocumentFileViewSet(viewsets.ModelViewSet):
    queryset = DocumentFile.objects.all()
    serializer_class = DocumentFileSerializer
    parser_classes = (MultiPartParser, FormParser) # Para recibir archivos
    permission_classes = [IsAuthenticated] # Ajusta permisos según tu lógica

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['procedure']
    search_fields = ['title', 'description']
    ordering_fields = ['uploaded_at', 'version_number']

    def get_queryset(self):
        # Por defecto, solo mostrar la última versión de cada documento
        queryset = super().get_queryset().filter(is_latest=True).select_related('uploaded_by')
        # Puedes añadir más filtros aquí, ej. por `procedure_id` si el ViewSet no es anidado
        return queryset

    def perform_create(self, serializer):
        # Al crear un nuevo archivo (primera versión), se establece como la última.
        serializer.save(uploaded_by=self.request.user, version_number=1, is_latest=True)

    def perform_update(self, serializer):
        # Esta es la lógica clave para el versionado
        instance = self.get_object() # La DocumentFile actual que se está actualizando
        
        # Obtenemos los datos del request. Los archivos están en request.FILES
        new_file = self.request.FILES.get('file')
        
        if new_file:
            # Si se ha subido un NUEVO archivo:
            # 1. Marcar la versión actual como NO la más reciente
            instance.is_latest = False
            instance.save(update_fields=['is_latest']) # Guardar solo este campo

            # 2. Crear una NUEVA instancia de DocumentFile para la nueva versión
            new_version_data = serializer.validated_data # Datos validados del request
            
            # Aseguramos que los campos 'file' no estén en validated_data para evitar conflicto
            # ya que lo vamos a pasar directamente a la nueva_version.file
            if 'file' in new_version_data:
                new_version_data.pop('file')

            # Copiar datos relevantes de la versión anterior a la nueva
            new_version_instance = DocumentFile(
                procedure=instance.procedure,
                title=new_version_data.get('title', instance.title), # Usa nuevo título o el anterior
                description=new_version_data.get('description', instance.description), # Nueva descripción o anterior
                file=new_file, # El nuevo archivo subido
                uploaded_by=self.request.user,
                version_number=instance.version_number + 1, # Incrementa la versión
                is_latest=True, # Esta es la nueva última versión
                previous_version=instance # Enlaza a la versión anterior (la que era "latest")
            )
            new_version_instance.save()
            serializer.instance = new_version_instance # Actualiza la instancia del serializador para la respuesta
        else:
            # Si NO se sube un nuevo archivo, solo se actualizan los metadatos de la versión actual
            # Aquí se asume que solo se permite actualizar metadatos si no se sube un nuevo archivo
            # Si se permite actualizar metadatos y el archivo, la lógica sería más compleja
            super().perform_update(serializer) # Actualiza la instancia actual (metadata)

    # --- Acción personalizada para obtener el historial de un documento ---
    @action(detail=True, methods=['get'], url_path='history')
    def history(self, request, pk=None):
        document_file = self.get_object() # Obtiene la versión actual (is_latest=True)

        # Recopila todas las versiones anteriores de esta "serie" de documentos
        versions = [document_file]
        current_version = document_file.previous_version
        while current_version:
            versions.append(current_version)
            current_version = current_version.previous_version
        
        # Ordena las versiones de la más reciente a la más antigua para el historial
        versions.sort(key=lambda x: x.version_number, reverse=True)

        # Opcional: Podrías querer incluir la siguiente versión para visualización en el historial también
        # if document_file.next_version: # Si existe una 'next_version'
        #     # Manejar lógica si 'next_version' es parte de la cadena o para mostrar futuros cambios
        #     pass

        serializer = DocumentFileHistorySerializer(versions, many=True, context={'request': request})
        return Response(serializer.data)






























# --- Nueva Vista de Registro de Usuario ---
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny] # Permite que usuarios no autenticados accedan a esta vista

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Opcional: Después del registro, puedes loguear al usuario automáticamente
        # y devolver los tokens. Para esto, necesitas importar TokenObtainPairSerializer
        # y configurarlo para devolver los tokens.
        # Por ahora, solo devolveremos un mensaje de éxito.

        # Si quieres auto-login y devolver tokens:
        from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
        token_serializer = TokenObtainPairSerializer(data={
            'username': user.username,
            'password': request.data['password'] # Usa la contraseña directamente
        })
        token_serializer.is_valid(raise_exception=True)
        tokens = token_serializer.validated_data

        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "message": "Usuario registrado exitosamente.",
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                **tokens # Incluye los tokens en la respuesta
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated] # Solo usuarios autenticados pueden ver/actualizar su perfil

    def get_object(self):
        # Esta función asegura que el usuario solo pueda ver/editar su propio perfil
        return self.request.user