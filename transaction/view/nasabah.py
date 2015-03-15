
from views_routine import *

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def index(request):
	context = { 'nasabah': q_nasabah("individu"), 'user': request.user}
	return render(request, 'transaction/nasabah.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def index_kolektif(request):
	context = { 'nasabah': q_nasabah("kolektif"), 'user': request.user}
	return render(request, 'transaction/nasabah_kolektif.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def detail(request, nasabah_id):
	context = {'detail': q_nasabah_detail(nasabah_id), 'user': request.user}
	return render(request, 'transaction/nasabah_detail.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def add(request):
	if request.method == 'POST':
		form = NasabahForm(request.POST, request.FILES)
		if form.is_valid():
			print "Valid"
			form.save()
			return HttpResponseRedirect(reverse('nasabah'))
	else:
		form = NasabahForm()

	context = {'form':form, 'user': request.user}
	return render(request, 'transaction/nasabah_add.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def edit(request, nasabah_id):
	nn = Nasabah.objects.filter(id=nasabah_id)
	if len(nn) < 1:
		return HttpResponseRedirect(reverse('nasabah'))

	if request.method == 'POST':
		form = NasabahForm(request.POST, request.FILES, instance=nn[0])
		if form.is_valid():
			print "Valid"
			form.save()
			return HttpResponseRedirect(reverse('nasabah'))
	else:
		form = NasabahForm(instance=nn[0])

	context = {'form':form, 'id': nasabah_id, 'user': request.user}
	return render(request, 'transaction/nasabah_edit.html', context)