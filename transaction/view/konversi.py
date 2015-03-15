from views_routine import *

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def index(request):
	konversi_entries = paginate_data(
		Konversi.objects.all().order_by('-tanggal'),
		request.GET.get('page'),
		100)

	context = { 'konversi': konversi_entries, 'user': request.user,
		"pages": customize_pages(konversi_entries.number, konversi_entries.paginator.num_pages)}
	return render(request, 'transaction/konversi.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def add(request):
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
def detail(request, konversi_id):
	res = q_konversi_detail(konversi_id)
	res['general'] = Konversi.objects.filter(id=konversi_id)
	res['user'] = request.user
	res['can_delete'] = q_is_konversi_clear(konversi_id)
	return render(request, 'transaction/konversi_detail.html', res)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def delete(request, konversi_id):
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