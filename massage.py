import csv
import glob
import json
import re

ID_KEY = 'idkey'
REAL_NAME_KEY = 'namekey'

group_id = 1
people = {}
groups = {}
for fn in glob.glob("csvs/WorkingGroup*"):
  group_name = label = re.sub("([A-Z])"," \g<0>",fn.split('_')[1].split('.')[0])
  print group_id
  with open(fn, 'rU') as group_file:
    groups[group_id] = group_name
    for row in csv.reader(group_file):
      name = row[1].strip() + ' ' + row[0].strip()
      name_key = name.lower()
      if name_key in people:
        people[name_key][ID_KEY] += group_id
      else:
        people[name_key] = {
          ID_KEY: group_id,
          REAL_NAME_KEY: name
        }
  group_id <<= 1

nodes = []
edges = []
people = people.values()
print people
for index, person in enumerate(people):
  nodes.append({
    "name": person[REAL_NAME_KEY],
    "group": person[ID_KEY]
  })
  for cindex, colleague in enumerate(people[index+1:]):
    shared_groups = colleague[ID_KEY] & person[ID_KEY]
    group_id = 1
    while shared_groups > 0:
      if shared_groups & group_id:
        edges.append({
          "source": index,
          "target": index + cindex + 1,
          "value": group_id
        })
        shared_groups -= group_id
      group_id <<= 1

with open("test.json", "w+") as output:
  output.write(json.dumps({
    "nodes" : nodes,
    "edges" : edges
  }))
  output.close()

