from django.urls import path
from .views import login_view, logout_view, panel_admin, panel_usuario, registro_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('registro/', registro_view, name='registro'),


    # Paneles según rol
    path('panel/admin/', panel_admin, name='panel_admin'),
    path('panel/usuario/', panel_usuario, name='panel_usuario'),
]
