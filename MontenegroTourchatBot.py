import telebot
import os
import pandas as pd
from difflib import get_close_matches

# Učitajmo bazu podataka sa pitanjima i odgovorima
data = {
    "Pitanje": [
        "Koja je valuta u Crnoj Gori?",
        "Kako da stignem iz Bara do Kotora?",
        "Koje su najbolje plaže u Budvi?",
        "Gde mogu iznajmiti automobil u Podgorici?",
        "Koji su najpoznatiji restorani u Kotoru?",
        "Kako da koristim gradski prevoz u Podgorici?",
        "Gde se nalaze nacionalni parkovi u Crnoj Gori?",
        "Da li je potrebna viza za ulazak u Crnu Goru?",
        "Koji su brojevi za hitne službe u Crnoj Gori?",
        "Gde mogu da pronađem informacije o vremenskoj prognozi?"
    ],
    "Odgovor": [
        "Zvanična valuta u Crnoj Gori je euro (EUR).",
        "Možete putovati autobusom sa glavne stanice u Baru ili koristiti rent-a-car opciju.",
        "Najpoznatije plaže u Budvi su Mogren, Jaz, Slovenska plaža i Bečići.",
        "U Podgorici možete iznajmiti automobil u agencijama kao što su Tara-Rent, Ideal Rent-a-Car i Rokšped Rent-a-Car.",
        "Preporučeni restorani u Kotoru su Galion, Konoba Scala Santa i Stari Mlini.",
        "Gradski prevoz u Podgorici funkcioniše putem autobuskih linija, a karte se mogu kupiti kod vozača.",
        "Najpoznatiji nacionalni parkovi su Durmitor, Biogradska Gora, Skadarsko jezero, Lovćen i Prokletije.",
        "Građani EU, SAD, Srbije i većine zemalja Balkana ne trebaju vizu za boravak do 90 dana.",
        "Brojevi hitnih službi u Crnoj Gori su: Policija - 122, Hitna pomoć - 124, Vatrogasci - 123.",
        "Vremensku prognozu možete pratiti na sajtu meteo.co.me ili putem aplikacija AccuWeather i Windy."
    ]
}
faq_df = pd.DataFrame(data)

# Inicijalizacija Telegram bota
TOKEN = "8159628381:AAEUWt59cKCPR_DUZ1AuesR5bGw7ndfLXOM"  # Ovde unesi svoj API token iz BotFather-a
bot = telebot.TeleBot(TOKEN)

# Funkcija za pretragu najboljeg odgovora
def find_best_answer(question):
    matches = get_close_matches(question, faq_df["Pitanje"], n=1, cutoff=0.5)
    if matches:
        answer = faq_df[faq_df["Pitanje"] == matches[0]]["Odgovor"].values[0]
        return answer
    else:
        return "Nažalost, nemam odgovor na to pitanje. Molim vas pokušajte sa drugačijim formulacijom."

# Postavljanje handlera za primanje poruka
@bot.message_handler(func=lambda message: True)
def respond_to_message(message):
    user_question = message.text
    answer = find_best_answer(user_question)
    bot.reply_to(message, answer)

# Pokretanje bota
print("Bot je pokrenut...")
bot.polling()
# Ova izmena je samo da Railway povuče novi kod
import threading
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Montenegro Tourist Bot is running!"

def run_server():
    app.run(host="0.0.0.0", port=10000)  # Pokreće dummy server na portu 10000

# Pokretanje Flask servera u posebnoj niti (thread)
server_thread = threading.Thread(target=run_server)
server_thread.start()
