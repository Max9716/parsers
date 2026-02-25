import requests
from bs4 import BeautifulSoup
import json
import re
import xml.etree.ElementTree as ET
import datetime


def floor(x):
    url = f'https://domrfdevelopment.ru/projects/dom-na-vostoke/flats/{x}/'
    response = requests.get(url)
    response.encoding = 'utf-8'
    try:
        soup = BeautifulSoup(response.text, 'xml').find_all("div", class_="flat-info-tabs__picture")[0].find("img")["src"]
        return soup
    except:
        pass

def poisk(y):
    flat1 = {}
    flat1["flat_id"] = y["id"]
    flat1["number"] = y["object_number"]
    #flat1["numberE"] = y["attributes"]["position_on_floor"]
    flat1["complex"] = "1"
    flat1["complex_id"] = "Дом на Востоке"
    flat1["house"] = y["buildings"]
    flat1["house_id"] = y["buildings"]
    flat1["floor"] = y["floor"].split(" ")[0]
    #flat1["section"] = y["sectionName"]
    flat1["rooms"] = y["rooms"]
    flat1["type_room"] = y["rooms"]+y["subtype"]
    flat1["price"] = y["price"][:-1]
    flat1["price_base"] = y["price"][:-1]
    flat1["area"] = y["area"]
    # flat1["areaH"] = y["area_living"]
    # flat1["areaK"] = y["area_kitchen"]
    #flat1["status"] = y["status"]
    flat1["decor"] = y["decoration"]
    try:
        flat1["plan"] = "https://domrfdevelopment.ru"+y["img"]
    except:
        flat1["plan"] = ""
    # try:
    #     flat1["floor_plan"] = floor(y["id"])
    # except:
    #     flat1["floor_plan"] = ""
    return flat1

date = datetime.datetime.now()
date = str(date)[:19]
root = ET.Element('root', date=date)

flat2 = []
for i in range(0, 100):
    url = f'https://domrfdevelopment.ru/api/v1/interactive/objects/?page_num={i}&mode=showMore&rooms=&euroformat=&decoration=&floor_from=2&floor_to=17&cost_from=5.56&cost_to=21.94&area_from=25&area_to=112&windows=&setting_date=&sort_by=FINAL_PRICE&sort_direction=asc&buildings='
    response = requests.get(url)
    response.encoding = 'utf-8'
    try:
        soup = response.json()["data"]["items"]
        for a in soup:
            flat2.append(a)
    except:
        break
flat = [poisk(y) for y in flat2]

for l in flat:
    flatID = ET.SubElement(root, "Квартира", id=str(l["flat_id"]))
    nom = ET.SubElement(flatID, "Номер")
    #nomE = ET.SubElement(flatID, "НомерНаЭтаже")
    komp = ET.SubElement(flatID, "Комплекс")
    kompid = ET.SubElement(flatID, "КомплексID")
    korp = ET.SubElement(flatID, "Корпус")
    korpid = ET.SubElement(flatID, "КорпусID")
    etz = ET.SubElement(flatID, "Этаж")
    #sec = ET.SubElement(flatID, "Секция")
    room = ET.SubElement(flatID, "Комнат")
    type = ET.SubElement(flatID, "ТипПомещений")
    sale = ET.SubElement(flatID, "СтоимостьСоСкидкой")
    salebase = ET.SubElement(flatID, "СтоимостьБазовая")
    sq = ET.SubElement(flatID, "Площадь")
    # sqH = ET.SubElement(flatID, "ПлощадьЖил")
    # sqK = ET.SubElement(flatID, "ПлощадьКух")
    st = ET.SubElement(flatID, "Статус")
    # dec = ET.SubElement(flatID, "Отделка")
    Plan = ET.SubElement(flatID, "Планировка")
    #floor_plan = ET.SubElement(flatID, "Поэтажка")
    nom.text = str(l["number"])
    #nomE.text = str(l["numberE"])
    komp.text = str(l["complex"])
    kompid.text = str(l["complex_id"])
    korp.text = str(l["house"])
    korpid.text = str(l["house_id"])
    etz.text = str(l["floor"])
    #sec.text = str(l["section"])
    room.text = str(l["rooms"])
    type.text = str(l["type_room"])
    sale.text = str(l["price"])
    salebase.text = str(l["price_base"])
    sq.text = str(l["area"])
    # sqH.text = str(l["areaH"])
    # sqK.text = str(l["areaK"])
    #st.text = str(l["status"])
    # dec.text = str(l["decor"])
    Plan.text = str(l["plan"])
    #floor_plan.text = str(l["floor_plan"])
mydata = ET.tostring(root, encoding='utf-8')
with open("dom-na-vostoke.xml", "wb") as myfile:
    myfile.write(mydata)



