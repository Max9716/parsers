import requests
from bs4 import BeautifulSoup
import json
import re
import xml.etree.ElementTree as ET
import datetime

def poisk(y):
    url = "https://vdomrf.ru"+y
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    flat1 = {}
    flat1["flat_id"] = y
    flat1["number"] = soup.find("h1", class_="item__h").text.split(" - ")[0]
    flat1["complex"] = "ВДомеЖить"
    flat1["complex_id"] = "1"
    flat1["house"] = "Проекты"
    flat1["house_id"] = "1"
    flat1["floor"] = soup.find_all("div", class_="projekt-feature-div")[2].text.split(":")[1].strip()
    flat1["rooms"] = ""
    flat1["type_room"] = "Строительство"
    flat1["price"] = soup.find("p", class_="item__price").text[:-1].replace(" ", "")
    flat1["area"] = soup.find_all("div", class_="projekt-feature-div")[0].text.split(":")[1].split(" ")[0]
    # flat1["status"] = y["status"]
    #flat1["plan"] = y["image"]
    return flat1

date = datetime.datetime.now()
date = str(date)[:19]
root = ET.Element('root', date=date)


flat2 = []

url = 'https://vdomrf.ru/stroitelstvo-domov/'
response = requests.get(url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'lxml').find_all("div", class_="news-item")
for a in soup:
    try:
        flat2.append(a.find("a")["href"])
    except:
        continue

flat = [poisk(y) for y in flat2]

for l in flat:
    flatID = ET.SubElement(root, "Квартира", id=str(l["flat_id"]))
    nom = ET.SubElement(flatID, "Номер")
    komp = ET.SubElement(flatID, "Комплекс")
    kompid = ET.SubElement(flatID, "КомплексID")
    korp = ET.SubElement(flatID, "Корпус")
    korpid = ET.SubElement(flatID, "КорпусID")
    etz = ET.SubElement(flatID, "Этаж")
    room = ET.SubElement(flatID, "Комнат")
    type = ET.SubElement(flatID, "ТипПомещений")
    sale = ET.SubElement(flatID, "СтоимостьСоСкидкой")
    sq = ET.SubElement(flatID, "Площадь")
    nom.text = str(l["number"])
    komp.text = str(l["complex"])
    kompid.text = str(l["complex_id"])
    korp.text = str(l["house"])
    korpid.text = str(l["house_id"])
    etz.text = str(l["floor"])
    room.text = str(l["rooms"])
    type.text = str(l["type_room"])
    sale.text = str(l["price"])
    sq.text = str(l["area"])
mydata = ET.tostring(root, encoding='utf-8')
with open("izhs.xml", "wb") as myfile:
    myfile.write(mydata)



