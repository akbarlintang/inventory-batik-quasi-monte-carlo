from __future__ import division

from django.shortcuts import render
from django.http import Http404
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse
from django.core import serializers
import json

from .models import *

from .forms import *

# import dependency pso dan periodic review
import pandas as pd
import csv
import numpy as np
import random
import math
from statistics import NormalDist
from scipy.stats import norm
from statistics import stdev
import os
import io, base64
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style('whitegrid')

import operator

iteration_halton = 0
halton_result = 0.00

# Dashboard
def dashboard_view(request):
    purchases = Purchase.objects.all()
    sales = Sales.objects.all()
    products = Item.objects.filter(type="JADI")
    outlets = Outlet.objects.all()

    purchase_total = 0
    for p in purchases:
        purchase_total += int(p.price) * int(p.amount)

    sales_total = 0
    for s in sales:
        sales_total = int(s.price) * int(s.amount)

    product_list = []
    for prod in products:
        product_list.append(prod.name)

    # return HttpResponse(product_list)
    
    context = {
        "purchases": purchase_total,
        "sales": sales_total,
        "products": products,
        "outlets": outlets,
        "product_list": product_list
    }
    return render(request, 'dashboard/index.html', context)

# Outlet
def outlet_view(request):
    outlets = Outlet.objects.all()
    context = {
        'outlets': outlets
    }

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

def outlet_update_view(request, outlet_id):
    try:
        # mengambil data outlet yang akan diubah berdasarkan outlet id
        outlet = Outlet.objects.get(pk=outlet_id)
    except Outlet.DoesNotExist:
        # Jika data outlet tidak ditemukan,
        # maka akan di redirect ke halaman 404 (Page not found).
        raise Http404("Outlet tidak ditemukan.")
    # Mengecek method pada request
    # Jika method-nya adalah POST, maka akan dijalankan
    # proses validasi dan penyimpanan data
    if request.method == 'POST':
        form = OutletForm(request.POST, instance=outlet)
        if form.is_valid():
            # Simpan perubahan data ke dalam table outlets
            form.save()
            # mengeset pesan sukses dan redirect ke halaman daftar outlet
            messages.success(request, 'Sukses Mengubah Outlet.')
            return redirect('outlet.index')
    # Jika method-nya bukan POST
    else:
        # membuat objek dari class OutletForm
        form = OutletForm(instance=outlet)
    # merender template form dengan memparsing data form
    return render(request, 'outlet/form.html', {'form': form})

def outlet_delete_view(request, outlet_id):
    try:
        # mengambil data outlet yang akan dihapus berdasarkan outlet id
        outlet = Outlet.objects.get(pk=outlet_id)
        # menghapus data dari table outlets
        outlet.delete()
        # mengeset pesan sukses dan redirect ke halaman daftar outlet
        messages.success(request, 'Sukses Menghapus Outlet.')
        return redirect('outlet.index')
    except Outlet.DoesNotExist:
        # Jika data outlet tidak ditemukan,
        # maka akan di redirect ke halaman 404 (Page not found).
        raise Http404("Outlet tidak ditemukan.")

def outlet_select_view(request, outlet_id):
    request.session['outlet_id'] = outlet_id

    if outlet_id == 'all':
        request.session['outlet_name'] = 'Semua Cabang'
    else:
        outlet = Outlet.objects.get(pk=outlet_id)
        request.session['outlet_name'] = outlet.name

    return HttpResponse(True)

def outlet_get_view(request):
    outlets = Outlet.objects.all()
    data = serializers.serialize('json', outlets)
    
    return HttpResponse(data, content_type="text/json-comment-filtered")

# Item
def item_view(request):
    items = Item.objects.filter(type="MENTAH")
    context = {
        'items': items
    }

    return render(request, 'item/index.html', context)

def item_create_view(request):
    # Mengecek method pada request
    # Jika method-nya adalah POST, maka akan dijalankan
    # proses validasi dan penyimpanan data
    if request.method == 'POST':
        # membuat objek dari class TaskForm
        form = ItemForm(request.POST, request.FILES)
        # Mengecek validasi form
        if form.is_valid():
            # Membuat Task baru dengan data yang disubmit
            new_task = ItemForm(request.POST, request.FILES)
            # Simpan data ke dalam table tasks
            new_task.save()
            # mengeset pesan sukses dan redirect ke halaman daftar task
            messages.success(request, 'Sukses Menambah Item baru.')
            return redirect('item.index')
    # Jika method-nya bukan POST
    else:
        # membuat objek dari class TaskForm
        form = ItemForm()
    # merender template form dengan memparsing data form
    return render(request, 'item/form.html', {'form': form})

