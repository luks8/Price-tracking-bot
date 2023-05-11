# Price-tracking-bot

Descrizione tecnica

Il bot è progettato per monitorare i prezzi dei prodotti su un sito web e inviare notifiche quando viene rilevata una diminuzione significativa del prezzo. 



Funzionamento:

Il bot utilizza la libreria python-telegram-bot per interagire con l'API di Telegram.
Utilizza anche le librerie requests e beautifulsoup4 per effettuare scraping dei dati dalla pagina web del sito di e-commerce.
Fa uso di schedule per programmare l'esecuzione periodica della funzione di monitoraggio dei prezzi.
Il bot utilizza anche selenium per automatizzare un browser (Chrome nel codice di esempio) al fine di consentire il rendering JavaScript delle pagine web.
Per eseguire correttamente il bot, devi specificare il token del tuo bot Telegram, che puoi ottenere dal BotFather di Telegram, e il group_id del gruppo o della chat dove desideri inviare i messaggi.



Dipendenze

python-telegram-bot: pip install python-telegram-bot
requests: pip install requests
beautifulsoup4: pip install beautifulsoup4
schedule: pip install schedule
selenium: pip install selenium
webdriver (necessario per il browser specificato): devi scaricare il driver corrispondente al browser che desideri utilizzare e aggiungerlo al tuo ambiente di esecuzione. Nel codice di esempio, viene utilizzato il driver per Chrome.



Configurazione

Assicurati di avere installato Python 3 sul tuo sistema.
Clona o scarica il repository del bot dal tuo account GitHub.
Apri una finestra del terminale e spostati nella directory del progetto.
Installazione delle dipendenze

Esegui il seguente comando per installare le dipendenze richieste:
Copy code
pip install -r requirements.txt
Configurazione del token del bot

Apri il file del codice sorgente (bot.py) nel tuo editor di testo preferito.
Cerca la variabile TOKEN e sostituisci "INSERT_YOUR_BOT_TOKEN_HERE" con il token del tuo bot Telegram. Puoi ottenere il token del tuo bot dal BotFather di Telegram.
Trova la variabile group_id e sostituisci INSERT_YOUR_CHAT_ID_HERE con l'ID del gruppo o della chat dove desideri inviare i messaggi.
Configurazione dell'URL del sito web

Nel file del codice sorgente (bot.py), trova la costante CATEGORY_URL.
Sostituisci l'URL di esempio con l'URL effettivo della categoria del prodotto che desideri monitorare.
Avvio del bot

Nel terminale, esegui il seguente comando per avviare il bot:
Copy code
python bot.py
Il bot sarà ora attivo e pronto a rispondere ai comandi.
Utilizzo del bot

Aggiungi il tuo bot a un gruppo o avvia una chat con esso.
Invia il comando /start per iniziare l'interazione con il bot.
Utilizza il comando /check per avviare manualmente il monitoraggio dei prezzi e ricevere eventuali notifiche di diminuzione significativa del prezzo.
Assicurati di aver configurato correttamente il token del bot, l'ID del gruppo o della chat e l'URL del sito web prima di avviare il bot. Inoltre, tieni presente che il bot utilizzerà il browser specificato (nel codice di esempio è Chrome) per effettuare lo scraping dei dati dalla pagina web. Pertanto, è necessario che il browser sia correttamente configurato e installato nel sistema.

