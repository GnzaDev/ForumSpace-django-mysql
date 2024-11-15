from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.db.models import Q
from pagina.models import CustomUser, Categoria, Post, Respuesta, Notificacion
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy
from django.views.generic import CreateView
from pagina.forms import CustomUserCreationForm, CategoriaForm


def is_admin(user):
    return user.is_admin

class CustomLoginView(LoginView):
    template_name = 'login.html'

class RegistroUsuario(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registro.html'
    success_url = reverse_lazy('login')

def index(request):
    query = request.GET.get('query', '')
    categoria_id = request.GET.get('categoria')

    posts = Post.objects.all().order_by('-fecha_creacion')

    if query:
        posts = posts.filter(
            Q(titulo__icontains=query) |
            Q(contenido__icontains=query)
        )

    if categoria_id:
        posts = posts.filter(categoria_id=categoria_id)

    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    categorias = Categoria.objects.all()

    context = {
        'posts': posts,
        'categorias': categorias,
    }

    return render(request, 'index.html', context)

@login_required
def crear_post(request):
    categorias = Categoria.objects.all()
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        contenido = request.POST.get('contenido')
        categoria_id = request.POST.get('categoria')
        
        if titulo and contenido and categoria_id:
            post = Post.objects.create(
                titulo=titulo,
                contenido=contenido,
                autor=request.user,
                categoria_id=categoria_id
            )
            messages.success(request, 'Publicación creada exitosamente.')
            return redirect('ver_post', post_id=post.id)
    
    return render(request, 'crear_post.html', {'categorias': categorias})

def ver_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    respuestas = post.respuesta_set.filter(aprobado=True).order_by('fecha_creacion')
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            contenido = request.POST.get('contenido')
            if contenido:
                respuesta = Respuesta.objects.create(
                    post=post,
                    autor=request.user,
                    contenido=contenido,
                    aprobado=not request.user.is_admin
                )
                messages.success(request, 'Respuesta enviada exitosamente.')

                # Crea la notificación para el usuario
                Notificacion.objects.create(
                    usuario=post.autor,
                    post=post,
                    tipo='respuesta',
                    autor=request.user
                )

                return redirect('ver_post', post_id=post.id)
        else:
            messages.error(request, 'Necesitas iniciar sesión para agregar una respuesta.')

    return render(request, 'ver_post.html', {
        'post': post,
        'respuestas': respuestas
    })

@login_required
def eliminar_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.autor != request.user:
        messages.error(request, 'No tienes permiso para eliminar este post.')
        return redirect('ver_post', post_id=post_id)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Publicación eliminada exitosamente.')
        return redirect('index')

    return render(request, 'eliminar_post.html', {'post': post})

@user_passes_test(is_admin)
def confirmar_eliminar_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post eliminado exitosamente.')
        return redirect('admin_panel')

    return render(request, 'confirmar_eliminar_post.html', {'post': post})

@user_passes_test(is_admin)
def admin_panel(request):
    posts_pendientes = Post.objects.filter(respuesta__aprobado=False).distinct()
    usuarios = CustomUser.objects.all()
    categorias = Categoria.objects.all()
    
    context = {
        'posts_pendientes': posts_pendientes,
        'usuarios': usuarios,
        'categorias': categorias,
    }
    
    return render(request, 'admin_panel.html', context)

@user_passes_test(is_admin)
def aprobar_respuesta(request, respuesta_id):
    respuesta = get_object_or_404(Respuesta, id=respuesta_id)
    respuesta.aprobado = True
    respuesta.save()
    messages.success(request, 'Respuesta aprobada exitosamente.')
    return redirect('admin_panel')

@login_required
def mostrar_perfil(request):
    user = request.user

    if request.method == 'POST':
        email = request.POST.get('email')
        
        # Valida y actualiza el correo
        if email:
            user.email = email
            user.save()
            messages.success(request, "Correo electrónico actualizado correctamente.")

        # Valida y actualiza la contraseña
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if old_password and new_password:
            if new_password == confirm_password:
                if user.check_password(old_password):
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)  # se mantiene autenticado el usuario
                    messages.success(request, "Contraseña actualizada correctamente.")
                else:
                    messages.error(request, "La contraseña actual es incorrecta.")
            else:
                messages.error(request, "Las nuevas contraseñas no coinciden.")

        return redirect('mostrar_perfil')  # Redirecciona al perfil actualizado

    return render(request, 'perfil.html', {'user': user})
    
@login_required
def eliminar_cuenta(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, 'Tu cuenta ha sido eliminada exitosamente.')
        return redirect('index')  # Redirigir al foro 

    return render(request, 'perfil.html')

@user_passes_test(is_admin)
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente.')
            return redirect('admin_panel')
    else:
        form = CategoriaForm()
    return render(request, 'crear_categoria.html', {'form': form})

@user_passes_test(is_admin)
def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        if nombre:
            categoria.nombre = nombre
            categoria.save()
            messages.success(request, 'Categoría actualizada exitosamente.')
            return redirect('admin_panel')
    return render(request, 'editar_categoria.html', {'categoria': categoria})

@user_passes_test(is_admin)
def eliminar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada exitosamente.')
        return redirect('admin_panel')
    
    return render(request, 'eliminar_categoria.html', {'categoria': categoria})

@login_required
def mis_publicaciones(request):
    posts = Post.objects.filter(autor=request.user).order_by('-fecha_creacion')

    context = {
        'posts': posts,
    }
    return render(request, 'mis_publicaciones.html', context)

@login_required
def dar_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

        # Crea notificación para el usuario del Post
        Notificacion.objects.create(
            usuario=post.autor,
            post=post,
            tipo='like',
            autor=request.user
        )

    return redirect('ver_post', post_id=post.id)

@login_required
def ver_notificaciones(request):
    notificaciones = Notificacion.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'notificaciones.html', {'notificaciones': notificaciones})

# Nueva vista para ver publicaciones de un usuario
@user_passes_test(is_admin)
def ver_publicaciones_usuario(request, usuario_id):
    usuario = get_object_or_404(CustomUser, id=usuario_id)
    posts = Post.objects.filter(autor=usuario).order_by('-fecha_creacion')

    context = {
        'usuario': usuario,
        'posts': posts,
    }

    return render(request, 'ver_publicaciones_usuario.html', context)


# Nueva vista para ver respuestas de un usuario
@user_passes_test(is_admin)
def ver_respuestas_usuario(request, usuario_id):
    usuario = get_object_or_404(CustomUser, id=usuario_id)
    respuestas = Respuesta.objects.filter(autor=usuario).order_by('-fecha_creacion')

    context = {
        'usuario': usuario,
        'respuestas': respuestas,
    }

    return render(request, 'ver_respuestas_usuario.html', context)


