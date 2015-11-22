
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
			new_nasabah = form.save()
			next_page_alias = 'nasabah' if new_nasabah.jenis == 'individu' else 'nasabah_kolektif'
			return HttpResponseRedirect(reverse(next_page_alias))
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
			form.save()
			return HttpResponseRedirect(reverse('nasabah_detail', kwargs={'nasabah_id': nasabah_id}))
	else:
		form = NasabahForm(instance=nn[0])

	context = {'form':form, 'id': nasabah_id, 'user': request.user}
	return render(request, 'transaction/nasabah_edit.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def delete(request):
	if request.method == 'POST' and 'nasabah_id' in request.POST and is_integer(request.POST['nasabah_id']):

		nasabah_id = request.POST['nasabah_id']
		nasabah_result = Nasabah.objects.filter(id=nasabah_id)
		if len(nasabah_result) > 0:
			nasabah = nasabah_result[0]
			if nasabah.is_safe_to_be_deleted():
				nasabah.delete()

	return HttpResponseRedirect(reverse('nasabah'))


def is_integer(text):
	try:
		int(text)
		return True
	except ValueError:
		return False
