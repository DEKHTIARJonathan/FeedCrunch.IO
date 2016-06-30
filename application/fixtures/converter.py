# -*- coding: utf-8 -*-
import csv
import json
from datetime import datetime

csvfile = open('dataradar.csv', 'r')
jsonfile = open('dataradar.json', 'w')

fieldnames = ("id","title","link","date", "clicks", "activated")

reader = csv.DictReader( csvfile, fieldnames, delimiter=';')
headers = reader.next()

data = []
for row in reader:

	tmp = {}
	tmp['model'] = "feedcrunch.post"
	tmp['pk'] = int(row["id"])

	tmp_fields = {}
	tmp_fields["title"] = row["title"]
	tmp_fields["link"] = row["link"]

	tmp_date = datetime.strptime(row["date"], '%m/%d/%y %H:%M')
	tmp_date = tmp_date.strftime('%Y-%m-%dT%H:%M:00.000Z')

	tmp_fields["when"] = tmp_date
	tmp_fields["clicks"] = int(row["clicks"])


	if row["activated"] == "1":
		tmp_fields["activeLink"] = True
	else:
		tmp_fields["activeLink"] = False

	tmp_fields["user"] = "dataradar"

	tmp['fields'] = tmp_fields

	data.append(tmp)

str = json.dumps(data, indent=4, sort_keys=True)
jsonfile.write(str)

"""
{
   "model": "feedcrunch.post",
   "pk": 1,
   "fields": {
	  "title": "This is a link to google",
	  "link": "https://www.google.com",
	  "when": "2016-06-28T17:00:37.160Z",
	  "clicks": 0,
	  "activeLink": true,
	  "user":
   }
}


{
	"activated": "1",
	"clicks": "187",
	"date": "5/14/14 14:10",
	"id": "1",
	"link": "http://onepager.togaware.com/",
	"title": "One Page R: A Survival Guide to Data Science with R"
},

"""
