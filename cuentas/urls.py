from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='cuentas/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('menu/', views.menu_view, name='menu'),
    # ruta a pagina directivo y operativo
    path('directivo/', views.directivo_view, name='directivo'),
    path('operativo/', views.operativo_view, name='operativo'),
    # Agrega las nuevas rutas para directivo
    path("crear-acuerdo_directivo/", views.crear_acuerdo_directivo, name="crear_acuerdo_directivo"),
    path('guardar-matriz-acuerdos/', views.guardar_matriz_acuerdos, name='guardar_matriz_acuerdos_directivo'),
    path('historial-acuerdo_directivo/', views.historial_acuerdo_directivo, name='historial_acuerdo_directivo'),
    # Agrega las nuevas rutas para operativo
    path("crear-acuerdo_operativo/", views.crear_acuerdo_operativo, name="crear_acuerdo_operativo"),
    path('guardar-matriz-acuerdos/', views.guardar_matriz_acuerdos, name='guardar_matriz_acuerdos'),
    path('historial-acuerdo_operativo/', views.historial_acuerdo_operativo, name='historial_acuerdo_operativo'),

   
]