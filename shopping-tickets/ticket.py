import pyocr
import pyocr.builders
import re
import datetime
from PIL import Image
import pandas

def getText(ticket):
    tools = pyocr.get_available_tools()
    tool = tools[0]

    print('Processing image...')

    text = tool.image_to_string(
        Image.open(ticket),
        lang='spa',
        builder=pyocr.builders.TextBuilder()
    )
    #Just for testing
    print('-------TICKET---------\n',text,'\n----------------------\n')

    return text

def getDate(text):
    reDate = re.compile(r'\d\d/\d\d/\d\d\d\d')
    matchs = reDate.findall(text)
    date = matchs[0]
    if not date:
        print('No date found')
        print('Try with other file')
        main()

    day = int(date[:2])
    month = int(date[3:5])
    year = int(date[-4:])

    return datetime.date(year,month,day)

def getItems(text):
    #reItem = re.compile(r'\d[ ]\w\D*\d\d*,\d*') Don't admit numbers in names
    #reItem = re.compile(r'[1][ ]\w*\s\d\d*,\d*') One word items
    reItem = re.compile(r'[1][ ][^,\n]*,\d\d')
    matchs = reItem.findall(text)
    if not matchs:
        print('No products found')
        print('Try with other file')
        main()

    return matchs

def extractNamePrice(items):
    shoppingList = {}
    rePrice = re.compile(r'\d\d*,\d\d')
    for item in items:
        num = rePrice.findall(item)[0]
        price = float(num.replace(',','.'))
        name = item.replace(' '+num,'').replace('1 ','')
        shoppingList[name]={'Price':price}

    return shoppingList


def getTotal(text):
    reTotal = re.compile(r'EUROS \d\d*,\d\d')
    match = reTotal.findall(text)[0]
    reNum = re.compile(r'\d\d*,\d\d')
    total = float(reNum.findall(match)[0].replace(',','.'))

    return total

class Ticket:
    def __init__(self, ocrText):
        self.ocrText = ocrText
        self.date = getDate(self.ocrText)
        self.shopList = extractNamePrice(getItems(self.ocrText))
        self.total = getTotal(self.ocrText)

def main():
    filePath = input('Introduce file: ')
    text = getText(filePath)
    ticket = Ticket(text)

main()

