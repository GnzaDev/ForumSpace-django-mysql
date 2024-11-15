from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        if not username:
            raise ValueError('El usuario debe tener un nombre de usuario')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')
        if extra_fields.get('is_admin') is not True:
            raise ValueError('El superusuario debe tener is_admin=True.')

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    fecha_registro = models.DateTimeField(default=timezone.now)
    banear_hasta = models.DateTimeField(null=True, blank=True, default=None)  # Campo para gestionar el baneo

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def esta_baneado(self):
        if self.banear_hasta and self.banear_hasta > timezone.now():
            return True
        return False

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


#Posts
class Post(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    autor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(CustomUser, related_name='posts_liked', blank=True)

    def __str__(self):
        return self.titulo

    def num_respuestas(self):
        return self.respuesta_set.count()

    def num_likes(self):
        return self.likes.count()

class Respuesta(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    autor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    aprobado = models.BooleanField(default=False)

    def __str__(self):
        return f'Respuesta de {self.autor} en {self.post}'

class Notificacion(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    tipo = models.CharField(max_length=50)  # Tipo de notificación: respuesta, like, etc.
    autor = models.ForeignKey(CustomUser, related_name='notificacion_autor', on_delete=models.CASCADE)
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.tipo} - {self.post.titulo}"

