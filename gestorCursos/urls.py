from django.urls import path
from .views import (home_cursos,listar_cursos,crear_curso,editar_curso,eliminar_curso,listar_alumnos,crear_alumno,editar_alumno,eliminar_alumno)

urlpatterns = [
    # HOME DE CURSOS
    path("", listar_cursos, name="home_cursos"),
    path("home/", home_cursos, name="home_cursos_alias"),   
    path("inicio/", home_cursos, name="home_cursos_inicio"), 

    # CURSOS
    path("cursos/listar/", listar_cursos, name="listar_cursos"),
    path("cursos/crear/", crear_curso, name="crear_curso"),
    path("cursos/editar/<int:id>/", editar_curso, name="editar_curso"),
    path("cursos/eliminar/<int:id>/", eliminar_curso, name="eliminar_curso"),

    # ALUMNOS
    path("alumnos/", listar_alumnos, name="alumnos_redirect"),
    path("alumnos/listar/", listar_alumnos, name="listar_alumnos"),
    path("alumnos/crear/", crear_alumno, name="crear_alumno"),
    path("alumnos/editar/<int:id>/", editar_alumno, name="editar_alumno"),
    path("alumnos/eliminar/<int:id>/", eliminar_alumno, name="eliminar_alumno"),
]
