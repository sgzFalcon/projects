import os, requests, bs4
urlFile = open('url.txt')
url = urlFile.read().rstrip('\n')
contentType = input('Serie o película: ')
title = input('Introduce el nombre: ')
titleC = title.capitalize()

res = requests.get(url + 'secciones.php?sec=buscador&valor='+title.replace(' ', '+'))
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, 'html.parser')
linkElems = soup.select('tr[height="22"] a')
#Filter results
firstFilter = []
secondFilter = []
results = []

if contentType in ['serie', 'Serie']:
    season = input('Número de la temporada: ')
    quality = input('Calidad (720p o en blanco): ')
    for i in range(len(linkElems)):
        if ((titleC or title) and 'Temporada') in linkElems[i].getText():
            firstFilter += [linkElems[i]]
    for i in range(len(firstFilter)):
        if season in firstFilter[i].getText():
            secondFilter += [firstFilter[i]]
    for i in range(len(secondFilter)):
        if quality in secondFilter[i].getText():
            results += [secondFilter[i]]
else:
    for i in range(len(linkElems)):
        if (titleC or title) in linkElems[i].getText():
            results += [linkElems[i]]

#Priting results
for i in range(len(results)):
    print(i+1,'. ',results[i].getText(),sep='')

#Selecting files to download
if len(results) > 1:
    selection = int(input('Indica el número del elemento deseado'))
elif len(results) == 1:
    selection = 1
else:
    raise Exception('No se encontraron resultados')
pageElem = requests.get(url + results[selection -1].get('href'))
pageElem.raise_for_status()
