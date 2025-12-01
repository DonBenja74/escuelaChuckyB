from django.shortcuts import render, redirect
from .models import Curso, Alumno
from gestorUser.models import Perfil
from django.contrib.auth.decorators import login_required


# ------------------------------------
# HOME CURSOS (redirige según rol)
# ------------------------------------
@login_required
def home_cursos(request):
    perfil = Perfil.objects.get(user=request.user)

    if perfil.rol == "admin":
        return render(request, "gestorCursos/home_admin.html")
    else:
        return render(request, "gestorCursos/home_usuario.html")


# ------------------------------------
# LISTAR CURSOS (solo admin)
# ------------------------------------
# Admin ve todos – Usuario normal también ve todos (solo lectura)
@login_required
def listar_cursos(request):
    cursos = Curso.objects.all()
    perfil = Perfil.objects.get(user=request.user)

    return render(request, "gestorCursos/listar_cursos.html", {
        "cursos": cursos,
        "es_admin": perfil.rol == "admin"
    })

# ------------------------------------
# CREAR CURSO (solo admin)
# ------------------------------------
@login_required
def crear_curso(request):
    perfil = Perfil.objects.get(user=request.user)

    if perfil.rol != "admin":
        return redirect("panel_usuario")

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        codigo = request.POST.get("codigo")

        Curso.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            codigo=codigo
        )

        return redirect("listar_cursos")

    return render(request, "gestorCursos/crear_curso.html", {
        "es_admin": True
    })


# ------------------------------------
# EDITAR CURSO (solo admin)
# ------------------------------------
@login_required
def editar_curso(request, id):
    perfil = Perfil.objects.get(user=request.user)

    if perfil.rol != "admin":
        return redirect("panel_usuario")

    curso = Curso.objects.get(id=id)

    if request.method == "POST":
        curso.nombre = request.POST.get("nombre")
        curso.descripcion = request.POST.get("descripcion")
        curso.codigo = request.POST.get("codigo")
        curso.save()

        return redirect("listar_cursos")

    return render(request, "gestorCursos/editar_curso.html", {
        "curso": curso,
        "es_admin": True
    })


# ------------------------------------
# ELIMINAR CURSO (solo admin)
# ------------------------------------
@login_required
def eliminar_curso(request, id):
    perfil = Perfil.objects.get(user=request.user)

    if perfil.rol != "admin":
        return redirect("panel_usuario")

    Curso.objects.get(id=id).delete()
    return redirect("listar_cursos")


# ------------------------------------
# LISTAR ALUMNOS
# admin = ve todos
# usuario normal = ve solo los suyos
# ------------------------------------
@login_required
def listar_alumnos(request):
    perfil = Perfil.objects.get(user=request.user)

    alumnos = Alumno.objects.all()

    es_admin = (perfil.rol == "admin")

    return render(request, "gestorCursos/listar_alumnos.html", {
        "alumnos": alumnos,
        "es_admin": es_admin
    })



# ------------------------------------
# CREAR ALUMNO
# admin = crea cualquiera
# usuario = también crea alumnos
# ------------------------------------
@login_required
def crear_alumno(request):
    perfil = Perfil.objects.get(user=request.user)
    cursos = Curso.objects.all()

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        rut = request.POST.get("rut")
        curso_id = request.POST.get("curso")

        Alumno.objects.create(
            nombre=nombre,
            apellido=apellido,
            rut=rut,
            curso=Curso.objects.get(id=curso_id),
            creador=request.user
        )

        return redirect("listar_alumnos")

    return render(request, "gestorCursos/crear_alumno.html", {
        "cursos": cursos,
        "es_admin": (perfil.rol == "admin")
    })


# ------------------------------------
# EDITAR ALUMNO
# admin = puede editar todos
# usuario = solo los que creó
# ------------------------------------
@login_required
def editar_alumno(request, id):
    alumno = Alumno.objects.get(id=id)
    cursos = Curso.objects.all()
    perfil = Perfil.objects.get(user=request.user)

    # bloqueo de permisos
    if perfil.rol != "admin" and alumno.creador != request.user:
        return redirect("listar_alumnos")

    if request.method == "POST":
        alumno.nombre = request.POST.get("nombre")
        alumno.apellido = request.POST.get("apellido")
        alumno.rut = request.POST.get("rut")
        alumno.curso_id = request.POST.get("curso")
        alumno.save()

        return redirect("listar_alumnos")

    return render(request, "gestorCursos/editar_alumno.html", {
        "alumno": alumno,
        "cursos": cursos,
        "es_admin": (perfil.rol == "admin")
    })


# ------------------------------------
# ELIMINAR ALUMNO
# admin = elimina cualquiera
# usuario = NO puede eliminar
# ------------------------------------
@login_required
def eliminar_alumno(request, id):
    perfil = Perfil.objects.get(user=request.user)

    if perfil.rol != "admin":
        return redirect("panel_usuario")

    Alumno.objects.get(id=id).delete()
    return redirect("listar_alumnos")
