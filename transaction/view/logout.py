from views_routine import *

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
	logout(request)
	return HttpResponseRedirect(reverse('django.contrib.auth.views.login'))