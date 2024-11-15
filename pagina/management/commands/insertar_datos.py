from django.core.management.base import BaseCommand
from pagina.models import Categoria, Post, CustomUser

class Command(BaseCommand):
    help = 'Inserta categorías y posts variados en la base de datos'

    def handle(self, *args, **kwargs):
        # Inserta categorías
        categorias_data = [
            Categoria(nombre='Tecnología'),
            Categoria(nombre='Ciencia'),
            Categoria(nombre='Arte'),
            Categoria(nombre='Deportes'),
            Categoria(nombre='Música'),
            Categoria(nombre='Gastronomía'),
            Categoria(nombre='Literatura'),
            Categoria(nombre='Cultura'),
            Categoria(nombre='Educación'),
            Categoria(nombre='Cine')
        ]
        Categoria.objects.bulk_create(categorias_data)
        self.stdout.write(self.style.SUCCESS('Categorías creadas exitosamente.'))

        # Obtener las categorías para crear posts
        categorias = Categoria.objects.all()
        
        usuario, _ = CustomUser.objects.get_or_create(username="usuario1", email="usuario1@example.com")
        
        # Inserta posts variados
        posts_data = [
            Post(titulo="El futuro de la IA", contenido="Discusión sobre inteligencia artificial", autor=usuario, categoria=categorias.get(nombre='Tecnología')),
            Post(titulo="Exploración espacial", contenido="Nuevas misiones a Marte", autor=usuario, categoria=categorias.get(nombre='Ciencia')),
            Post(titulo="El impacto del arte digital", contenido="Cómo el arte digital cambia la percepción", autor=usuario, categoria=categorias.get(nombre='Arte')),
            Post(titulo="Deporte y salud", contenido="La importancia del deporte en la salud", autor=usuario, categoria=categorias.get(nombre='Deportes')),
            Post(titulo="Música y emociones", contenido="El impacto de la música en las emociones", autor=usuario, categoria=categorias.get(nombre='Música')),
            Post(titulo="La revolución de la comida rápida", contenido="Cómo ha cambiado la industria alimentaria", autor=usuario, categoria=categorias.get(nombre='Gastronomía')),
            Post(titulo="Nuevas tendencias en literatura", contenido="Exploración de la literatura moderna", autor=usuario, categoria=categorias.get(nombre='Literatura')),
            Post(titulo="Cultura y globalización", contenido="El impacto de la globalización en las culturas locales", autor=usuario, categoria=categorias.get(nombre='Cultura')),
            Post(titulo="Educación en la era digital", contenido="Cómo la tecnología afecta el aprendizaje", autor=usuario, categoria=categorias.get(nombre='Educación')),
            Post(titulo="Clásicos del cine moderno", contenido="Análisis de películas que marcaron una era", autor=usuario, categoria=categorias.get(nombre='Cine')),
            Post(titulo="Desafíos éticos de la inteligencia artificial", contenido="Cuestiones éticas en el desarrollo de IA", autor=usuario, categoria=categorias.get(nombre='Tecnología')),
            Post(titulo="Cambio climático y ciencia", contenido="Impacto del cambio climático en investigaciones científicas", autor=usuario, categoria=categorias.get(nombre='Ciencia')),
            Post(titulo="Restauración de obras de arte", contenido="Proceso y técnicas de restauración de arte", autor=usuario, categoria=categorias.get(nombre='Arte')),
            Post(titulo="Eventos deportivos internacionales", contenido="La importancia de los eventos deportivos en la diplomacia", autor=usuario, categoria=categorias.get(nombre='Deportes')),
            Post(titulo="Música y cultura juvenil", contenido="Relación entre música y movimientos juveniles", autor=usuario, categoria=categorias.get(nombre='Música')),
            Post(titulo="Gastronomía molecular", contenido="Innovación en la cocina mediante ciencia y tecnología", autor=usuario, categoria=categorias.get(nombre='Gastronomía')),
            Post(titulo="Literatura en la era digital", contenido="Cómo la tecnología transforma la industria editorial", autor=usuario, categoria=categorias.get(nombre='Literatura')),
            Post(titulo="El patrimonio cultural en riesgo", contenido="Amenazas al patrimonio cultural en un mundo cambiante", autor=usuario, categoria=categorias.get(nombre='Cultura')),
            Post(titulo="El rol de los docentes en el siglo XXI", contenido="Nuevos desafíos en la educación moderna", autor=usuario, categoria=categorias.get(nombre='Educación')),
            Post(titulo="Cine independiente", contenido="Exploración del cine independiente y su impacto", autor=usuario, categoria=categorias.get(nombre='Cine'))
        ]
        Post.objects.bulk_create(posts_data)
        self.stdout.write(self.style.SUCCESS('Posts creados exitosamente.'))
        
        # Crear un superusuario (admin)
        admin_user = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@admin.com',
            password='admin'
        )
        self.stdout.write(self.style.SUCCESS(f'Superusuario creado exitosamente: {admin_user.username}'))
