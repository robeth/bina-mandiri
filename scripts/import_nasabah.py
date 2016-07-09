import csv
from transaction.models import Nasabah
import pdb

def override_dict(dictionary, condition_function, new_value):
    result = {}
    for key, value in dictionary.iteritems():
        result[key] = new_value if condition_function(key, value) else value
    return result

def run():
    filename = 'data/nasabah.csv'
    nasabah_file = open(filename)
    reader = csv.DictReader(nasabah_file,
        fieldnames=['id', 'no_induk', 'nama', 'alamat', 'telepon', 'nama_pj'])
    nasabah = None
    counter = 1000

    def is_empty_string(key, value):
        return value == ''

    def is_address_empty(key, value):
        return key == 'alamat' and value is None

    for row in reader:
        try:
            print "Importing: " + row['id']
            data = override_dict(row, is_empty_string, None)
            data = override_dict(data, is_address_empty, '')
            data['jenis'] = 'kolektif'
            if not data['id'] or data['id'] == '?':
                data['id'] = str(counter)
                counter = counter + 1

            nasabah = Nasabah(**data)
            nasabah.save()
            print "Success: " + nasabah.id
        except Exception as exception:
            print "Exception: " + str(exception)
