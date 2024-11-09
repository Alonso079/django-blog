Crear SuperUser:
- Para Windows: `py manage.py createsuperuser`
- Para Linux/Mac: `python3 manage.py createsuperuser`

Finalmente Ejecute los Proyectos:
- Para Windows: `py manage.py runserver`
- Para Linux/Mac: `python3 manage.py runserver`

Características del proyecto:
- Usuarios Dedicados Frontend Admin Panel.
- Sistema de Iniciar sesión/Registrarse en el Frontend.

**Lados del usuario (Frontend)**
- Los usuarios pueden registrarse.
- Los usuarios pueden iniciar sesión/cerrar sesión.
- Los usuarios pueden agregar publicaciones (Nota: La creación de blogs por parte del usuario aún no está del todo bien, pero después de la asignación del blog desde el panel de administración, el usuario puede editar, subir y ocultar publicaciones).
- Los usuarios pueden mostrar/ocultar publicaciones.
- Los usuarios pueden editar publicaciones.
- Los usuarios pueden eliminar publicaciones.

**Lados de administración (Frontend)**
- Los administradores pueden agregar publicaciones.
- Los administradores pueden agregar categorías.
- El administrador puede editar publicaciones.
- El administrador puede editar categorías.
- El administrador puede eliminar publicaciones.
- El administrador puede eliminar categorías.
- El administrador puede agregar usuarios y eliminar usuarios.
- El administrador puede hacer publicaciones destacadas.
- El administrador puede aprobar publicaciones pendientes.

**Características de las Publicaciones del Blog**
- El menú de blogs muestra categorías con la mayoría de las publicaciones debajo de ellas, de más alto a más bajo.
- Las publicaciones se muestran por destacadas, recientemente agregadas, por categorías, o por la mayoría de los recuentos de vistas.
- Solo se mostrarán las publicaciones activas/aprobadas, no las pendientes.
- Cada publicación tiene un conteo de visitas.
- La publicación puede ser destacada o popular por la mayoría de los recuentos de visitas y comentarios.
- Cada publicación tiene características de comentarios.
- Sistema de suscripción para recopilar correos electrónicos para marketing por correo electrónico.
- Publicaciones liberadas por los usuarios.
- Instalación de búsqueda.
- Página de categoría única dedicada (por destacadas, populares, recientemente agregadas).
