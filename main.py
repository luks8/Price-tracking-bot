import os
import telegram
import time
import requests
import schedule
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler
from selenium import webdriver

# Inserisci il token del tuo bot qui
TOKEN = "INSERT_YOUR_BOT_TOKEN_HERE"


CATEGORY_URL = 'https://www.unieuro.it/online/Piccoli-e-Grandi-Elettrodomestici/Grandi-Elettrodomestici/Lavatrici?p=1&dFR[categories.lvl3][0]=C7101&_gl=1*1tjtb87*_up*MQ..&gclid=CjwKCAjwrpOiBhBVEiwA_473dBRjXRQNGWxrK0fmdqDBv96Xe2DRp_R73wBDNM6J61KNnyHZcCL-zBoC4oIQAvD_BwE&gclsrc=aw.ds'


# Percentuale minima di riduzione del prezzo per inviare il messaggio
MIN_PERCENTAGE_DECREASE = 50

ARROW_DOWN = "\U00002B07"
SOLDI = "\U0001F4B0"
DITO_DESTRA = "👉🏻"

global products_data, last_price


#group_id dove vengono mandati i messaggi
group_id = INSERT_YOUR_CHAT_ID_HERE


bot = telegram.Bot(token=TOKEN)


# Funzione per gestire il comando /start del bot
def start(update, context):
    context.bot.send_message(chat_id=group_id, text="Ciao! Sono un sul monitoraggio dei prezzi. Inviami il comando /check per verificare il prezzo del prodotto.")


# Funzione per l'estrazione dei dati dalla pagina di Unieuro
def get_products_data(url):
    driver = webdriver.Chrome() # o il browser che preferisci
    driver.get(url)
    time.sleep(5) # attendiamo 5 secondi per il caricamento completo della pagina
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit() # chiudiamo il browser
    products = soup.find_all('article', class_='product-tile')
    data = []
    for product in products:
        name_elem = product.find('div', class_='product-tile__title')
        if not name_elem:
            continue
        name = name_elem.find('a', class_='gtmListing')
        if not name:
            continue
        name = name.text.strip()
        original_price_elem = product.find('a', class_='prices__original-price')
        if not original_price_elem:
            continue
        original_price = original_price_elem.text.strip().replace('€\xa0', '').replace(',', '.')
        original_price = float(''.join(filter(str.isdigit, original_price))) / 100
        discounted_price_elem = product.find('a', class_='prices__price')
        if discounted_price_elem:
            discounted_price = discounted_price_elem.text.strip().replace('€\xa0', '').replace(',', '.')
            discounted_price = float(''.join(filter(str.isdigit, discounted_price))) / 100
            percentage_decrease = round((1 - (discounted_price / original_price)) * 100)
            link_elem = product.find('a', class_='gtmListing')
            if link_elem:
                link = 'https://www.unieuro.it' + link_elem['href']
            else:
                link = ''
            data.append({'name': name, 'original_price': original_price, 'discounted_price': discounted_price, 'percentage_decrease': percentage_decrease, 'link': link})
    return data


# Salva gli ultimi prezzi noti degli articoli
last_price = {}

def check_price():
    products_data = get_products_data(CATEGORY_URL)
    for product in products_data:
        name = product['name']
        original_price = product['original_price']
        discounted_price = product['discounted_price']
        percentage_decrease = product['percentage_decrease']
        link = product['link']
        
        if name in last_price:
            if discounted_price < last_price[name]:
                decrease = round((1 - (discounted_price / last_price[name])) * 100)
                if decrease >= MIN_PERCENTAGE_DECREASE:
                    message = f"Ottime notizie! Il prezzo di: \n\n{DITO_DESTRA} <b>{name}</b>\n\nè diminuito del <b>{ARROW_DOWN} {percentage_decrease}%</b>!\n\nPrezzo originale: <b>€{original_price:.2f}</b>\nPrezzo scontato: <b>€{product['discounted_price']:.2f}</b> {SOLDI}\n\nEcco il link dell'articolo:\n\n{link} "
                    bot.send_message(chat_id=group_id, text=message)
        last_price[name] = discounted_price
    print("last_price: ", last_price)


schedule.every(5).seconds.do(check_price)


# Funzione per avviare il bot e programmare l'esecuzione della funzione di check ogni 5 secondi
def run():
    # Crea un'istanza dell'Updater del bot Telegram utilizzando il token del bot
    updater = Updater(TOKEN)

    # Aggiungi un gestore per il comando /start
    updater.dispatcher.add_handler(CommandHandler("start", start))

    # Aggiungi un gestore per il comando /check
    updater.dispatcher.add_handler(CommandHandler("check", check_price))

    # Avvia il bot
    updater.start_polling()

    print("Bot avviato!")

    # Programma l'esecuzione della funzione di check ogni 5 secondi
    schedule.every(5).seconds.do(check_price)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    run()
