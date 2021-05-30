
a={'destination_addresses': ['Calle Cantarerías, 8F, 44540 Albalate del Arzobispo, Teruel, Spain'], 'origin_addresses': ['Unnamed Road, 44556 Berge, Teruel, Spain'], 'rows': [{'elements': [{'distance': {'text': '42.5 km', 'value': 42491}, 'duration': {'text': '44 mins', 'value': 2646}, 'status': 'OK'}]}], 'status': 'OK'}

print(a['rows'][0]['elements'][0]['duration']['value'])
for i in a['rows']:
    print(i)