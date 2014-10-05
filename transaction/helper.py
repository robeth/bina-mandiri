from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from transaction.models import Nasabah

def paginate_data(data, selected_page, n_entries):
	pager = Paginator(data, n_entries)

	try:
		page_entries = pager.page(selected_page)
	except PageNotAnInteger:
		page_entries = pager.page(1)
	except EmptyPage:
		page_entries = pager.page(pager.num_pages)

	return page_entries