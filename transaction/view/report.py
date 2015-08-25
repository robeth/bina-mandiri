from views_routine import *

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
def utang_nasabah(request):
	pembelian_entries = paginate_data(
		Pembelian.objects.filter(
			penarikan_id__isnull=True).order_by('-tanggal'),
			request.GET.get('page',1),
			100)
	context = { 'pembelian': pembelian_entries, 'user': request.user,
		"pages": customize_pages(pembelian_entries.number, pembelian_entries.paginator.num_pages)}
	return render(request, 'transaction/utang_nasabah.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def tonase_nasabah(request):
	from datetime import date
	today = date.today()
	month = request.GET.get('month', today.month)
	year = request.GET.get('year', today.year)

	pembelian_list = Pembelian.objects.filter(tanggal__year=year, tanggal__month=month)

	res = {}

	for pembelian in pembelian_list:
		pembelian_json = {
					'id': pembelian.id,
					'tanggal': pembelian.tanggal,
					'total_value': pembelian.total_value(),
					'total_unit' : pembelian.total_unit()
				}
		if pembelian.nasabah.id in res:
			res[pembelian.nasabah.id]['pembelian_list'].append(pembelian_json)
			res[pembelian.nasabah.id]['total_value'] += pembelian_json['total_value']
			res[pembelian.nasabah.id]['total_unit'] += pembelian_json['total_unit']
		else:
			res[pembelian.nasabah.id] = {
				'nama' : pembelian.nasabah.nama,
				'nama_pj' : pembelian.nasabah.nama_pj,
				'no_induk' : pembelian.nasabah.no_induk,
				'alamat' : pembelian.nasabah.alamat,
				'telepon' : pembelian.nasabah.telepon,
				'pembelian_list' : [ pembelian_json ],
				'total_value' : pembelian_json['total_value'],
				'total_unit' : pembelian_json['total_unit'],
				'summary' : {}
			}

		for stock in pembelian.stocks.all():
			report_kategori = stock.kategori.report_kategori
			if report_kategori in res[pembelian.nasabah.id]['summary']:
				res[pembelian.nasabah.id]['summary'][report_kategori]['jumlah'] += stock.jumlah
			else:
				res[pembelian.nasabah.id]['summary'][report_kategori] = {
					'jumlah' : stock.jumlah,
					'satuan' : report_kategori.satuan
				}

	context = { 'report': res, 'user': request.user, 'bulan': int(month), 'tahun': int(year), 'year_range': range(2013, today.year + 1)}
	return render(request, 'transaction/tonase_nasabah.html', context)

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
