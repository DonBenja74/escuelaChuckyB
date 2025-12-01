from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Perfil



# LOGIN
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            perfil = Perfil.objects.get(user=user)

            if perfil.rol == "admin":
                return redirect("panel_admin")
            else:
                return redirect("panel_usuario")

        return render(request, "gestorUser/login.html", {
            "error": "Usuario o contraseña incorrectos"
        })

    return render(request, "gestorUser/login.html")



# LOGOUT
def logout_view(request):
    logout(request)
    return redirect("login")



# REGISTRO
def registro_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        rol = "normal"

        # Crear usuario
        user = User.objects.create_user(username=username, password=password)

        # Crear perfil asociado
        Perfil.objects.create(user=user, rol=rol)

        return redirect("login")

    return render(request, "gestorUser/registro.html")



# PANEL ADMIN
@login_required
def panel_admin(request):
    perfil = Perfil.objects.get(user=request.user)

    if perfil.rol != "admin":
        return redirect("panel_usuario")

    return render(request, "gestorUser/panel_admin.html")


# PANEL USUARIO
@login_required
def panel_usuario(request):
    perfil = Perfil.objects.get(user=request.user)

    if perfil.rol != "normal":
        return redirect("panel_admin")

    return render(request, "gestorUser/panel_usuario.html")
