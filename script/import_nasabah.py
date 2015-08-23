# HOW TO EXEC:
# 1. python manage.py shell
# 2. execfile('script/import_nasabah.py')
import csv
from transaction.models import Nasabah

nasabah_dict = {}

with open('script/nasabah.csv', 'r') as csvfile:
  nasabah_reader = csv.reader(csvfile, delimiter=',')
  for row in nasabah_reader:
    temp_no_induk = None if row[1].strip() == '' else row[1]
    nasabah_dict[row[0]] = {
        'no_induk': temp_no_induk,
        'nama': row[2],
        'alamat': row[3],
        'telepon': row[4],
        'nama_pj':row[5]
    }

result = {'success': [], 'fail': []}

for nasabah_id, nasabah_data in nasabah_dict.items():
  query_id = '-1'
  try:
      query_id = int(nasabah_id)
  except ValueError:
      pass

  query_result = Nasabah.objects.filter(id=query_id)
  if len(query_result) > 0 :
    current_nasabah = query_result[0]
    current_nasabah.nama = nasabah_data['nama']
    current_nasabah.no_induk = nasabah_data['no_induk']
    current_nasabah.alamat = nasabah_data['alamat']
    current_nasabah.telepon = nasabah_data['telepon']
    current_nasabah.nama_pj = nasabah_data['nama_pj']

    current_nasabah.save()
    result['success'].append(nasabah_id)
  else:
    result['fail'].append(nasabah_id)

print "Success: %d data" % (len(result['success']))

print "Fail/NOT FOUND: %d data" % (len(result['fail']))
for fail_id in result['fail']:
    print 'N' + str(fail_id)
