from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Category, Manual, Procedure, DocumentFile, Profile

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class UserSerializerForDocument(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class DocumentFileSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializerForDocument(read_only=True)
    file_url = serializers.SerializerMethodField()
    class Meta:
        model = DocumentFile
        fields = '__all__'
        # fields = [
        #     'procedure', 'title', 'description', 'file', 
        #     'uploaded_at', 'uploaded_by', 'version_number', 
        #     'is_latest', 'previous_version'
        # ]
        read_only_fields = ['uploaded_at', 'uploaded_by', 'version_number', 'is_latest', 'previous_version']
        extra_kwargs = {
            'file': {'required': True}
        }
    def get_file_url(self, obj):
       
        if obj.file:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None
    def get_file_url(self, obj):
            if obj.file:
                return self.context['request'].build_absolute_uri(obj.file.url)
            return None



class DocumentFileHistorySerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializerForDocument(read_only=True)

    class Meta:
        model = DocumentFile
        fields = '__all__'
        read_only_fields = fields 


class ProcedureSerializer(serializers.ModelSerializer):
    files = DocumentFileSerializer(many=True, read_only=True)
    document_files = DocumentFileSerializer(many=True, read_only=True) 

    class Meta:
        model = Procedure
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class ManualSerializer(serializers.ModelSerializer):
    procedures = ProcedureSerializer(many=True, read_only=True) # Para incluir procedimientos en el manual
    category = CategorySerializer(read_only=True)# Para mostrar el nombre de la categoría
   

    class Meta:
        model = Manual
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
class ManualListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    class Meta:
        model = Manual
        fields = '__all__'

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=False, allow_blank=True) 
    last_name = serializers.CharField(required=False, allow_blank=True)   
    avatar = serializers.ImageField(required=False, allow_null=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password2',
            'first_name', 'last_name',
            'avatar', 'bio', 'phone_number', 'address'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "Este nombre de usuario ya está en uso."})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Este email ya está registrado."})
        return data

    def create(self, validated_data):
        profile_data = {}
        for field_name in ['avatar', 'bio', 'phone_number', 'address']:
            if field_name in validated_data:
                profile_data[field_name] = validated_data.pop(field_name)

        first_name = validated_data.pop('first_name', '') 
        last_name = validated_data.pop('last_name', '') 

        validated_data.pop('password2')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=first_name,
            last_name=last_name
        )
        if profile_data:
            profile = user.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        try:
            viewer_group = Group.objects.get(name='Visualizadores')
            user.groups.add(viewer_group)
            user.save()
        except Group.DoesNotExist:
            print("El grupo 'Visualizadores' no existe. El usuario se creó sin asignación de grupo.")

        return user

class UserProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True) 
    first_name = serializers.CharField(required=False, allow_blank=True) 
    last_name = serializers.CharField(required=False, allow_blank=True)
    avatar = serializers.ImageField(required=False, allow_null=True) 
    bio = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    groups = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'avatar', 'bio', 'phone_number', 'address', 'groups'
        ]
        # 'read_only_fields' se gestiona mejor campo por campo para flexibilidad

    def get_groups(self, obj):
        return [group.name for group in obj.groups.all()]


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        profile_fields = ['avatar', 'bio', 'phone_number', 'address']
        for field in profile_fields:
            if hasattr(instance, 'profile') and hasattr(instance.profile, field):
                if field == 'avatar' and instance.profile.avatar:
                    request = self.context.get('request')
                    if request is not None:
                        representation[field] = request.build_absolute_uri(instance.profile.avatar.url)
                    else:
                        representation[field] = instance.profile.avatar.url
                else:
                    representation[field] = getattr(instance.profile, field)
            else:
                representation[field] = None # O un valor por defecto si no existe

        return representation
    avatar = serializers.ImageField(required=False, allow_null=True)

    def validate_avatar(self, value):
        if value:
            # Validar tamaño (ej. 4MB)
            if value.size > 4 * 1024 * 1024:
                raise serializers.ValidationError("La imagen del avatar no puede superar los 4MB.")

            # Validar tipo (ej. solo JPG/PNG)
            if not value.content_type in ['image/jpeg', 'image/png']:
                raise serializers.ValidationError("Solo se permiten imágenes JPG o PNG.")

            # Opcional: validar dimensiones (requiere PIL/Pillow y abrir la imagen)
            # from PIL import Image
            # img = Image.open(value)
            # if img.width > 500 or img.height > 500:
            #     raise serializers.ValidationError("La imagen no debe exceder 500x500 píxeles.")
        return value
    # Sobreescribimos el método 'update' para manejar los campos de User y Profile
    def update(self, instance, validated_data):
        # Actualizar campos del User
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save() # Guarda el usuario

        # Actualizar campos del Profile
        profile_data = {}
        for field_name in ['avatar', 'bio', 'phone_number', 'address']:
            if field_name in validated_data:
                profile_data[field_name] = validated_data.pop(field_name)

        if profile_data:
            # Asegúrate de que el perfil exista (debería crearse por la señal)
            profile, created = Profile.objects.get_or_create(user=instance)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save() # Guarda el perfil
        return instance

   