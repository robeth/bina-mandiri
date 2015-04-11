from views_routine import *

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def index(request):
	pembelian_entries = paginate_data(
		Pembelian.objects.all().order_by('-tanggal'),
		request.GET.get('page'),
		100)
		
	context = { 'pembelian': pembelian_entries, 'user': request.user, 
		"pages": customize_pages(pembelian_entries.number, pembelian_entries.paginator.num_pages)}
	return render(request, 'transaction/pembelian.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def add(request):
	if request.method == 'POST':
		form = PembelianForm(request.POST)
		if form.is_valid():
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
		options.append({'kode' : k.kode, 'nama': k.nama, 'id': k.id, 'stabil': str(k.stabil), 'satuan': k.satuan})

	context = {'form': form, 'options' : options, 'user': request.user}
	return render(request, 'transaction/pembelian_add.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
@transaction.atomic
def edit(request, pembelian_id):
	error_messages = []
	if request.method == 'POST':
		form = PembelianForm(request.POST)
		is_valid_form = True
		is_pembelian_clear = True
			#code.interact(local=dict(globals(), **locals()))
			
		if not form.is_valid():
			is_valid_form = False
			error_messages.append("Invalid form submission")

		if not q_is_pembelian_clear(pembelian_id):
			is_pembelian_clear = False
			error_messages.append("Some data still depend on this pembelian")

		if is_valid_form and is_pembelian_clear:
			data = form.data

			# get existing pembelian
			try:
				with transaction.atomic():
					p = Pembelian.objects.get(id=pembelian_id)

					# update pembelian info. clear all stocks
					n = Nasabah.objects.get(id=data['nasabah'])
					p.nasabah = n
					p.nota = data['nota']
					p.tanggal = data['tanggal']
					# assuming all new stocks are 'new'
					p.stocks.all().delete()

					p.save()

					# add items
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

					p.save()
					#FIX ME: previous cash withdrawal won't be updated
					if 'cash' in data:
						p_cash = Penarikan(tanggal=data['tanggal'], nasabah=n, total=temp_total)
						if 'nota_cash' in data:
							p_cash.nota = data['nota_cash']
						p_cash.save()
			except:
				error_messages.append("Invalid database operation")
			else:
				return HttpResponseRedirect(reverse('pembelian'))
	
	form = PembelianForm()
	kk = Kategori.objects.all().order_by('kode')
	options = []

	for k in kk:
		options.append({'kode' : k.kode, 'nama': k.nama, 'id': k.id, 'stabil': str(k.stabil), 'satuan': k.satuan})

	context = {'form': form, 'options' : options, 'user': request.user, 'pembelian_id': pembelian_id, 'error_messages': error_messages}
	return render(request, 'transaction/pembelian_edit.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def delete(request, pembelian_id):
	p = None
	try:
		p = Pembelian.objects.get(id=pembelian_id)
	except Pembelian.DoesNotExist:
		message_error = "Pembelian: id="+str(pembelian_id)+" not exists"

	if p:
		valid = q_is_pembelian_clear(pembelian_id)
		if valid:
			p.stocks.all().delete()
			p.delete()

	return HttpResponseRedirect(reverse('pembelian'))

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def detail(request, pembelian_id):
	res = q_pembelian_detail(pembelian_id)
	res['general'] = Pembelian.objects.filter(id=pembelian_id)
	res['user'] = request.user
	res['can_delete'] = q_is_pembelian_clear(pembelian_id)
	return render(request, 'transaction/pembelian_detail.html', res)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def print_version(request, pembelian_id):
	res = q_pembelian_detail(pembelian_id)
	res['general'] = Pembelian.objects.filter(id=pembelian_id)
	res['user'] = request.user
	return render(request, 'transaction/pembelian_print.html', res)