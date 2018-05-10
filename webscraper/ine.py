'''
Command line App to access data from the INE (Instituto Nacional de Estadística)

'''
import sys, os
import requests
import json

def getInput():
    command = input('> ').split()
    action = command[0]
    if action in help(1) and callable(globals()[action]):
        if len(command)>1:
            globals()[action](command[1])
        else:
            globals()[action]()
    else:
        print ('Function not found. For all functions available introduce help')

def help(arg=0):
    funs = {
        'data':'Downloads a data series in json format. Add detailed for an explicit version',
        'help':'Shows all functions available',
        'quit' :'Closes the program.'
    }
    if arg == 0:
        for k in funs.keys():
            print(k,'\t',funs[k])

    return funs.keys()

def quit():
    sys.exit()

def data(arg=0):
    
    code = getCode()
    if code[0] in ['0','1','2','3','4','5','6','7','8','9']:
        url = 'http://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/'
    else:
        url = 'http://servicios.ine.es/wstempus/js/ES/DATOS_SERIE/'
    n = input('Last n data: ')
    payload = {'nult':n}
    if arg == 'detailed':
        payload['det']='2'
    res = requests.get(url+code,params=payload)
    res.raise_for_status()
    saveData(res)

def saveData(res):
    outFile = input('Introduce a name to save the data: ')
    if not os.path.exists('data'):
        os.makedirs('data')

    while os.path.isfile('data/'+outFile+'.json'):
        print('File already exists.')
        outFile = input('Introduce a new name: ')

    jsonFile = 'data/'+outFile+'.json'
    with open(jsonFile,'wb') as dFile:
        for chunk in res.iter_content(100000):
            dFile.write(chunk)
        print('Data saved in',jsonFile)

def getCode():
    serie = input('Name of the series: ')
    codes = {
        'IPC':'IPC206449',
        'IPC Armonizado':'IPCA1886',
        'Indice Precios de Viviendas': 'IPV946',
        'Condiciones de Vida': 'ECV4740',
        'Presupuestos Familiares': 'EPF425625',
        'Tecnología en Hogares':'DCS38',
        'Indicadores Urbanos':'10849',
        'EPA':'EPA86',
        'Flujo EPA':'EFPA971',
        'Coste Laboral Trimestral':'ETCL13725',
        'Coste Laboral Armonizado':'ICLA733',
        'Indice Precios del Trabajo':'IPT184',
        'Coste Laboral Anual':'EACL4',
        'Estructura Salarial':'DCS18',
        'Movilidad Laboral':'EMLG138',
    }
    while serie not in codes.keys():
        print('Data series not found. Introduce help for the complete list.')
        serie = input('> ')
        if serie == 'help':
            for k in codes.keys():
                print(k)
            serie = input('> ')

    return codes[serie]

def main():
    
    while True:
        getInput()

if __name__ == '__main__':
    main()