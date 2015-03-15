from views_routine import *

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
def add(request):
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