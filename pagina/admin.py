from django.contrib import admin
from pagina.models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'fecha_creacion')

admin.site.register(Post, PostAdmin)