def item_update_view(request, item_id):
    try:
        item = Item.objects.get(pk=item_id)
    except Item.DoesNotExist:
        raise Http404("Item tidak ditemukan.")
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sukses Mengubah Item.')
            return redirect('item.index')
    else:
        form = ItemForm(instance=item)
    return render(request, 'item/form.html', {'form': form})

def item_delete_view(request, item_id):
    try:
        item = Item.objects.get(pk=item_id)
        item.delete()
        messages.success(request, 'Sukses Menghapus Item.')
        return redirect('item.index')
    except Item.DoesNotExist:
        raise Http404("Item tidak ditemukan.")
    
# Product
def product_view(request):
    items = Item.objects.filter(type="JADI")
    context = {
        'items': items
    }

    return render(request, 'product/index.html', context)

def product_create_view(request):
    # Mengecek method pada request
    # Jika method-nya adalah POST, maka akan dijalankan
    # proses validasi dan penyimpanan data
    if request.method == 'POST':
        # membuat objek dari class TaskForm
        form = ItemForm(request.POST, request.FILES)
        # Mengecek validasi form
        if form.is_valid():
            # Membuat Task baru dengan data yang disubmit
            new_task = ItemForm(request.POST, request.FILES)
            # Simpan data ke dalam table tasks
            new_task.save()
            # mengeset pesan sukses dan redirect ke halaman daftar task
            messages.success(request, 'Sukses Menambah Item baru.')
            return redirect('product.index')
    # Jika method-nya bukan POST
    else:
        # membuat objek dari class TaskForm
        form = ItemForm()
    # merender template form dengan memparsing data form
    return render(request, 'product/form.html', {'form': form})

def product_update_view(request, product_id):
    try:
        item = Item.objects.get(pk=product_id)
    except Item.DoesNotExist:
        raise Http404("Item tidak ditemukan.")
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sukses Mengubah Item.')
            return redirect('product.index')
    else:
        form = ItemForm(instance=item)
    return render(request, 'product/form.html', {'form': form})

def product_delete_view(request, product_id):
    try:
        item = Item.objects.get(pk=product_id)
        item.delete()
        messages.success(request, 'Sukses Menghapus Item.')
        return redirect('product.index')
    except Item.DoesNotExist:
        raise Http404("Item tidak ditemukan.")

# Purchase
def purchase_view(request):
    if request.session.has_key('outlet_id'):
        if request.session['outlet_id'] == 'all':
            purchases = Purchase.objects.all().order_by('-created_at')
        else:
            purchases = Purchase.objects.filter(outlet_id=request.session['outlet_id']).order_by('-created_at')
    else:
        purchases = Purchase.objects.all()

    context = {
        'purchases': purchases
    }

    return render(request, 'purchase/index.html', context)

