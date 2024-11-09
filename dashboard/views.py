from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import View
from blog.models import Blog, Categoria, Etiqueta
from .models import Autor
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db.models import Count, Sum, Q

# Vista del Panel de Usuario (Dashboard)
class Dashboard(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        usuario = request.user

        # Verificar si el usuario tiene un perfil de Autor
        if not hasattr(usuario, 'autor'):
            contexto = {
                'usuario': usuario,
                'mensaje_error': "El usuario no tiene un perfil de autor asociado.",
            }
            return render(request, 'dashboard/dash/dashboard.html', contexto)

        publicaciones = usuario.autor.blog_set.all()
        publicaciones_activas = publicaciones.filter(estado='activo')
        publicaciones_pendientes = publicaciones.filter(estado='pendiente')
        conteo_visitas = publicaciones.aggregate(Sum('conteo_visitas'))['conteo_visitas__sum']

        contexto = {
            'usuario': usuario,
            'publicaciones': publicaciones,
            'publicaciones_activas': publicaciones_activas,
            'publicaciones_pendientes': publicaciones_pendientes,
            'conteo_publicaciones': publicaciones.count(),
            'conteo_activas': publicaciones_activas.count(),
            'conteo_pendientes': publicaciones_pendientes.count(),
            'conteo_visitas': conteo_visitas,
        }
        return render(request, 'dashboard/dash/dashboard.html', contexto)

# Crear Autor
class CrearAutor(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, 'dashboard/user/create_user.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        email = request.POST.get('email')
        nombre = request.POST.get('fname')
        apellido = request.POST.get('lname')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        usuario = User.objects.filter(username=username)
        email_obj = Autor.objects.filter(correo=email)

        if usuario:
            messages.warning(request, '¡El nombre de usuario ya existe!')
            return redirect('sign_up')
        elif password1 != password2:
            messages.warning(request, 'Las contraseñas no coinciden')
            return redirect('sign_up')
        else:
            nuevo_usuario = User(username=username, password=make_password(password1))
            nuevo_usuario.save()

        if email_obj:
            messages.warning(request, '¡El correo ya está registrado!')
            return redirect('sign_up')
        else:
            nuevo_autor = Autor(usuario=nuevo_usuario, correo=email, nombre=nombre, apellido=apellido)
            nuevo_autor.save()
            messages.success(request, 'Gracias por registrarte, por favor inicia sesión')
            return redirect('login')

# Perfil del Autor
class PerfilAutor(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        autor = request.user
        contexto = {
            'autor': autor
        }
        return render(request, 'dashboard/user/profile.html', contexto)

# Editar Perfil del Autor
class EditarAutor(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, 'dashboard/user/edit_profile.html')

    def post(self, request):
        obj = request.user.autor
        obj.imagen_autor = request.FILES.get('imagen')
        obj.nombre = request.POST.get('fname')
        obj.apellido = request.POST.get('lname')
        obj.correo = request.POST.get('email')
        obj.save()
        messages.success(request, 'Tu perfil ha sido actualizado exitosamente')
        return redirect('perfil')

# Vista de Inicio de Sesión (Login)
class VistaLogin(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, 'dashboard/user/login.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('dashboard')
        else:
            messages.warning(request, 'El nombre de usuario o la contraseña no coinciden')
            return redirect('login')

# Vista de Cierre de Sesión (Logout)
class VistaLogout(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')

# Listar Publicaciones Activas
class ListarPublicacionesActivas(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        publicaciones_activas = request.user.autor.blog_set.filter(estado='activo').order_by('-id')
        contexto = {
            'publicaciones_activas': publicaciones_activas
        }
        return render(request, 'dashboard/post/post_listing_active.html', contexto)

# Listar Publicaciones Pendientes
class ListarPublicacionesPendientes(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        publicaciones_pendientes = request.user.autor.blog_set.filter(estado='pendiente').order_by('-id')
        contexto = {
            'publicaciones_pendientes': publicaciones_pendientes
        }
        return render(request, 'dashboard/post/post_listing_pending.html', contexto)

# Listar Publicaciones
class ListarPublicaciones(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        publicaciones = Blog.objects.filter(autor=request.user.autor).order_by('-id')
        contexto = {
            'publicaciones': publicaciones
        }
        return render(request, 'dashboard/post/all_post.html', contexto)

# Ver Publicación
class VerPublicacion(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id):
        # Obtener la publicación o devolver un 404 si no existe
        publicacion = get_object_or_404(Blog, id=id)

        # Crear el contexto para pasar a la plantilla
        contexto = {
            'post': publicacion  # Asegúrate de que el nombre del contexto sea el correcto según la plantilla
        }

        # Renderizar la plantilla con el contexto
        return render(request, 'dashboard/post/post_view.html', contexto)
# Editar Publicación
# Editar Publicación
class EditarPublicacion(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id):
        publicacion = get_object_or_404(Blog, id=id)
        categorias = Categoria.objects.all()
        contexto = {
            'obj': publicacion,  # Cambiado para que coincida con la plantilla
            'categorias': categorias
        }
        return render(request, 'dashboard/post/edit_post.html', contexto)

    def post(self, request, id):
        publicacion = get_object_or_404(Blog, id=id)
        publicacion.titulo = request.POST.get('title')  # Cambiado para que coincida con el campo en el formulario
        publicacion.detalle = request.POST.get('detail')
        
        if 'imagen' in request.FILES:
            publicacion.imagen = request.FILES.get('imagen')

        categoria_id = request.POST.get('category')

        # Validar si categoria_id es un número antes de usarlo
        if categoria_id and categoria_id.isdigit():
            publicacion.categoria = get_object_or_404(Categoria, id=int(categoria_id))
        else:
            messages.error(request, 'Categoría inválida proporcionada.')

        publicacion.save()
        messages.success(request, 'Publicación actualizada exitosamente')
        return redirect('todas_publicaciones')
# Eliminar Publicación
class EliminarPublicacion(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, id):
        publicacion = get_object_or_404(Blog, id=id)
        publicacion.delete()
        messages.success(request, 'Publicación eliminada exitosamente')
        return redirect('todas_publicaciones')

# Hacer Publicación Visible
class HacerPublicacionVisible(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, id):
        publicacion = get_object_or_404(Blog, id=id)
        publicacion.visible = True
        publicacion.save()
        messages.success(request, 'La publicación ahora es visible')
        return redirect('todas_publicaciones')

# Ocultar Publicación
class OcultarPublicacion(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, id):
        publicacion = get_object_or_404(Blog, id=id)
        publicacion.visible = False
        publicacion.save()
        messages.success(request, 'La publicación ha sido ocultada')
        return redirect('todas_publicaciones')

# Crear Publicación
class CrearPublicacion(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        categorias = Categoria.objects.all()
        contexto = {
            'categorias': categorias
        }
        return render(request, 'dashboard/post/create_post.html', contexto)

    def post(self, request):
        autor = request.user.autor
        titulo = request.POST.get('titulo')
        detalle = request.POST.get('detalle')
        imagen = request.FILES.get('imagen')
        categoria_id = request.POST.get('categoria')
        categoria = get_object_or_404(Categoria, id=categoria_id)

        nueva_publicacion = Blog(autor=autor, titulo=titulo, detalle=detalle, imagen=imagen, categoria=categoria)
        nueva_publicacion.save()
        messages.success(request, 'Publicación creada exitosamente')
        return redirect('todas_publicaciones')

# Crear Categoría
class CrearCategoria(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, 'dashboard/category/category.html')

    def post(self, request):
        categoria_nombre = request.POST.get('categoria')
        categoria_existente = Categoria.objects.filter(nombre=categoria_nombre)
        if categoria_existente:
            messages.warning(request, 'Esta categoría ya existe en la base de datos')
        else:
            Categoria.objects.create(nombre=categoria_nombre)
            messages.success(request, 'Categoría creada exitosamente')
        return redirect('categoria')

# Actualizar Categoría
class ActualizarCategoria(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, id):
        categoria = get_object_or_404(Categoria, id=id)
        categoria.nombre = request.POST.get('categoria')
        categoria.save()
        return redirect('categoria')

# Eliminar Categoría
class EliminarCategoria(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, id):
        categoria = get_object_or_404(Categoria, id=id)
        categoria.delete()
        messages.success(request, 'Categoría eliminada exitosamente')
        return redirect('categoria')

# Crear Etiqueta
class CrearEtiqueta(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, 'dashboard/tag/tag.html')

    def post(self, request):
        etiqueta_nombre = request.POST.get('etiqueta')
        etiqueta_existente = Etiqueta.objects.filter(nombre=etiqueta_nombre)
        if etiqueta_existente:
            messages.warning(request, 'Esta etiqueta ya existe')
        else:
            Etiqueta.objects.create(nombre=etiqueta_nombre)
            messages.success(request, 'Etiqueta creada exitosamente')
        return redirect('etiqueta')

# Actualizar Etiqueta
class ActualizarEtiqueta(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, id):
        etiqueta = get_object_or_404(Etiqueta, id=id)
        etiqueta.nombre = request.POST.get('etiqueta')
        etiqueta.save()
        return redirect('etiqueta')

# Eliminar Etiqueta
class EliminarEtiqueta(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, id):
        etiqueta = get_object_or_404(Etiqueta, id=id)
        etiqueta.delete()
        messages.success(request, 'Etiqueta eliminada exitosamente')
        return redirect('etiqueta')

# Listar Etiquetas
class ListarEtiquetas(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        etiquetas = Etiqueta.objects.all().order_by('-id')
        contexto = {
            'etiquetas': etiquetas
        }
        return render(request, 'dashboard/tag/tag.html', contexto)

# Vista de Blog Individual
class VistaBlog(View):
    def get(self, request, id, *args, **kwargs):
        blog = get_object_or_404(Blog, id=id)
        # Incrementar el conteo de visitas
        blog.conteo_visitas += 1
        blog.save()

        # Publicaciones relacionadas del mismo autor
        relacionadas = Blog.objects.filter(autor=blog.autor).exclude(id=id).order_by('-id')[:4]

        contexto = {
            'publicacion': blog,
            'relacionadas': relacionadas,
        }
        return render(request, 'dashboard/post/single_blog.html', contexto)

# Vista de Búsqueda de Publicaciones
class BuscarView(View):
    def get(self, request, *args, **kwargs):
        consulta = request.GET.get('q', '')
        publicaciones = Blog.objects.filter(estado='activo', visible=True)

        if len(consulta) > 100:
            resultados = publicaciones.none()
        else:
            resultados = publicaciones.filter(
                Q(titulo__icontains=consulta) |
                Q(detalle__icontains=consulta) |
                Q(categoria__nombre__icontains=consulta)
            )

        contexto = {
            'consulta': consulta,
            'resultados': resultados,
        }
        return render(request, 'home/search.html', contexto)

# Vista de Etiqueta
class VistaEtiqueta(View):
    def get(self, request, id, *args, **kwargs):
        etiqueta = get_object_or_404(Etiqueta, id=id)
        publicaciones = etiqueta.blog_set.all().order_by('-id')
        conteo_etiqueta = publicaciones.count()

        contexto = {
            'etiqueta': etiqueta,
            'publicaciones': publicaciones,
            'conteo_etiqueta': conteo_etiqueta,
        }
        return render(request, 'dashboard/tag/tag.html', contexto)

# Listar Categorías
class ListarCategorias(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        categorias = Categoria.objects.all().order_by('-id')
        contexto = {
            'categorias': categorias
        }
        return render(request, 'blogs/category/category.html', contexto)
