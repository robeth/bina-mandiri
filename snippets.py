anomaly = [penarikan for penarikan in Penarikan.objects.all() if penarikan.total != sum([dp.jumlah for dp in penarikan.detailpenarikan_set.all()]) ]