def purchase_create_view(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            temp = form.save()

            # Simpan transaction dari purchase
            Transaction.objects.create(
                item_id = request.POST.get('item',''),
                outlet_id = request.POST.get('outlet',''),
                purchase_id = temp.id,
                type = 'purchase'
            )

            messages.success(request, 'Sukses menambah pembelian baru.')
            return redirect('purchase.index')
    else:
        form = PurchaseForm()
    return render(request, 'purchase/form.html', {'form': form})

def purchase_update_view(request, purchase_id):
    try:
        purchase = Purchase.objects.get(pk=purchase_id)
    except Purchase.DoesNotExist:
        raise Http404("Pembelian tidak ditemukan.")
    if request.method == 'POST':
        form = PurchaseForm(request.POST, instance=purchase)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sukses Mengubah pembelian.')
            return redirect('purchase.index')
    else:
        form = PurchaseForm(instance=purchase)
    return render(request, 'purchase/form.html', {'form': form})

def purchase_delete_view(request, purchase_id):
    try:
        purchase = Purchase.objects.get(pk=purchase_id)
        purchase.delete()
        messages.success(request, 'Sukses menghapus pembelian.')
        return redirect('purchase.index')
    except Purchase.DoesNotExist:
        raise Http404("Pembelian tidak ditemukan.")

# Production
def production_view(request):
    if request.session.has_key('outlet_id'):
        if request.session['outlet_id'] == 'all':
            productions = Production.objects.all().order_by('-created_at')
        else:
            productions = Production.objects.filter(outlet_id=request.session['outlet_id']).order_by('-created_at')
    else:
        productions = Production.objects.all()

    context = {
        'productions': productions
    }

    return render(request, 'production/index.html', context)

def production_create_view(request):
    if request.method == 'POST':
        form = ProductionForm(request.POST)
        if form.is_valid():
            form.save()

            # Simpan stock dari production
            try:
                obj = Stock.objects.get(outlet=request.POST.get('outlet',''), item=request.POST.get('item',''))
                obj.amount = int(obj.amount) + int(request.POST.get('amount',''))
                obj.save()
            except Stock.DoesNotExist:
                Stock.objects.create(
                    item_id = request.POST.get('item',''),
                    outlet_id = request.POST.get('outlet',''),
                    amount = request.POST.get('amount',''),
                )

            messages.success(request, 'Sukses menambah produksi baru.')
            return redirect('production.index')
    else:
        form = ProductionForm()
    return render(request, 'production/form.html', {'form': form})

def production_update_view(request, production_id):
    try:
        production = Production.objects.get(pk=production_id)
    except Production.DoesNotExist:
        raise Http404("Produksi tidak ditemukan.")
    if request.method == 'POST':
        form = ProductionForm(request.POST, instance=production)
        if form.is_valid():
            # prod = Production.objects.get(id=form.id)
            return HttpResponse(request.POST.get('pk',''))
            temp = form.save()

            # Simpan stock dari production
            try:
                obj = Stock.objects.get(outlet=request.POST.get('outlet',''), item=request.POST.get('item',''))
                return HttpResponse(prod.amount)
                obj.amount = int(obj.amount) - int(prod.amount) + int(request.POST.get('amount',''))
                obj.save()
            except Stock.DoesNotExist:
                Stock.objects.create(
                    item_id = request.POST.get('item',''),
                    outlet_id = request.POST.get('outlet',''),
                    amount = request.POST.get('amount',''),
                )
            
            messages.success(request, 'Sukses Mengubah Produksi.')
            return redirect('production.index')
    else:
        form = ProductionForm(instance=production)
    return render(request, 'production/form.html', {'form': form})

def production_delete_view(request, production_id):
    try:
        production = Production.objects.get(pk=production_id)
        production.delete()
        messages.success(request, 'Sukses menghapus pembelian.')
        return redirect('production.index')
    except Production.DoesNotExist:
        raise Http404("Pembelian tidak ditemukan.")

# Sales
def sales_view(request):
    if request.session.has_key('outlet_id'):
        if request.session['outlet_id'] == 'all':
            sales = Sales.objects.all().order_by('-created_at')
        else:
            sales = Sales.objects.filter(outlet_id=request.session['outlet_id']).order_by('-created_at')
    else:
        sales = Sales.objects.all()

    context = {
        'sales': sales
    }

    return render(request, 'sales/index.html', context)

def sales_create_view(request):
    if request.method == 'POST':
        form = SalesForm(request.POST)
        if form.is_valid():
            temp = form.save()

            # Simpan transaction dari sales
            Transaction.objects.create(
                item_id = request.POST.get('item',''),
                outlet_id = request.POST.get('outlet',''),
                sales_id = temp.id,
                type = 'sales'
            )

            # Simpan stock dari production
            try:
                obj = Stock.objects.get(outlet=request.POST.get('outlet',''), item=request.POST.get('item',''))
                obj.amount = int(obj.amount) - int(request.POST.get('amount',''))
                obj.save()
            except Stock.DoesNotExist:
                Stock.objects.create(
                    item_id = request.POST.get('item',''),
                    outlet_id = request.POST.get('outlet',''),
                    amount = request.POST.get('amount',''),
                )

            messages.success(request, 'Sukses menambah penjualan baru.')
            return redirect('sales.index')
    else:
        form = SalesForm()
    return render(request, 'sales/form.html', {'form': form})

def sales_update_view(request, sales_id):
    try:
        sales = Sales.objects.get(pk=sales_id)
    except Sales.DoesNotExist:
        raise Http404("Penjualan tidak ditemukan.")
    if request.method == 'POST':
        form = SalesForm(request.POST, instance=sales)
        if form.is_valid():
            form.save()

            # Simpan stock dari production
            try:
                obj = Stock.objects.get(outlet=request.POST.get('outlet',''), item=request.POST.get('item',''))
                obj.amount = int(obj.amount) - int(request.POST.get('amount',''))
                obj.save()
            except Stock.DoesNotExist:
                Stock.objects.create(
                    item_id = request.POST.get('item',''),
                    outlet_id = request.POST.get('outlet',''),
                    amount = request.POST.get('amount',''),
                )

            messages.success(request, 'Sukses Mengubah penjualan.')
            return redirect('sales.index')
    else:
        form = SalesForm(instance=sales)
    return render(request, 'sales/form.html', {'form': form})

def sales_delete_view(request, sales_id):
    try:
        sales = Sales.objects.get(pk=sales_id)
        sales.delete()
        messages.success(request, 'Sukses menghapus penjualan.')
        return redirect('sales.index')
    except Sales.DoesNotExist:
        raise Http404("Penjualan tidak ditemukan.")

# Transaction
def transaction_view(request):
    if request.session.has_key('outlet_id'):
        if request.session['outlet_id'] == 'all':
            transactions = Transaction.objects.all().order_by('-created_at')
        else:
            transactions = Transaction.objects.filter(outlet_id=request.session['outlet_id']).order_by('-created_at')
    else:
        transactions = Transaction.objects.all()
    
    context = {
        'transactions': transactions
    }

    return render(request, 'transaction/index.html', context)

# Stocks
def stock_view(request):
    if request.session.has_key('outlet_id'):
        if request.session['outlet_id'] == 'all':
            stocks = Stock.objects.all()
        else:
            stocks = Stock.objects.filter(outlet_id=request.session['outlet_id'])
    else:
        stocks = Stock.objects.all()
    
    context = {
        'stocks': stocks
    }

    return render(request, 'stock/index.html', context)

# Export
def export_view(request):
    if request.method == 'POST':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="ExportData.csv"'        
        writer = csv.writer(response)
        writer.writerow(['Sales Data'])
        writer.writerow(['No', 'Nama Barang','Biaya Pesan','Permintaan Bahan Baku','Biaya Simpan','Biaya Kekurangan','Harga Produk','Lead Time Pemenuhan', 'Standar Deviasi'])
        items = Item.objects.filter(type="JADI").all()
        for idx, item in enumerate(items):
            sales = Sales.objects.all().filter(item_id=item.id)

            # return HttpResponse(len(sales))
            sales_count = 0
            sales_list = []

            for sale in sales:
                sales_count += sale.amount
                sales_list.append(sale.amount)

            biaya_kekurangan = (item.price * 7.5 / 100) + item.price
            n = len(sales_list)
            if n < 2:
                standar_deviasi = sales_list[0]
            else:
                # standar_deviasi = stdev(sales_list)
                standar_deviasi = np.std(sales_list)
            
            # Write row excel
            row = [idx+1, item.name, item.biaya_pesan, sales_count, 225805, biaya_kekurangan, item.price, item.lead_time, standar_deviasi]
            writer.writerow(row)
        return response
    
    context = {
        # 'transactions': transactions
    }

    return render(request, 'export/index.html', context)

# Halton
# Drawing from a log normal distribution
def halton(dim: int, nbpts: int):
    h = np.full(nbpts * dim, np.nan)
    p = np.full(nbpts, np.nan)
    P = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    lognbpts = math.log(nbpts + 1)
    for i in range(dim):
        b = P[i]
        n = int(math.ceil(lognbpts / math.log(b)))
        for t in range(n):
            p[t] = pow(b, -(t + 1))

        for j in range(nbpts):
            d = j + 1
            sum_ = math.fmod(d, b) * p[0]
            for t in range(1, n):
                d = math.floor(d / b)
                sum_ += math.fmod(d, b) * p[t]

            h[j*dim + i] = sum_
    return h.reshape(nbpts, dim)

def getHalton(iteration_halton):

    if iteration_halton == 0:
        N=100
    else:
        N=iteration_halton
    seq = halton(2, N)
    accum = 0
    for i in range(N):
        x = 1 + seq[i][0]*(5 - 1)
        y = 1 + seq[i][1]*(5**2 - 1**2)
        accum += x**2
    volume = 5 - 1
    halton_result = volume * accum / float(N) /100
    return halton_result

def daily_demand(mean, sd):
    global halton_result
    random_num = np.random.uniform(0, 1)
    if random_num > halton_result:
        return 0
    else:
        return np.random.normal(mean, sd)
    
def monte_carlo(M, product, review_period=30):
    product_mc = {}
    product_mc["nama_barang"] = product['nama_barang']
    product_mc["biaya_pesan"] = product['biaya_pesan']
    product_mc["permintaan_baku"] = product['permintaan_baku']
    product_mc["biaya_simpan"] = product['biaya_simpan']
    product_mc["biaya_kekurangan"] = product['biaya_kekurangan']
    product_mc["harga_produk"] = product['harga_produk']
    product_mc["lead_time"] = product['lead_time']
    product_mc["standar_deviasi"] = product['standar_deviasi']
    
    # lead_time = product["lead_time"]
    mean = product["permintaan_baku"] / 30
    sd = product["standar_deviasi"]

    total_demand = 0

    for day in range(1, 365):
        day_demand = round(daily_demand(mean, sd))

        if day_demand >= 0:
            total_demand += day_demand
    
    product_mc["permintaan_baku"] = total_demand
    
    return product_mc

def calculate_profit(data, product):
    unit_cost = product["harga_produk"]
    selling_price = product["harga_produk"]
    holding_cost = product["biaya_simpan"]
    order_cost = product["biaya_pesan"]
    days = 150

    revenue = sum(data['units_sold']) * selling_price
    Co = len(data['orders']) * order_cost
    # Ch = sum(data['inv_level']) * holding_cost * size * (1 / days)
    Ch = sum(data['inv_level']) * holding_cost * (1 / days)
    cost = sum(data['orders']) * unit_cost

    profit = revenue - cost - Co - Ch

    return profit

def mc_simulation(product, M, num_simulations=10):
    total_biaya_penyimpanan_list = []
    for sim in range(num_simulations):
        data = monte_carlo(M, product)

        # Calculating total biaya penyimpanan
        total_biaya_penyimpanan = per_review(data)
        total_biaya_penyimpanan_list.append(total_biaya_penyimpanan)

    return total_biaya_penyimpanan_list

def p_review(product, low, high, step=50):
    m_range = [i for i in range(low, high, step)]
    review_dict = {}
    for M in m_range:
        p_list, o_list = mc_simulation(product, M)
        review_dict[M] = (np.mean(p_list), np.quantile(p_list, 0.05), np.quantile(p_list, 0.95), np.std(p_list), np.mean(o_list))

    return review_dict

def p_review_optimum(product, M, sim=10):
    review_dict = {}
    p_list, o_list = mc_simulation(product, M, sim)
    review_dict[M] = (np.mean(p_list), np.quantile(p_list, 0.05), np.quantile(p_list, 0.95), np.std(p_list), np.mean(o_list))

    return review_dict

def per_review(product):
    T_temp = []
    To_temp = []
    s_temp = []
    S_temp = []
    # for i in range(5):
    # Hitung nilai To
    to = math.sqrt((2 * product["biaya_pesan"]) / (product["permintaan_baku"] * product["biaya_simpan"]))

    # Hitung nilai alpha dan R
    alpha = to * product["biaya_simpan"] / product["biaya_kekurangan"]
    z_alpha = round((NormalDist().inv_cdf(alpha) * -1), 2)

    fz_alpha = round(norm.pdf(2.22 , loc = 0 , scale = 1 ), 5)
    # wz_alpha = fz_alpha - (z_alpha * (1 - fz_alpha))
    wz_alpha = round((fz_alpha - 0.00001), 5)

    R = round((product["permintaan_baku"] * to) + (product["permintaan_baku"] * product["lead_time"]) + (z_alpha * (math.sqrt(to + product["lead_time"]))))

    # Hitung total biaya total persediaan
    N = math.ceil(product["standar_deviasi"] * ((math.sqrt(to + product["lead_time"])) * ((fz_alpha - (z_alpha * wz_alpha)) * -1)))

    T = (product["permintaan_baku"] * product["harga_produk"]) + (product["biaya_pesan"] / to) + (product["biaya_simpan"] * (R - (product["permintaan_baku"] * product["lead_time"]) + (product["permintaan_baku"] * to / 2))) + (product["biaya_kekurangan"] / to * N)

    # Hitung nilai XR, XRL, dan sigma_RL
    XR = to * product["permintaan_baku"]
    XRL = (to + product["lead_time"]) * product["permintaan_baku"]
    sigma_RL = (to + product["lead_time"]) * product["standar_deviasi"]

    Qp = round(1.3 * (XR ** 0.494) * ((product["biaya_pesan"] / product["biaya_simpan"]) ** 0.506) * ((1 + ((sigma_RL ** 2) / (XR ** 2))) ** 0.116))
    z = round(math.sqrt((Qp * product["biaya_simpan"]) / (sigma_RL * product["biaya_kekurangan"])), 2)
    Sp = round((0.973 * XRL) + (sigma_RL * ((0.183 / z) + 1.063 - (2.192 * z))), 2)

    k = round(product["biaya_simpan"] / (product["biaya_simpan"] + product["biaya_kekurangan"]), 2)

    So = round(XRL + (k * sigma_RL))

    To = round(to * 100)
    s = round(Sp)
    S = round(Sp + Qp)

    # T_temp.append(T)
    # To_temp.append(To)
    # s_temp.append(s)
    # S_temp.append(S)
    
    # for idx, temp in enumerate(T_temp):
    #     if temp == min(T_temp):
    #         index = idx
    #         break

    return T

# Periodic Review
def periodic_view(request):
    if request.method == 'POST':
        array = []
        data = []

        read_file = request.FILES['file']
        csv_data = pd.read_csv(read_file, header=1, encoding="UTF-8")

        for dt in csv_data.values:
            array_data = {}
            array_data['nama_barang'] = dt[1]
            array_data['biaya_pesan'] = dt[2]
            array_data['permintaan_baku'] = dt[3]
            array_data['biaya_simpan'] = dt[4]
            array_data['biaya_kekurangan'] = dt[5]
            array_data['harga_produk'] = dt[6]
            array_data['lead_time'] = dt[7] / 100
            array_data['standar_deviasi'] = dt[8]

            array.append(array_data)

        # define var
        iteration_h = 10
        simulation_num = 10

        global iteration_halton
        global halton_result

        halton_result = getHalton(iteration_h)

        iteration_halton = iteration_h

        simulation_biaya = []
        tp_list_product = []
        monte_carlo_product = []
        img_monte_carlo_product = []
        review_product = []
        review_optimum = []

        high_low_temp = []

        f = plt.figure(figsize=(14, 14))
        gs = f.add_gridspec(2, 2)

        for index, x in enumerate(array):
            product = {}
            product["nama_barang"] = x['nama_barang']
            product["biaya_pesan"] = x['biaya_pesan']
            product["permintaan_baku"] = x['permintaan_baku']
            product["biaya_simpan"] = x['biaya_simpan']
            product["biaya_kekurangan"] = x['biaya_kekurangan']
            product["harga_produk"] = x['harga_produk']
            product["lead_time"] = x['lead_time']
            product["standar_deviasi"] = x['standar_deviasi']
            
            high_low_temp.append([x['permintaan_baku'],x['permintaan_baku'],10])

            nilai_optimum = []
            # for i in range(1,5):
            tp_list = mc_simulation(product, 3000, 10)
            mc_result = monte_carlo(3000, product)
            # monte_carlo_product.append(monte_carlo(3000, product))
            # for a in range(1,simulation_num+1):
            #     periodic_review_temp = p_review(product, high_low_temp[index][0],high_low_temp[index][1],high_low_temp[index][2])
            # review_product.append(periodic_review_temp)
            # prod_review_temp = max(periodic_review_temp.items(), key=operator.itemgetter(1))
            # review_optimum.append(p_review_optimum(product, prod_review_temp[0]))
            # nilai_optimum.append(prod_review_temp[0])

            biaya_penyimpanan = per_review(product)

            tp_list_product.append(tp_list)
            temp = []
            temp.append("Product ")
            temp.append(np.mean(tp_list_product))
            temp.append(np.std(tp_list_product))
            simulation_biaya.append(temp)

            ax = f.add_subplot(gs[0, 0])
            sns.distplot(tp_list_product,kde=False)
            
            temp = {
                # 'To': round(to),
                # 's': round(s),
                # 'S': round(S),
                'mc_result': mc_result,
                'nama_barang': product["nama_barang"],
                'biaya_penyimpanan': round(biaya_penyimpanan),
                'total_biaya_penyimpanan': round(min(tp_list)),
            }

            data.append(temp)

        flike = io.BytesIO()
        f.savefig(flike)
        simulation_profit_plot = base64.b64encode(flike.getvalue()).decode()
        
        context = {
            'data': data,
            'simulation_profit_plot': simulation_profit_plot
        }

        return render(request, 'periodic/calculation.html', context)
    
    context = {
        'data': '',
    }

    return render(request, 'periodic/index.html', context)