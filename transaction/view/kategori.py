from views_routine import *

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def index(request):
	if request.method == 'POST':
		form = KategoriForm(request.POST, request.FILES)
		if form.is_valid():
			print "Valid"
			form.save()
			return HttpResponseRedirect(reverse('nasabah'))
	else:
		form = KategoriForm()
	kk = Kategori.objects.all()
	context = {'data': kk, 'form':form, 'user': request.user}
	return render(request, 'transaction/kategori.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def edit(request, kategori_id):
	kk = Kategori.objects.filter(id=kategori_id)
	if len(kk) < 1:
		return HttpResponseRedirect(reverse('kategori'))

	if request.method == 'POST':
		form = KategoriForm(request.POST, request.FILES, instance=kk[0])
		if form.is_valid():
			print "Valid"
			form.save()
			return HttpResponseRedirect(reverse('kategori'))
	else:
		form = KategoriForm(instance=kk[0])
	context = {'form':form, 'id': kategori_id, 'user': request.user}
	return render(request, 'transaction/kategori_edit.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def add(request):
	if request.method == 'POST':
		form = KategoriForm(request.POST, request.FILES)
		if form.is_valid():
			print "Valid"
			form.save()
			return HttpResponseRedirect(reverse('kategori'))
	else:
		form = KategoriForm()
	context = {'form':form, 'user': request.user}
	return render(request, 'transaction/kategori_add.html', context)