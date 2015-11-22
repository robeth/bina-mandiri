from views_routine import *
from django.db import transaction
from transaction.db import q_retrieve_pembelian_candidates
from transaction.models import DetailPenarikan

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
	nasabah_result = Nasabah.objects.filter(id=nasabah_id)
	if len(nasabah_result) < 1:
			return HttpResponseRedirect(reverse('penarikan'))
	nasabah = nasabah_result[0]

	if request.method == 'POST':
		form = PenarikanForm(request.POST)
		if form.is_valid():
			new_penarikan = form.save()

			penarikan_amount = new_penarikan.total
			pembelians = q_retrieve_pembelian_candidates(nasabah_id)

			for pembelian in pembelians:
				amount = min(penarikan_amount, pembelian.unsettled_value())
				detail_penarikan = DetailPenarikan(penarikan=new_penarikan, pembelian=pembelian, jumlah=amount)
				detail_penarikan.save()
				penarikan_amount -= amount
				if penarikan_amount <= 0:
					break

			return HttpResponseRedirect(reverse('nasabah_detail', kwargs= {'nasabah_id' :nasabah_id}))
	else:
		form = PenarikanForm()

	candidate_pembelians = q_retrieve_pembelian_candidates(nasabah_id)

	context = { 'form': form, 'nasabah': nasabah_result, 'user': request.user, 'nasabah_id': nasabah_id, 'candidate_pembelians': candidate_pembelians}
	return render(request, 'transaction/penarikan_add.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
@transaction.atomic()
def delete(request, penarikan_id):
	penarikan_result = Penarikan.objects.filter(id=penarikan_id)
	if len(penarikan_result) == 0:
		return HttpResponseRedirect(reverse('penarikan'))

	penarikan = penarikan_result[0]

	penarikan.detailpenarikan_set.all().delete()
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
