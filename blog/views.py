from django import views
from django.core import paginator
from django.http import HttpResponseRedirect
from django.db.models.fields import EmailField
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Blog, Categoria, Etiqueta, RegistroCorreo, Comentario
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.contrib import messages

# Vista de la página principal (Home)
class HomeView(View):
    def get(self, request, *args, **kwargs):
        destacados = Blog.objects.filter(estado='activo', visible=True, destacado=True).order_by('categoria', '-creado_en')[:5]
        publicaciones = Blog.objects.filter(estado='activo', visible=True).order_by('categoria', '-creado_en')

        primer_post = destacados.first()
        segundo_post = destacados[1] if len(destacados) > 1 else None
        ultimos_posts = destacados[2:] if len(destacados) > 2 else []

        contexto = {
            'publicaciones': publicaciones,
            'destacados': destacados,
            'primer_post': primer_post,
            'segundo_post': segundo_post,
            'ultimos_posts': ultimos_posts
        }
        return render(request, 'home/index.html', contexto)


# Vista para una entrada de blog individual (VerPublicacion)
class VerPublicacion(View):
    def get(self, request, id, *args, **kwargs):
        post = get_object_or_404(Blog, id=id)
        post.conteo_visitas += 1
        post.save()

        relacionados = Blog.objects.filter(autor=post.autor).exclude(id=id).order_by('-id')[:4]
        primer_relacionado = relacionados.first()
        otros_relacionados = relacionados[1:]

        contexto = {
            'post': post,
            'relacionados': relacionados,
            'primer_relacionado': primer_relacionado,
            'otros_relacionados': otros_relacionados
        }
        return render(request, 'blogs/post/single_blog.html', contexto)


# Vista de Categoría (CategoriaView)
class CategoriaView(View):
    def get(self, request, slug, *args, **kwargs):
        categoria = get_object_or_404(Categoria, slug=slug)
        publicaciones = Blog.objects.filter(categoria=categoria, estado='activo', visible=True).order_by('-creado_en')
        populares = Blog.objects.filter(categoria=categoria, estado='activo', visible=True).annotate(post_count=Count('conteo_visitas')).order_by('-conteo_visitas')

        post_destacado = populares.first()
        posts_populares = populares[1:6]

        # Paginación
        paginador = Paginator(publicaciones, 3)
        numero_pagina = request.GET.get('page')
        pagina_obj = paginador.get_page(numero_pagina)

        contexto = {
            'categoria': categoria,
            'publicaciones': pagina_obj,
            'posts_populares': posts_populares,
            'post_destacado': post_destacado,
        }
        return render(request, 'blogs/category/category.html', contexto)


# Vista de Etiqueta (EtiquetaView)
class EtiquetaView(View):
    def get(self, request, id, *args, **kwargs):
        etiqueta = get_object_or_404(Etiqueta, id=id)
        publicaciones = etiqueta.blog_set.all().order_by('-id')
        conteo_etiqueta = publicaciones.count()

        contexto = {
            'etiqueta': etiqueta,
            'publicaciones': publicaciones,
            'conteo_etiqueta': conteo_etiqueta
        }
        return render(request, '/dashboard/tag/tag.html', contexto)


# Vista de Suscripción (SubscripcionView)
class SubscripcionView(View):
    def post(self, request, *args, **kwargs):
        correo = request.POST.get('subscribe')
        if RegistroCorreo.objects.filter(correo=correo).exists():
            messages.success(request, 'Ya estás suscrito, ¡gracias!')
        else:
            RegistroCorreo.objects.create(correo=correo)
            messages.success(request, 'Gracias por suscribirte')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Vista de Búsqueda (BuscarView)
class BuscarView(View):
    def get(self, request, *args, **kwargs):
        # Obtener el valor de 'q' y usar una cadena vacía como valor predeterminado si 'q' no está presente
        consulta = request.GET.get('q', '')

        # Filtrar las publicaciones solo cuando hay consulta válida
        publicaciones = Blog.objects.filter(estado='activo', visible=True)

        if len(consulta) == 0:
            # Si la consulta está vacía, no mostramos resultados específicos
            resultados = publicaciones.none()
        elif len(consulta) > 100:
            # Si la consulta es demasiado larga, no buscamos nada
            resultados = publicaciones.none()
        else:
            # Filtramos los resultados según la consulta proporcionada
            resultados = publicaciones.filter(
                Q(titulo__icontains=consulta) |
                Q(categoria__nombre__icontains=consulta) |
                Q(detalle__icontains=consulta)
            )

        # Crear el contexto para pasar a la plantilla
        contexto = {
            'publicaciones': resultados,
            'consulta': consulta
        }

        # Renderizar la respuesta con el contexto y la plantilla 'home/search.html'
        return render(request, 'home/search.html', contexto)

# Vista de Comentarios (ComentarioView)
class ComentarioView(View):
    def post(self, request, id, *args, **kwargs):
        post = get_object_or_404(Blog, id=id)
        nombre = request.POST.get('name')
        cuerpo = request.POST.get('body')
        Comentario.objects.create(post=post, nombre=nombre, cuerpo=cuerpo)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Vista de Prueba (PruebaView)
def PruebaView(request):
    categorias = Categoria.objects.all()
    conteo_categorias = len(categorias)
    posts = Categoria.objects.all().annotate(post_count=Count('blog')).order_by('-post_count')

    contexto = {
        'categorias': categorias,
        'conteo_categorias': conteo_categorias,
        'posts': posts
    }
    return render(request, 'test.html', contexto)


# Listar Etiquetas (ListarEtiquetasView)
class ListarEtiquetasView(View):
    def get(self, request, *args, **kwargs):
        etiquetas = Etiqueta.objects.all().order_by('-id')
        contexto = {
            'etiquetas': etiquetas
        }
        return render(request, 'dashboard/etiqueta/listar_etiquetas.html', contexto)
