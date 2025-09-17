from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='cuentas/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('menu/', views.menu_view, name='menu'),
    # Agrega las nuevas rutas para directivo y operativo
    path('directivo/', views.directivo_view, name='directivo'),
    path('operativo/', views.operativo_view, name='operativo'),
    
    path("crear-acuerdo/", views.crear_acuerdo, name="crear_acuerdo"),
    path('guardar-matriz-acuerdos/', views.guardar_matriz_acuerdos, name='guardar_matriz_acuerdos'),
    path('historial-acuerdo/', views.historial_acuerdo, name='historial_acuerdo'),

   
]