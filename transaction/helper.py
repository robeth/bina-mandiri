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

def customize_pages(current, last_page):
  pages = []

  current_teens = int(current / 10)
  last_teens = int(last_page / 10)

  # Add previous teens
  for i in range(1, current_teens):
    pages.append(i * 10)

  # Add all element in current teens
  for i in range(10):
    next_page = current_teens * 10 + i
    if next_page <= last_page and next_page > 0:
      pages.append(next_page)

  # Add next teens
  for i in range(current_teens + 1, last_teens + 1):
    pages.append(i * 10)

  pages.append(last_page)

  return pages