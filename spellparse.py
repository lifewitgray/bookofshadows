from __future__ import print_function
import re
import sys
from sets import Set
import urllib2
from bs4 import BeautifulSoup 
import pprint
import json

sourcefile=sys.argv[1]=open(sys.argv[1], 'r')
outfile=sys.argv[2]=open(sys.argv[2], 'w+')

hrefList=[]

pattern=re.compile('^.*href.*')

while True:
	line=sourcefile.readline()
	if line=='':
		break
	line=line.strip()
	if pattern.match(line):
		hrefList.append(line)

spellLinkSet=Set([])

pattern=re.compile(r'(ht[^"]*)')

for line in hrefList:
	spellLinkSet.add(pattern.findall(line)[0])

spelldata=[]

h=0
for l in spellLinkSet:
	html = urllib2.urlopen(l).read()
	soup = BeautifulSoup(html, 'html.parser')

	a=soup.find_all("p")

	spell={}
	i=0
	spelltext=""
	for b in a[0:4]:
		p = re.compile(r'<.*?>')
		b.contents
		for d in b:
			text=d.encode('utf-8').strip()
			if i==0:
				pattern=re.compile(r'[^,(]*')
				spell["name"]=pattern.findall(text)[0].strip()
				pattern2=re.compile(r'.*\(Ritual\).*')
				spell['ritual']= 1 if pattern2.match(text) else 0
				print(spell["name"])
			elif i==1:
				spell["school"]=text
			elif i==3:
				spell["level"]=text
			elif i==7:
				spell["casting_time"]=text
			elif i==11:
				spell["range"]=text
			elif i==15:
				spell["components"]=text
			elif i==19:
				spell['duration']=text
			elif i>=20:
				spelltext+=text
			i+=1
	spell["spelltext"]=spelltext
	spell['classes']=''
	spelldata.append(spell)
	h+=1
	print(spell)
	print(h)

json.dump(spelldata, outfile)
