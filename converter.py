from __future__ import print_function
import sys
import json
import re



infile=open(sys.argv[1], 'r')
sourcefile=sys.argv[2]=open(sys.argv[2], 'r')
outfile=sys.argv[3]=open(sys.argv[3], 'w+')

lookup={"BAR":"Bard", "SOR":"Sorcerer", "DRU":"Druid","WIZ":"Wizard","RAN":"Ranger","CLE":"Cleric","PAL":"Paladin","WAR":"Warlock"}

classDict={}

while True:
	line=sourcefile.readline()
	if line=="":
		break
	line=line.strip()
	name=line.rsplit("(")[0]
	classes=line.rsplit("(")[1][:-1].rsplit(',')
	classDict[name]=[]
	for c in classes:
		classDict[name].append(lookup[c.strip()])
print(classDict)
print(lookup)

spelldata=json.load(infile)
pattern=re.compile(r'<.*?>')
for spell in spelldata:
	spell['classes']=classDict[spell['name']]
	if pattern.sub('', spell['level'])=='Cantrip':
		spell['level']=0
	else:
		spell['level']=int(pattern.sub('', spell['level']))
	pattern2=re.compile(r'^.*br/>')
	spell['spelltext']=pattern2.sub('', spell['spelltext'])

print(spelldata)
json.dump(spelldata, outfile)
