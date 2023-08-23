from django.shortcuts import render
from django.http import Http404
from django.contrib import messages

from .models import *

from .forms import *

# Dashboard
def dashboard_view(request):
    context = {}
    return render(request, 'dashboard/index.html', context)


# Outlet
def outlet_view(request):
    outlets = Outlet.objects.all()
    context = {
        'outlets': outlets
    }

    # test
    return render(request, 'outlet/index.html', context)

def outlet_create_view(request):
    # Mengecek method pada request
    # Jika method-nya adalah POST, maka akan dijalankan
    # proses validasi dan penyimpanan data
    if request.method == 'POST':
        # membuat objek dari class TaskForm
        form = OutletForm(request.POST)
        # Mengecek validasi form
        if form.is_valid():
            # Membuat Task baru dengan data yang disubmit
            new_task = OutletForm(request.POST)
            # Simpan data ke dalam table tasks
            new_task.save()
            # mengeset pesan sukses dan redirect ke halaman daftar task
            messages.success(request, 'Sukses Menambah Outlet baru.')
            return redirect('outlet.index')
    # Jika method-nya bukan POST
    else:
        # membuat objek dari class TaskForm
        form = OutletForm()
    # merender template form dengan memparsing data form
    return render(request, 'outlet/form.html', {'form': form})
