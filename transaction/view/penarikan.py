from views_routine import *
from django.db import transaction

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def index(request):
	penarikan_entries = paginate_data(
		Penarikan.objects.all().order_by('-tanggal'),
		request.GET.get('page'),
		100)
		
	context = { 'penarikan': penarikan_entries, 'user': request.user, 
		"pages": customize_pages(penarikan_entries.number, penarikan_entries.paginator.num_pages)}
	return render(request, 'transaction/penarikan.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
@transaction.atomic()
def add(request, nasabah_id):
	if request.method == 'POST':
		form = PenarikanForm(nasabah_id,request.POST)
		if form.is_valid():
			new_penarikan = form.save()
			pembelians = form.cleaned_data.get('pembelians')
			for pembelian in pembelians:
				pembelian.penarikan = new_penarikan
				pembelian.save()

			return HttpResponseRedirect(reverse('nasabah_detail', kwargs= {'nasabah_id' :nasabah_id}))
	else:
		form = PenarikanForm(nasabah_id)

	context = { 'form': form, 'nasabah':q_nasabah_all(), 'user': request.user, 'nasabah_id': nasabah_id}
	return render(request, 'transaction/penarikan_add.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
@transaction.atomic()
def delete(request, penarikan_id):
	penarikan_result = Penarikan.objects.filter(id=penarikan_id)
	if len(penarikan_result) == 0:
		return HttpResponseRedirect(reverse('penarikan'))

	penarikan = penarikan_result[0]
	pembelians = penarikan.pembelian_set.all()
	for pembelian in pembelians:
		pembelian.penarikan = None
		pembelian.save()
	penarikan.delete()

	return HttpResponseRedirect(reverse('nasabah_detail', kwargs={'nasabah_id':penarikan.nasabah.id}))

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def detail(request, penarikan_id):
	penarikan_result = Penarikan.objects.filter(id=penarikan_id)
	if(len(penarikan_result) == 0):
		return HttpResponseRedirect(reverse('penarikan'))

	context = { 'penarikan' : penarikan_result[0]}
	return render(request, 'transaction/penarikan_detail.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
@transaction.atomic()
def edit(request, penarikan_id):
	penarikan_result = Penarikan.objects.filter(id=penarikan_id)
	if(len(penarikan_result) == 0):
		return HttpResponseRedirect(reverse('penarikan'))
	penarikan = penarikan_result[0]

	if request.method == 'POST':
		form = PenarikanForm(penarikan.nasabah.id,request.POST, instance=penarikan)
		if form.is_valid():
			editted_penarikan = form.save()
			old_pembelians = editted_penarikan.pembelian_set.all()
			for pembelian in old_pembelians:
				pembelian.penarikan = None
				pembelian.save()

			pembelians = form.cleaned_data.get('pembelians')
			for pembelian in pembelians:
				pembelian.penarikan = editted_penarikan
				pembelian.save()

			return HttpResponseRedirect(reverse('penarikan_detail', kwargs= {'penarikan_id' :penarikan_id}))
	else:
		form = PenarikanForm(penarikan.nasabah.id, instance=penarikan)

	context = { 'form': form, 'user': request.user, 'penarikan': penarikan}
	return render(request, 'transaction/penarikan_edit.html', context)