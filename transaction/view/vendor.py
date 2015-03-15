from views_routine import *

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def index(request):
	context = { 'vendor': q_vendor, 'user': request.user}
	return render(request, 'transaction/vendor.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def add(request):
	if request.method == 'POST':
		form = VendorForm(request.POST, request.FILES)
		if form.is_valid():
			print "Valid"
			form.save()
			return HttpResponseRedirect(reverse('vendor'))
	else:
		form = VendorForm()
	context = { 'form': form, 'user': request.user}
	return render(request, 'transaction/vendor_add.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def edit(request, vendor_id):
	vv = Vendor.objects.filter(id=vendor_id)
	if len(vv) < 1:
		return HttpResponseRedirect(reverse('vendor'))

	if request.method == 'POST':
		form = VendorForm(request.POST, request.FILES, instance=vv[0])
		if form.is_valid():
			print "Valid"
			form.save()
			return HttpResponseRedirect(reverse('vendor'))
	else:
		form = VendorForm(instance=vv[0])
	context = { 'form': form, 'id': vendor_id, 'user': request.user}
	return render(request, 'transaction/vendor_edit.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def detail(request, vendor_id):
	res = q_vendor_detail(vendor_id)
	res['general'] = Vendor.objects.filter(id=vendor_id)
	context = {'detail': res, 'user': request.user}
	return render(request, 'transaction/vendor_detail.html', context)