from views_routine import *
from django.db import transaction

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
@transaction.atomic()
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
				p.penarikan = p_cash
				p.save()

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
	pembelian = []
	try:
		with transaction.atomic():
			pembelian = Pembelian.objects.get(id=pembelian_id)
	except:
		return HttpResponseRedirect(reverse('pembelian'))

	if request.method == 'POST':
		form = PembelianForm(request.POST)
		is_valid_form = True
		is_pembelian_clear = True
			
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
					p = pembelian

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
			except:
				error_messages.append("Invalid database operation")
			else:
				# Successful edit operation
				return HttpResponseRedirect(reverse('pembelian_detail', kwargs={'pembelian_id': pembelian_id}))
	
	# GET response or invalid POST edit pembelian operation	
	form = PembelianForm(instance=pembelian)
	pembelian = Pembelian.objects.get(id=pembelian_id)
	kk = Kategori.objects.all().order_by('kode')
	options = []

	for k in kk:
		options.append({'kode' : k.kode, 'nama': k.nama, 'id': k.id, 'stabil': str(k.stabil), 'satuan': k.satuan})
	

	pembelian_dict = {
		'id' : pembelian.id,
		'tanggal': str(pembelian.tanggal),
		'nota' : pembelian.nota,
		'stocks': [],
		'nasabah_id' : pembelian.nasabah.id
	}

	for stok in pembelian.stocks.all() :
		pembelian_dict['stocks'].append({
			'id' : stok.id,
			'tanggal' : str(stok.tanggal),
			'harga': float(stok.harga),
			'jumlah': float(stok.jumlah),
			'kategori_id': float(stok.kategori.id)
		})
	# code.interact(local=dict(globals(), **locals()))
	context = {'form': form, 'options' : options, 'user': request.user, 'pembelian': pembelian_dict, 'error_messages': error_messages}
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