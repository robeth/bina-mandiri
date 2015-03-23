from views_routine import *

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
def add(request):
	if request.method == 'POST':
		form = PenarikanForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('penarikan'))
	else:
		form = PenarikanForm()

	context = { 'form': form, 'nasabah':q_nasabah_all(), 'user': request.user}
	return render(request, 'transaction/penarikan_add.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def delete(request, penarikan_id):
	p = None
	try:
		p = Penarikan.objects.get(id=penarikan_id)
	except Penarikan.DoesNotExist:
		message_error = "Penarikan: id="+str(penarikan_id)+" not exists"

	if p:
		p.delete()

	return HttpResponseRedirect(reverse('penarikan'))