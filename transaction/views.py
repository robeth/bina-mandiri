from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from transaction.models import Nasabah, Vendor, Pembelian, Penjualan, DetailPenjualan, Stok, Kategori, Konversi, DetailIn, Penarikan
from transaction.db import q_nasabah, q_vendor, q_pembelian, q_penjualan, q_konversi, q_nasabah_detail, q_vendor_detail, q_penjualan_detail, q_pembelian_detail, q_konversi_detail, q_remaining, q_get_last_stock, q_home, q_is_pembelian_clear , q_is_konversi_clear, q_laba_rugi, q_nasabah_all, q_arus_barang
from transaction.forms import NasabahForm, VendorForm, PembelianForm, PenjualanForm, KonversiForm, PenarikanForm, KategoriForm, LoginForm
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.utils.dateparse import parse_date
from transaction.helper import paginate_data

ENTRY_PER_PAGE = 100

def is_valid_date(inputDate):
	try: 
		n = parse_date(inputDate)
	except ValueError:
		return False

	if n :
		return True
	else:
		return False

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def home(request):
	context = { 'nasabah': q_nasabah, 'data': q_home(), 'user': request.user}
	return render(request, 'transaction/home.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_please(request):
	logout(request)
	return HttpResponseRedirect(reverse('django.contrib.auth.views.login'))

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def kategori(request):
	if request.method == 'POST':
		form = KategoriForm(request.POST, request.FILES)
		if form.is_valid():
			print "Valid"
			form.save()
			return HttpResponseRedirect(reverse('nasabah'))
	else:
		form = KategoriForm()
	kk = Kategori.objects.all()
	context = {'data': kk, 'form':form, 'user': request.user}
	return render(request, 'transaction/kategori.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def kategori_edit(request, kategori_id):
	kk = Kategori.objects.filter(id=kategori_id)
	if len(kk) < 1:
		return HttpResponseRedirect(reverse('kategori'))

	if request.method == 'POST':
		form = KategoriForm(request.POST, request.FILES, instance=kk[0])
		if form.is_valid():
			print "Valid"
			form.save()
			return HttpResponseRedirect(reverse('kategori'))
	else:
		form = KategoriForm(instance=kk[0])
	context = {'form':form, 'id': kategori_id, 'user': request.user}
	return render(request, 'transaction/kategori_edit.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def kategori_add(request):
	if request.method == 'POST':
		form = KategoriForm(request.POST, request.FILES)
		if form.is_valid():
			print "Valid"
			form.save()
			return HttpResponseRedirect(reverse('kategori'))
	else:
		form = KategoriForm()
	context = {'form':form, 'user': request.user}
	return render(request, 'transaction/kategori_add.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def nasabah(request):
	context = { 'nasabah': q_nasabah("individu"), 'user': request.user}
	return render(request, 'transaction/nasabah.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def nasabah_kolektif(request):
	context = { 'nasabah': q_nasabah("kolektif"), 'user': request.user}
	return render(request, 'transaction/nasabah_kolektif.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def nasabah_add(request):
	if request.method == 'POST':
		form = NasabahForm(request.POST, request.FILES)
		if form.is_valid():
			print "Valid"
			form.save()
			return HttpResponseRedirect(reverse('nasabah'))
	else:
		form = NasabahForm()

	context = {'form':form, 'user': request.user}
	return render(request, 'transaction/nasabah_add.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def nasabah_edit(request, nasabah_id):
	nn = Nasabah.objects.filter(id=nasabah_id)
	if len(nn) < 1:
		return HttpResponseRedirect(reverse('nasabah'))

	if request.method == 'POST':
		form = NasabahForm(request.POST, request.FILES, instance=nn[0])
		if form.is_valid():
			print "Valid"
			form.save()
			return HttpResponseRedirect(reverse('nasabah'))
	else:
		form = NasabahForm(instance=nn[0])

	context = {'form':form, 'id': nasabah_id, 'user': request.user}
	return render(request, 'transaction/nasabah_edit.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def vendor(request):
	context = { 'vendor': q_vendor, 'user': request.user}
	return render(request, 'transaction/vendor.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def vendor_add(request):
	if request.method == 'POST':
		form = VendorForm(request.POST, request.FILES)
		if form.is_valid():
			print "Valid"
			form.save()
			return HttpResponseRedirect(reverse('vendor'))
	else:
		form = VendorForm()
	context = { 'form': form, 'user': request.user}
	return render(request, 'transaction/vendor_add.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def vendor_edit(request, vendor_id):
	vv = Vendor.objects.filter(id=vendor_id)
	if len(vv) < 1:
		return HttpResponseRedirect(reverse('vendor'))

	if request.method == 'POST':
		form = VendorForm(request.POST, request.FILES, instance=vv[0])
		if form.is_valid():
			print "Valid"
			form.save()
			return HttpResponseRedirect(reverse('vendor'))
	else:
		form = VendorForm(instance=vv[0])
	context = { 'form': form, 'id': vendor_id, 'user': request.user}
	return render(request, 'transaction/vendor_edit.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def pembelian(request):
	pembelian_entries = paginate_data(
		Pembelian.objects.all().order_by('-tanggal'),
		request.GET.get('page'),
		100)
		
	context = { 'pembelian': pembelian_entries, 'user': request.user}
	return render(request, 'transaction/pembelian.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def pembelian_add(request):
	if request.method == 'POST':
		form = PembelianForm(request.POST)
		if form.is_valid():
			print "Valid"
			# Add new stock items
			data = form.data

			n = Nasabah.objects.get(id=data['nasabah'])
			p = Pembelian(tanggal=data['tanggal'], nasabah=n, nota=data['nota'])
			p.save()

			limit = int(data['total'])
			i = 1
			temp_total = 0
			while i <= limit:
				k = Kategori.objects.get(id=data['stok'+str(i)])
				s = Stok(kategori = k,
						tanggal = data['tanggal'],
						jumlah = data['jumlah' + str(i)],
						harga = data['harga' + str(i)])
				s.save()
				p.stocks.add(s)
				temp_total += float(s.jumlah) * float(s.harga)
				i += 1
				print temp_total

			p.save()
			if 'cash' in data:
				p_cash = Penarikan(tanggal=data['tanggal'], nasabah=n, total=temp_total)
				if 'nota_cash' in data:
					p_cash.nota = data['nota_cash']
				p_cash.save()

			return HttpResponseRedirect(reverse('pembelian'))
	else:
		form = PembelianForm()

	kk = Kategori.objects.all().order_by('kode')
	options = []

	for k in kk:
		options.append({'kode' : k.kode, 'nama': k.nama, 'id': k.id, 'stabil': str(k.stabil)})

	context = {'form': form, 'options' : options, 'user': request.user}
	return render(request, 'transaction/pembelian_add.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def pembelian_del(request, pembelian_id):
	p = None
	try:
		p = Pembelian.objects.get(id=pembelian_id)
	except Pembelian.DoesNotExist:
		message_error = "Pembelian: id="+str(pembelian_id)+" not exists"

	if p:
		valid = q_is_pembelian_clear(pembelian_id)
		if valid:
			p.delete()

	return HttpResponseRedirect(reverse('pembelian'))

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def penjualan(request): 
	penjualan_entries = paginate_data(
		Penjualan.objects.all().order_by('-tanggal'),
		request.GET.get('page'),
		100)

	context = { 'penjualan': penjualan_entries, 'user': request.user}
	return render(request, 'transaction/penjualan.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def penjualan_add(request):
	if request.method == 'POST':
		form = PenjualanForm(request.POST)
		if form.is_valid():
			print "Valid"
			data = form.data
			v = Vendor.objects.get(id=data['vendor'])
			p = Penjualan(tanggal=data['tanggal'], vendor = v, nota=data['nota'])
			p.save()

			limit = int(data['total'])
			i = 1
			while i <= limit:
				stocks = q_get_last_stock(data['stok'+str(i)], data['jumlah'+str(i)])
				for s in stocks:
					st = Stok.objects.get(id=s['id'])
					dp = DetailPenjualan(stok=st, penjualan=p, jumlah=s['jumlah'], harga=data['harga'+str(i)])
					dp.save()
				i += 1
			return HttpResponseRedirect(reverse('penjualan'))
	else:
		form = PenjualanForm()

	context = { 'remaining':  q_remaining(), 'form':form, 'user': request.user}
	return render(request, 'transaction/penjualan_add.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def penjualan_del(request, penjualan_id):
	p = None
	try:
		p = Penjualan.objects.get(id=penjualan_id)
	except Penjualan.DoesNotExist:
		message_error = "Penjualan: id="+str(penjualan_id)+" not exists"

	if p:
		p.delete()

	return HttpResponseRedirect(reverse('penjualan'))

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def konversi(request):
	context = { 'konversi': q_konversi, 'user': request.user}
	return render(request, 'transaction/konversi.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def konversi_add(request):
	if request.method == 'POST':
		form = KonversiForm(request.POST)
		if form.is_valid():
			print "Valid"
			data = form.data
			k = Konversi(tanggal=data['tanggal'], kode=data['kode'])
			k.save()

			total_nilai = 0
			total_jumlah = 0

			i = 1
			limit = int(data['total'])
			while i <= limit:
				stocks = q_get_last_stock(data['stok_in'+str(i)], data['jumlah_in'+str(i)])
				for s in stocks:
					st = Stok.objects.get(id=s['id'])
					total_nilai += float(st.harga) * float(s['jumlah'])
					print "total_nilai: "+str(float(st.harga)) + " * " + str(float(data['jumlah_in'+str(i)]))
					di = DetailIn(stok=st, konversi=k, jumlah=s['jumlah'])
					di.save()
				i += 1

			i = 1
			limit = int(data['total2'])
			while i <= limit:
				total_jumlah += float(data['jumlah_out'+str(i)])
				i += 1

			harga_satuan = total_nilai / total_jumlah
			print "satuan:" + str(harga_satuan)
			print "total nilai:" + str(total_nilai)
			print "total jumlah" + str(total_jumlah)
			i=1
			# Saving new stocks
			while i <= limit:
				kk = Kategori.objects.get(kode=data['stok_out'+str(i)])
				s = Stok(kategori = kk,
						tanggal = data['tanggal'],
						jumlah = float(data['jumlah_out' + str(i)]),
						harga = harga_satuan)

				s.save()
				k.outs.add(s)
				i += 1
			k.save()
			return HttpResponseRedirect(reverse('konversi'))
	else:
		form = KonversiForm()

	kk = Kategori.objects.all().order_by('kode')
	options = []

	for k in kk:
		options.append({'kode' : k.kode, 'nama': k.nama, 'id': k.id})

	context = {'remaining' : q_remaining(), 'category': options,'form': form, 'user': request.user}
	return render(request, 'transaction/konversi_add.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def penarikan(request):
	p = Penarikan.objects.order_by('tanggal')
	context = { 'penarikan': p, 'user': request.user}
	return render(request, 'transaction/penarikan.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def penarikan_add(request):
	if request.method == 'POST':
		form = PenarikanForm(request.POST)
		if form.is_valid():
			print "Valid"
			form.save()
			return HttpResponseRedirect(reverse('penarikan'))
	else:
		form = PenarikanForm()

	context = { 'form': form, 'nasabah':q_nasabah_all(), 'user': request.user}
	return render(request, 'transaction/penarikan_add.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def penarikan_del(request, penarikan_id):
	p = None
	try:
		p = Penarikan.objects.get(id=penarikan_id)
	except Penarikan.DoesNotExist:
		message_error = "Penarikan: id="+str(penarikan_id)+" not exists"

	if p:
		p.delete()

	return HttpResponseRedirect(reverse('penarikan'))

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def nasabah_detail(request, nasabah_id):
	context = {'detail': q_nasabah_detail(nasabah_id), 'user': request.user}
	return render(request, 'transaction/nasabah_detail.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def vendor_detail(request, vendor_id):
	res = q_vendor_detail(vendor_id)
	res['general'] = Vendor.objects.filter(id=vendor_id)
	context = {'detail': res, 'user': request.user}
	return render(request, 'transaction/vendor_detail.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def pembelian_detail(request, pembelian_id):
	res = q_pembelian_detail(pembelian_id)
	res['general'] = Pembelian.objects.filter(id=pembelian_id)
	res['user'] = request.user
	res['can_delete'] = q_is_pembelian_clear(pembelian_id)
	return render(request, 'transaction/pembelian_detail.html', res)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def pembelian_print(request, pembelian_id):
	res = q_pembelian_detail(pembelian_id)
	res['general'] = Pembelian.objects.filter(id=pembelian_id)
	res['user'] = request.user
	return render(request, 'transaction/pembelian_print.html', res)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def penjualan_detail(request, penjualan_id):
	res = q_penjualan_detail(penjualan_id)
	res['general'] = Penjualan.objects.filter(id=penjualan_id)
	res['user'] = request.user
	return render(request, 'transaction/penjualan_detail.html', res)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def penjualan_print(request, penjualan_id):
	res = q_penjualan_detail(penjualan_id)
	res['general'] = Penjualan.objects.filter(id=penjualan_id)
	res['user'] = request.user
	return render(request, 'transaction/penjualan_print.html', res)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def laba_rugi(request):
	from datetime import datetime
	current = datetime.now()
	month = current.month
	year = current.year
	if request.method == "POST":
		if request.POST['month']:
			month = int(request.POST['month'])
		if request.POST['year']:
			year = int(request.POST['year'])
	res = {}
	res['user'] = request.user

	res['penjualan'] = q_laba_rugi(month, year)
	res['total_bruto'] = 0
	res['total_hpp'] = 0
	for p in res['penjualan']:
		res['total_bruto'] += float(p['bruto'])
		res['total_hpp'] += float(p['hpp'])
	res['total_netto'] = res['total_bruto'] - res['total_hpp']
	
	res['bulan'] = month
	res['tahun'] = year
	res['year_range'] = range(2013, current.year+1)
	return render(request, 'transaction/laba_rugi.html', res)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def arus_barang(request):
	from datetime import datetime
	current = datetime.now()
	month = current.month
	year = current.year
	if request.method == "POST":
		if request.POST['month']:
			month = int(request.POST['month'])
		if request.POST['year']:
			year = int(request.POST['year'])
	res = {}
	res['user'] = request.user

	res['arus'] = q_arus_barang(month, year)
	
	res['bulan'] = month
	res['tahun'] = year
	res['year_range'] = range(2013, current.year+1)
	return render(request, 'transaction/arus_barang.html', res)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def konversi_detail(request, konversi_id):
	res = q_konversi_detail(konversi_id)
	res['general'] = Konversi.objects.filter(id=konversi_id)
	res['user'] = request.user
	res['can_delete'] = q_is_konversi_clear(konversi_id)
	return render(request, 'transaction/konversi_detail.html', res)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def konversi_del(request, konversi_id):
	k = None
	try:
		k = Konversi.objects.get(id=konversi_id)
	except Konversi.DoesNotExist:
		message_error = "Konversi: id="+str(konversi_id)+" not exists"

	if k:
		valid = q_is_konversi_clear(konversi_id)
		if valid:
			k.outs.all().delete()
			k.delete()

	return HttpResponseRedirect(reverse('konversi'))

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def stok_detail(request, stok_id):
	p = Pembelian.objects.filter(stocks__id=stok_id)
	if len(p) != 0:
		return HttpResponseRedirect(reverse('pembelian_detail',args=[p[0].id]))

	k = Konversi.objects.filter(outs__id=stok_id)
	if len(k) != 0:
		return HttpResponseRedirect(reverse('konversi_detail', args=[k[0].id]))

	return HttpResponseRedirect(reverse('home'))