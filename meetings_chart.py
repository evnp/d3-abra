import csv
import glob
import json

attendees = {}
for fn in glob.glob("csvs/Mtg_*"):
  year = int(fn.split('_')[1])
  with open(fn, "rU") as f:
    for row in csv.reader(f):
      name = row[0].strip().lower() + '_' + row[1].strip().lower()
      yearly_attendees = attendees[year] if year in attendees else set()
      yearly_attendees.add(name)
      attendees[year] = yearly_attendees

data = [{'name': 'First Time', 'data': []}, {'name': 'Consecutive Attendence', 'data': []}, {'name': 'Skipped a Year', 'data': []}]
with open("meetings.json", "w+") as output:
  for year in attendees.keys():
    segments = [len(attendees[year]),
      len([a for a in attendees[year] if a in attendees[year-1]]) if year-1 in attendees else 0,
      len([a for a in attendees[year] if (a in attendees[year-2] and a not in attendees[year-1])]) if year-2 in attendees else 0]
    for seg, dat in zip(segments, data):
      dat['data'].append(seg)

  output.write(json.dumps({
    "meetings": data
  }, indent=2))

print 'Done!'
