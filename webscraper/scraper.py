import os, requests, bs4, webbrowser, sys
urlFile = open('url.txt')
url = urlFile.read().rstrip('\n')
title = input('Introduce el nombre de la serie: ')
titleC = title.capitalize()

print('Buscando...')

res = requests.get(url + 'secciones.php?sec=buscador&valor='+title.replace(' ', '+'))
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, 'html.parser')
linkElems = soup.select('tr[height="22"] a')
#Filter results
firstFilter = []
secondFilter = []
results = []

season = input('Número de la temporada: ')
quality = input('Calidad (720p o en blanco): ')
for i in range(len(linkElems)):
    if ((titleC or title) and 'Temporada') in linkElems[i].getText():
        firstFilter += [linkElems[i]]
for i in range(len(firstFilter)):
    if season+'ª' in firstFilter[i].getText():
        secondFilter += [firstFilter[i]]
for i in range(len(secondFilter)):
    if quality in secondFilter[i].getText():
        results += [secondFilter[i]]

#Priting results
for i in range(len(results)):
    print(i+1,'. ',results[i].getText(),sep='')

#Selecting files to download
if len(results) > 1:
    selection = int(input('Indica el número del elemento deseado: '))
elif len(results) == 1:
    selection = 1
else:
    raise Exception('No se encontraron resultados')

print('Descargando...')

pageElem = requests.get(url + results[selection -1].get('href'))
pageElem.raise_for_status()
soup2 = bs4.BeautifulSoup(pageElem.text, 'html.parser')
episodeElems = soup2.select('td[bgcolor="#C8DAC8"] a')

def download(url, episodeElems, attempt):
    attempt += 1
    if attempt == 3:
        print('Inténtalo de nuevo más tarde')
        sys.exit()
    for index, i in enumerate(range(len(episodeElems))):
        finalPage = requests.get(url + episodeElems[i].get('href'))
        if finalPage.status_code != 200:
            print('Error', finalPage.status_code)
            print('Probando de nuevo...')
            download(url, episodeElems, attempt)
        soup3 = bs4.BeautifulSoup(finalPage.text, 'html.parser')
        downloadLink = soup3.select('table[width="440"] a[style="font-size:12px;"]')
        downPage = requests.get(url + downloadLink[0].get('href'))
        if downPage.status_code != 200:
            print('Error', downPage.status_code)
            print('Probando de nuevo...')
            download(url, episodeElems, attempt)
        soup4 = bs4.BeautifulSoup(downPage.text, 'html.parser')
        hereLink = soup4.select('table[width="550"] a')
        herePage = requests.get(url + hereLink[0].get('href'))
        if herePage.status_code != 200:
            print('Error', herePage.status_code)
            print('Probando de nuevo...')
            download(url, episodeElems, attempt)
        #Save path
        downloadFile = open(os.path.join('D:','Descargas',
            os.path.basename(hereLink[0].get('href'))),'wb')
        for block in herePage.iter_content(100000):
            downloadFile.write(block)
        print(((index+1)*100)//len(episodeElems),'%',end="\r", flush=True)
    print('Descarga completada')

attempt = 0
download(url, episodeElems, attempt)
