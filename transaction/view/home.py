from views_routine import *

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def index(request):
	context = { 'nasabah': q_nasabah, 'data': q_home(), 'user': request.user}
	return render(request, 'transaction/home.html', context)