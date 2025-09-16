from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime

@login_required
def menu_view(request):
    return render(request, 'cuentas/menu.html')

def directivo_view(request):
    return render(request, 'rutadir/directivo.html')

def operativo_view(request):
    # Pasar la fecha actual al template
    context = {
        'fecha_actual': datetime.now()
    }
    return render(request, 'operativo/reunion_main.html', context)