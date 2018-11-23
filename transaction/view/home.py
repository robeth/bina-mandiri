from views_routine import *

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def index(request):
	# context = { 'nasabah': q_nasabah, 'data': q_home(), 'user': request.user}

	res = {}
	res['pembelian_pertanggal'] = {}
	res['pembelian_day'] = {}
	res['pembelian_week'] = {}
	res['pembelian_month'] = {}
	res['penjualan_pertanggal'] = {}
	res['penjualan_day'] = {}
	res['penjualan_week'] = {}
	res['penjualan_month'] = {}
	res['stok_week'] = {}
	res['stok_month'] = {}
	res['stok_day'] = {}
	res['10_penjualan'] = {}
	res['10_konversi'] = {}
	res['10_pembelian'] = {}
	res['penarikan_pertanggal'] = {}
	res['10_penarikan'] = {}
	res['saldo'] = {}
	res['aset'] = {}
	res['aset_total'] = 0

	context = { 'nasabah': q_nasabah, 'data': res, 'user': request.user}
	return render(request, 'transaction/home.html', context)