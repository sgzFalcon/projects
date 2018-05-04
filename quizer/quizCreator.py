import json
import os

mode = input('Do you want to create or modify a quiz? ')
workingfile = input('Introduce name of file (i.e. "test"): ')

if mode.lower() == 'create':
    while os.path.isfile('data/'+workingfile+'.json'):
        print('File already exists.')
        workingfile = input('Introduce a new name: ')

    jsonFile = 'data/'+workingfile+'.json'
    with open(jsonFile,'w') as dFile:
        json.dump({},dFile)
        print(workingfile+'.json ','has been created.')

else:
    jsonFile = 'data/'+workingfile+'.json'

    if not os.path.isfile('data/'+workingfile+'.json'):
        print('File doesn\'t exist. A new file will be created.')
        with open(jsonFile, 'w') as dFile:
            json.dump({},dFile)

with open(jsonFile) as dFile:
    data = json.load(dFile)
    print('\t',workingfile+'.json','loaded succesfully.')

categories =[]
for v in data.values():
    categories += [v[1]]


while True:
    question = input('Introduce your question: ')
    answer = input('Introduce the correct answer: ')
    category = input('Introduce the type of the answer {}: '.format(set(categories)))
    data[question]=[answer,category,0,0]

    for v in data.values():
        categories += [v[1]]

    add = input('Add another question? ')
    if add.lower() == 'no':
        break

with open(jsonFile,'w') as dFile:
    json.dump(data,dFile)