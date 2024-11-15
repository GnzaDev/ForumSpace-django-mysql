from django.urls import path
from pagina import views
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView
from pagina.views import (CustomLoginView, RegistroUsuario, eliminar_post,
                          confirmar_eliminar_post, mis_publicaciones, dar_like,
                          ver_notificaciones)

urlpatterns = [
    path('', views.index, name='index'),  # Ruta principal
    path('perfil/', views.mostrar_perfil, name='mostrar_perfil'),  # Ruta para mostrar el perfil
    path('post/crear/', views.crear_post, name='crear_post'),  # Ruta para crear posts
    path('post/<int:post_id>/', views.ver_post, name='ver_post'),  # Usamos post_id en lugar de tema_id
    path('admin-panel/', views.admin_panel, name='admin_panel'),  # Ruta para el panel de administración
    path('aprobar-respuesta/<int:respuesta_id>/', views.aprobar_respuesta, name='aprobar_respuesta'),  # Ruta para aprobar respuestas
    path('login/', CustomLoginView.as_view(), name='login'),  # Ruta para iniciar sesión
    path('logout/', LogoutView.as_view(), name='logout'),  # Ruta para cerrar sesión
    path('registro/', RegistroUsuario.as_view(), name='registro'),  # Ruta para el registro
    path('categoria/crear/', views.crear_categoria, name='crear_categoria'),  # Ruta para crear categoría
    path('categoria/eliminar/<int:categoria_id>/', views.eliminar_categoria, name='eliminar_categoria'),  # Ruta para eliminar categoría
    path('categoria/editar/<int:categoria_id>/', views.editar_categoria, name='editar_categoria'),  # Ruta para editar categoría
    path('post/eliminar/<int:post_id>/', eliminar_post, name='eliminar_post'),  # Consistencia con post_id
    path('post/eliminar/<int:post_id>/', confirmar_eliminar_post, name='confirmar_eliminar_post'),  # Consistencia con post_id
    path('mis-publicaciones/', mis_publicaciones, name='mis_publicaciones'),  # URL para Mis Publicaciones
    path('post/<int:post_id>/like/', dar_like, name='dar_like'),  # Consistencia con post_id
    path('notificaciones/', ver_notificaciones, name='notificaciones'),  # Ruta para las notificaciones
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),  # Ruta para cambiar contraseña
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),  # Ruta para confirmar que la contraseña ha cambiado
    path('eliminar-cuenta/', views.eliminar_cuenta, name='eliminar_cuenta'),
    
    path('usuarios/<int:usuario_id>/publicaciones/', views.ver_publicaciones_usuario, name='ver_publicaciones_usuario'),
    path('usuarios/<int:usuario_id>/respuestas/', views.ver_respuestas_usuario, name='ver_respuestas_usuario'),


]
