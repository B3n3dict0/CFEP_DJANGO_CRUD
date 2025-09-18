from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='cuentas/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('menu/', views.menu_view, name='menu'),

    # Rutas operativa
    path('operativo/', views.operativo_view, name='operativo'),
    path('crear-acuerdo_operativo/', views.crear_acuerdo_operativo, name='crear_acuerdo_operativo'),
    path('historial-acuerdo_operativo/', views.historial_acuerdo_operativo, name='historial_acuerdo_operativo'),
    path('guardar-matriz-acuerdos-operativa/', views.guardar_matriz_acuerdos_operativa, name='guardar_matriz_acuerdos_operativa'),

    # Rutas directiva
    path('directivo/', views.directivo_view, name='directivo'),
    path('crear-acuerdo_directivo/', views.crear_acuerdo_directivo, name='crear_acuerdo_directivo'),
    path('historial-acuerdo_directivo/', views.historial_acuerdo_directivo, name='historial_acuerdo_directivo'),
    path('guardar-matriz-acuerdos-directiva/', views.guardar_matriz_acuerdos_directiva, name='guardar_matriz_acuerdos_directiva'),

    # Integrantes y reuniones
    path("reunion/", views.reunion_main, name="reunion_main"),
    path("agregar-integrante/", views.agregar_integrante, name="agregar_integrante"),
    path("eliminar-integrante/", views.eliminar_integrante, name="eliminar_integrante"),
]
