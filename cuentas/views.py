from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, redirect
from .models import AcuerdoDetalle, AcuerdoDirectivo
from django.http import JsonResponse
from .models import AcuerdoDetalle
from datetime import datetime
from .models import Integrante

@login_required
def menu_view(request):
    return render(request, 'cuentas/menu.html')

# toda la logica en vista directiva
def directivo_view(request):
    context = {
        'fecha_actual': datetime.now()
    }
    return render(request, 'directivo/reunion_main.html', context)

def historial_acuerdo_directivo(request):
    return render(request, "directivo/partials/historial_acuerdo_directivo.html")

def crear_acuerdo_directivo(request):
    return render(request, 'directivo/partials/crear_acuerdo_directivo.html')

def historial_acuerdo_directivo(request):
    acuerdos = AcuerdoDetalle.objects.all().order_by('-creado_en')
    return render(request, 'directivo/partials/historial_acuerdo_operativo.html', {'acuerdos': acuerdos})

# toda la logica en vista operativa
def operativo_view(request):
    context = {
        'fecha_actual': datetime.now()
    }
    return render(request, 'operativo/reunion_main.html', context)

def reunion_directiva(request): #aqui se inserta los integrantes
    integrantes = Integrante.objects.filter(categoria="directiva")
    return render(request, "directiva/reunion_main.html", {"integrantes": integrantes})

def historial_acuerdo_operativo(request):
    return render(request, "operativo/partials/historial_acuerdo_operativo.html")

def crear_acuerdo_operativo(request):
    return render(request, 'operativo/partials/crear_acuerdo_operativo.html')

def guardar_matriz_acuerdos(request): #Aqui va para el crear formulario de acuerdos operativo
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

def historial_acuerdo_operativo(request):
    acuerdos = AcuerdoDetalle.objects.all().order_by('-creado_en')
    return render(request, 'operativo/partials/historial_acuerdo_operativo.html', {'acuerdos': acuerdos})

def reunion_main(request): #aqui es para cargar insertar los integrantes
    integrantes = Integrante.objects.all()
    return render(request, "operativo/reunion_main.html", {"integrantes": integrantes})


def reunion_main(request):
    integrantes = Integrante.objects.all()
    return render(request, "operativo/reunion_main.html", {"integrantes": integrantes})

@csrf_exempt
def agregar_integrante(request):
    if request.method == "POST":
        data = json.loads(request.body)
        rol = data.get("rol")

        integrante, creado = Integrante.objects.get_or_create(rol=rol)
        if creado:
            return JsonResponse({"success": True, "rol": rol})
        else:
            return JsonResponse({"success": False, "message": "Ya existe este integrante"})

@csrf_exempt
def eliminar_integrante(request):
    if request.method == "POST":
        data = json.loads(request.body)
        rol = data.get("rol")

        try:
            integrante = Integrante.objects.get(rol=rol)
            integrante.delete()
            return JsonResponse({"success": True})
        except Integrante.DoesNotExist:
            return JsonResponse({"success": False, "message": "No existe este integrante"})
        
        

def guardar_matriz_acuerdos(request):
    if request.method == "POST":
        try:
            acuerdos = []
            data = request.POST

            # agrupa por contador (ej: numerador_1, descripcion_1, etc.)
            filas = {}
            for key, value in data.items():
                # separar por "_"
                if "_" in key:
                    campo, idx = key.rsplit("_", 1)
                    if idx not in filas:
                        filas[idx] = {}
                    filas[idx][campo] = value

            # recorrer filas y guardar en la base de datos
            for fila in filas.values():
                acuerdo = AcuerdoDirectivo(
                    numerador=int(fila.get("numerador", 0)),
                    tipo_unidad=fila.get("tipo_unidad", ""),
                    descripcion=fila.get("descripcion", ""),
                    unidad_parada=True if fila.get("unidad_parada") == "on" else False,
                    fecha_limite=datetime.strptime(fila.get("fecha_limite", ""), "%Y-%m-%d").date(),
                    pendiente=True if fila.get("pendiente") == "on" else False,
                    responsable=fila.get("responsable", ""),
                    responsable_manual=fila.get("responsable_manual", "").strip() or None,
                    porcentaje_avance=int(fila.get("porcentaje_avance", 0)),
                )
                acuerdo.save()
                acuerdos.append(acuerdo.id)

            return JsonResponse({"success": True, "ids": acuerdos})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Método no permitido"})

def historial_acuerdo_directivo(request):
    acuerdos = AcuerdoDirectivo.objects.all().order_by("-creado_en")
    return render(request, "directivo/partials/historial_acuerdo_directivo.html", {"acuerdos": acuerdos})