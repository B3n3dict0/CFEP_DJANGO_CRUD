from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, redirect
from .models import AcuerdoDetalle
from django.http import JsonResponse
from .models import AcuerdoDetalle
from datetime import datetime

@login_required
def menu_view(request):
    return render(request, 'cuentas/menu.html')

def directivo_view(request):
    return render(request, 'rutadir/directivo.html')

def operativo_view(request):
    context = {
        'fecha_actual': datetime.now()
    }
    return render(request, 'operativo/reunion_main.html', context)

def historial_acuerdos(request):
    return render(request, "operativo/partials/historial_acuerdo.html")

def crear_acuerdo(request):
    # Template para crear nuevos acuerdos
    return render(request, 'operativo/partials/crear_acuerdo.html')

#Aqui va para el crear formulario de acuerdos operativo
from django.http import JsonResponse
from .models import AcuerdoDetalle
from datetime import datetime

def guardar_matriz_acuerdos(request):
    if request.method != "POST":
        return JsonResponse({'success': False, 'error': 'Método no permitido'})

    filas = {}
    for key, value in request.POST.items():
        if '_' not in key:
            continue
        prefix, index = key.rsplit('_', 1)
        filas.setdefault(index, {})[prefix] = value

    try:
        for index, datos in filas.items():
            unidad_parada = datos.get('unidad_parada', '') == 'on'
            pendiente = datos.get('pendiente', '') == 'on'
            responsable = datos.get('responsable_manual') if datos.get('responsable_manual') else datos.get('responsable')

            numerador = int(datos.get('numerador', 0))
            porcentaje_avance = int(datos.get('porcentaje_avance', 0))
            fecha_limite = datos.get('fecha_limite')
            if fecha_limite:
                fecha_limite = datetime.strptime(fecha_limite, "%Y-%m-%d").date()
            else:
                fecha_limite = None

            AcuerdoDetalle.objects.create(
                numerador=numerador,
                tipo_unidad=datos.get('tipo_unidad', ''),
                descripcion=datos.get('descripcion', ''),
                unidad_parada=unidad_parada,
                pendiente=pendiente,
                fecha_limite=fecha_limite,
                responsable=responsable,
                porcentaje_avance=porcentaje_avance
            )
        return JsonResponse({'success': True})
    except Exception as e:
        print("Error al guardar:", e)
        return JsonResponse({'success': False, 'error': str(e)})


# Aqui consulto historial de operativo
def historial_acuerdo(request):
    # Obtener todos los acuerdos ordenados por fecha de creación descendente
    acuerdos = AcuerdoDetalle.objects.all().order_by('-creado_en')
    
    # Pasar los acuerdos al template
    return render(request, 'operativo/partials/historial_acuerdo.html', {'acuerdos': acuerdos})