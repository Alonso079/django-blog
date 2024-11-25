from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect
from .models import Blog, Categoria, Etiqueta, RegistroCorreo, Comentario
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.contrib import messages

# Vista de la página principal (Home)
class HomeView(View):
    def get(self, request, *args, **kwargs):
        destacados = Blog.objects.filter(estado='activo', visible=True, destacado=True).order_by('categoria', '-creado_en')[:5]
        publicaciones = Blog.objects.filter(estado='activo', visible=True).order_by('-creado_en')

        contexto = {
            'publicaciones': publicaciones,
            'destacados': destacados,
            'primer_post': destacados.first() if destacados else None,
            'segundo_post': destacados[1] if len(destacados) > 1 else None,
            'ultimos_posts': destacados[2:] if len(destacados) > 2 else []
        }
        return render(request, 'home/index.html', contexto)


# Vista para una entrada de blog individual (VerPublicacion)
class VerPublicacion(View):
    def get(self, request, id, *args, **kwargs):
        post = get_object_or_404(Blog, id=id)
        post.conteo_visitas += 1
        post.save()

        relacionados = Blog.objects.filter(autor=post.autor).exclude(id=id).order_by('-id')[:4]

        contexto = {
            'post': post,
            'primer_relacionado': relacionados.first() if relacionados else None,
            'otros_relacionados': relacionados[1:] if len(relacionados) > 1 else []
        }
        return render(request, 'blogs/post/single_blog.html', contexto)


# Vista de Categoría (CategoriaView)
class CategoriaView(View):
    def get(self, request, slug, *args, **kwargs):
        categoria = get_object_or_404(Categoria, slug=slug)
        publicaciones = Blog.objects.filter(categoria=categoria, estado='activo', visible=True).order_by('-creado_en')
        populares = publicaciones.annotate(post_count=Count('conteo_visitas')).order_by('-conteo_visitas')

        # Paginación
        paginador = Paginator(publicaciones, 3)
        numero_pagina = request.GET.get('page')
        pagina_obj = paginador.get_page(numero_pagina)

        contexto = {
            'categoria': categoria,
            'publicaciones': pagina_obj,
            'posts_populares': populares[1:6],
            'post_destacado': populares.first() if populares else None,
        }
        return render(request, 'blogs/category/category.html', contexto)


# Vista de Etiqueta (EtiquetaView)
class EtiquetaView(View):
    def get(self, request, id, *args, **kwargs):
        etiqueta = get_object_or_404(Etiqueta, id=id)
        publicaciones = etiqueta.blog_set.filter(estado='activo', visible=True).order_by('-id')

        # Paginación
        paginador = Paginator(publicaciones, 3)
        numero_pagina = request.GET.get('page')
        pagina_obj = paginador.get_page(numero_pagina)

        contexto = {
            'etiqueta': etiqueta,
            'publicaciones': pagina_obj,
            'conteo_etiqueta': publicaciones.count()
        }
        return render(request, 'dashboard/tag/tag.html', contexto)


# Vista de Suscripción (SubscripcionView)
class SubscripcionView(View):
    def post(self, request, *args, **kwargs):
        correo = request.POST.get('subscribe')
        if RegistroCorreo.objects.filter(correo=correo).exists():
            messages.info(request, 'Ya estás suscrito, ¡gracias!')
        else:
            RegistroCorreo.objects.create(correo=correo)
            messages.success(request, 'Gracias por suscribirte')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Vista de Búsqueda (BuscarView)
from django.db.models import Count

class BuscarView(View):
    def get(self, request, *args, **kwargs):
        consulta = request.GET.get('q', '').strip()
        resultados = Blog.objects.filter(estado='activo', visible=True)

        if consulta:
            # Solo realizar la búsqueda si la consulta tiene menos de 100 caracteres
            if len(consulta) <= 100:
                resultados = resultados.filter(
                    Q(titulo__icontains=consulta) |
                    Q(categoria__nombre__icontains=consulta) |
                    Q(detalle__icontains=consulta)
                )
            else:
                # Mostrar un mensaje si la consulta es demasiado larga
                return render(request, 'home/search.html', {
                    'consulta': consulta,
                    'mensaje': 'La búsqueda debe tener menos de 100 caracteres.',
                    'total_resultados': 0
                })

        # Limitar el número de resultados para evitar sobrecarga
        resultados = resultados[:50]

        contexto = {
            'publicaciones': resultados,
            'consulta': consulta,
            'total_resultados': len(resultados) if consulta else 0
        }

        # Mostrar un mensaje si no se encuentran resultados
        if consulta and not resultados:
            contexto['mensaje'] = 'No se encontraron resultados para tu búsqueda.'

        return render(request, 'home/search.html', contexto)


# Vista de Comentarios (ComentarioView)
class ComentarioView(View):
    def post(self, request, id, *args, **kwargs):
        post = get_object_or_404(Blog, id=id)
        nombre = request.POST.get('name').strip()
        cuerpo = request.POST.get('body').strip()
        if cuerpo:
            Comentario.objects.create(publicacion=post, nombre=nombre, cuerpo=cuerpo)
            messages.success(request, 'Comentario añadido con éxito.')
        else:
            messages.error(request, 'El comentario no puede estar vacío.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Vista de Prueba (PruebaView)
def PruebaView(request):
    categorias = Categoria.objects.all()
    posts = Categoria.objects.annotate(post_count=Count('blog')).order_by('-post_count')

    contexto = {
        'categorias': categorias,
        'conteo_categorias': categorias.count(),
        'posts': posts
    }
    return render(request, 'test.html', contexto)


# Listar Etiquetas (ListarEtiquetasView)
class ListarEtiquetasView(View):
    def get(self, request, *args, **kwargs):
        etiquetas = Etiqueta.objects.all().order_by('-id')

        # Paginación
        paginador = Paginator(etiquetas, 10)
        numero_pagina = request.GET.get('page')
        pagina_obj = paginador.get_page(numero_pagina)

        contexto = {
            'etiquetas': pagina_obj
        }
        return render(request, 'dashboard/etiqueta/listar_etiquetas.html', contexto)
