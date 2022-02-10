import json
from pydantic import BaseModel


class ApartmentItem(BaseModel):
    title: str
    address: str
    size: str
    rooms: str
    price: str


degewo_apartments = []
ebay_apartments = []
immonent_apartments = []
immowelt_apartments = []


def analyse(self, *args, spider_name: str):
    global degewo_apartments, ebay_apartments, immonent_apartments, immowelt_apartments
    with open(f'{spider_name}.json', 'r', encoding='utf-8') as apartments_json:
        apartments = json.load(apartments_json)
        if spider_name == 'degewo':
            degewo_apartments = analyse_apartments(degewo_apartments, apartments)
            return
        if spider_name == 'ebay':
            ebay_apartments = analyse_apartments(ebay_apartments, apartments)
            return
        if spider_name == 'immonent':
            immonent_apartments = analyse_apartments(immonent_apartments, apartments)
            return
        if spider_name == 'immowelt':
            immowelt_apartments = analyse_apartments(immowelt_apartments, apartments)
            return
    return


def analyse_apartments(apartments, new_apartments_dict):
    new_apartments = []
    for new_apartment in new_apartments_dict:
        new_apartment_item = ApartmentItem(
            title=new_apartment['Titel'],
            address=new_apartment['Adresse'],
            size=new_apartment['Größe'],
            rooms=new_apartment['Zimmer'],
            price=new_apartment['Preis'],
            link=new_apartment['Link']
        )
        new_apartments.append(new_apartment_item)

    if len(apartments) == 0:
        apartments = new_apartments
        return apartments
    else:
        for new_apartment in new_apartments:
            for apartment in apartments:
                if new_apartment.title == apartment.title:
                    break
                # TODO: Function to call Bot
        return new_apartments
