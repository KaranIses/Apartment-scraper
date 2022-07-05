import configparser
import json
import os
from json import JSONDecodeError

import discord
from discord.ext import tasks
from pydantic import BaseModel

client = discord.Client()


class ApartmentItem(BaseModel):
    title: str
    address: str
    size: str
    rooms: str
    price: str
    link: str


degewo_apartments = []
ebay_apartments = []
immonet_apartments = []
immowelt_apartments = []
wbm_apartments = []


async def analyse(spider_name: str):
    global degewo_apartments, ebay_apartments, immonet_apartments, immowelt_apartments, wbm_apartments
    with open(f'{spider_name}.json', 'r', encoding='utf-8') as apartments_json:
        try:
            apartments = json.load(apartments_json)
            if spider_name == 'degewo':
                print(f'New analysis of Degewo: \n{degewo_apartments}')
                degewo_apartments = await analyse_apartments(degewo_apartments, apartments)
                return
            if spider_name == 'ebay':
                print(f'New analysis of Ebay: \n{ebay_apartments}')
                ebay_apartments = await analyse_apartments(ebay_apartments, apartments)
                return
            if spider_name == 'immonet':
                print(f'New analysis of Immonet: \n{immonet_apartments}')
                immonet_apartments = await analyse_apartments(immonet_apartments, apartments)
                return
            if spider_name == 'immowelt':
                print(f'New analysis of Immowelt: \n{immowelt_apartments}')
                immowelt_apartments = await analyse_apartments(immowelt_apartments, apartments)
                return
            if spider_name == 'wbm':
                print(f'New analysis of WBM: \n{wbm_apartments}')
                wbm_apartments = await analyse_apartments(wbm_apartments, apartments)
                return
        except JSONDecodeError:
            os.chdir("")
            pass
    return


async def analyse_apartments(apartments, new_apartments_dict):
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
        print('apartment list was empty. Returning filled list')
        print(new_apartments)
        return new_apartments
    else:
        apartment_found_flag = False
        for new_apartment in new_apartments:
            for apartment in apartments:
                if new_apartment.title == apartment.title:
                    print(f'{apartment.title} already found')
                    apartment_found_flag = True
                    break
            if not apartment_found_flag:
                print(f'{new_apartment.title} is a new apartment')
                await send_update(new_apartment)
        return new_apartments


@client.event
async def on_ready():
    print(f'Running as {client.user}!')


@tasks.loop(minutes=1)
async def get_apartments():
    print('now')
    await analyse('degewo')
    await analyse('ebay')
    await analyse('immonet')
    await analyse('immowelt')
    await analyse('wbm')


async def send_update(apartment: ApartmentItem):
    update_message = f'<@{user_id}> \nNeues Objekt gefunden:\n**{apartment.title}**\n**Ort:** ' \
                     f'{apartment.address}\n**Größe:** {apartment.size}m²\n**Zimmer:** {apartment.rooms}\n' \
                     f'**Preis:** {apartment.price}€\n{apartment.link}'
    channel = client.get_channel(id=int(channel_id))
    await channel.send(update_message)


bot_config = configparser.ConfigParser()
bot_config.read("discord_bot_api.ini")
api_key = bot_config.get('DISCORD_BOT', 'api_key')
channel_id = bot_config.get('DISCORD_BOT', 'channel_id')
user_id = bot_config.get('DISCORD_BOT', 'user_id')
os.chdir("..\\..\\..")
get_apartments.start()
client.run(api_key)
