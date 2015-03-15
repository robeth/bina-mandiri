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
def stok_detail(request, stok_id):
	p = Pembelian.objects.filter(stocks__id=stok_id)
	if len(p) != 0:
		return HttpResponseRedirect(reverse('pembelian_detail',args=[p[0].id]))

	k = Konversi.objects.filter(outs__id=stok_id)
	if len(k) != 0:
		return HttpResponseRedirect(reverse('konversi_detail', args=[k[0].id]))

	return HttpResponseRedirect(reverse('home'))