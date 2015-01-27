from googleplaces import GooglePlaces
import csv
import time 

places = GooglePlaces("AIzaSyAbG5vBlnNli4gilP1CWWmgCYWy-oyWd8c")
marker_text = """
new google.maps.Marker({position: new google.maps.LatLng(%s, %s), map: map, title:"%s"});
"""
js = []
with open("csvs/2014_with_locations.csv", 'rU') as f:
  for row in csv.reader(f):
    print row
    name = row[1].strip() + ' ' + row[2].strip()
    loc = row[0] + ', ' + row[3]
    print loc
    res = places.text_search(query=loc) 
    if res:
      p = res.places[0]
      coor = p.geo_location
      print coor
      lname = p.name
      js.append(marker_text % (coor['lat'], coor['lng'], lname + ', ' + name))
    time.sleep(.5)

for t in js:
  print t
