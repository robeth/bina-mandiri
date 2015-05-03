from views_routine import *
from django.db import transaction

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def index(request): 
	penjualan_entries = paginate_data(
		Penjualan.objects.all().order_by('-tanggal'),
		request.GET.get('page'),
		100)

	context = { 'penjualan': penjualan_entries, 'user': request.user,
		"pages": customize_pages(penjualan_entries.number, penjualan_entries.paginator.num_pages)}
	return render(request, 'transaction/penjualan.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
@transaction.atomic()
def add(request):
	if request.method == 'POST':
		form = PenjualanForm(request.POST)
		if form.is_valid():
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
@transaction.atomic()
def edit(request, penjualan_id):
	error_messages = []
	penjualan = None

	try:
		penjualan = Penjualan.objects.get(id=penjualan_id)
	except:
		return HttpResponseRedirect(reverse('penjualan'))

	if request.method == 'POST':
		form = PenjualanForm(request.POST)
		if form.is_valid():
			try:
				with transaction.atomic():
					data = form.data
					cleaned_data = form.cleaned_data

					v = Vendor.objects.get(id=data['vendor'])
					p = penjualan
					p.tanggal= cleaned_data['tanggal'] 
					p.vendor = v 
					p.nota = cleaned_data['nota']
					p.detailpenjualan_set.all().delete()

					p.save()

					limit = int(data['total'])
					i = 1
					while i <= limit:

						# Validate each stock
						
						stocks = q_get_last_stock(data['stok'+str(i)], data['jumlah'+str(i)])
						for s in stocks:
							st = Stok.objects.get(id=s['id'])
							dp = DetailPenjualan(stok=st, penjualan=p, jumlah=s['jumlah'], harga=data['harga'+str(i)])
							dp.save()
						i += 1
			except Exception, e:
				error_messages.append("Invalid database operation:" + str(e))
			else:
				# Successful edit operation
				return HttpResponseRedirect(reverse('penjualan_detail', kwargs={'penjualan_id': penjualan_id}))

		else:
			error_messages.append("Invalid form submission")
	else:
		# Get Response or invalid edit operation
		form = PenjualanForm(instance=penjualan)

	penjualan_data = {
		'id' : penjualan.id,
		'tanggal': str(penjualan.tanggal),
		'nota': penjualan.nota,
		'detailPenjualanList': [],
		'vendor_id': penjualan.vendor.id
	}

	for detailPenjualan in penjualan.detailpenjualan_set.all():
		penjualan_data['detailPenjualanList'].append({
				'kode': detailPenjualan.stok.kategori.kode,
				'kategori_id' : detailPenjualan.stok.kategori.id,
				'stok_id' : detailPenjualan.stok.id,
				'jumlah' : float(detailPenjualan.jumlah),
				'harga' : float(detailPenjualan.harga)
			})

	context = { 
		'remaining':  q_remaining(), 
		'form':form, 
		'user': request.user, 
		'penjualan': penjualan_data,
		'error_messages': error_messages
	 }
	return render(request, 'transaction/penjualan_edit.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def delete(request, penjualan_id):
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
def detail(request, penjualan_id):
	res = q_penjualan_detail(penjualan_id)
	res['general'] = Penjualan.objects.filter(id=penjualan_id)
	res['user'] = request.user
	return render(request, 'transaction/penjualan_detail.html', res)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def print_version(request, penjualan_id):
	res = q_penjualan_detail(penjualan_id)
	res['general'] = Penjualan.objects.filter(id=penjualan_id)
	res['user'] = request.user
	return render(request, 'transaction/penjualan_print.html', res)