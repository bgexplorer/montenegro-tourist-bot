import telebot  # Biblioteka za rad sa Telegram botom
import os  # Modul za rad sa sistemskim varijablima
import pandas as pd  # Biblioteka za rad sa tabelarnim podacima
from difflib import get_close_matches  # Funkcija za pronalaženje sličnih reči
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton  # Biblioteka za inline dugmiće

# Učitajmo bazu podataka sa pitanjima i odgovorima u obliku rečnika
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
        "Gde mogu da pronađem informacije o vremenskoj prognozi?",
        "Koliko košta taxi u Crnoj Gori?",
        "Koje su najbolje znamenitosti u Crnoj Gori?",
        "Kako da putujem između gradova u Crnoj Gori?",
        "Koji su najpoznatiji nacionalni parkovi?",
        "Gde mogu da promenim novac u Podgorici?",
        "Koje su najbolje plaže u Baru?",
        "Koji su najbolji restorani u Baru?",
        "Šta obići u Baru?",
        "Kako funkcioniše gradski prevoz u Baru?"
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
        "Vremensku prognozu možete pratiti na sajtu meteo.co.me ili putem aplikacija AccuWeather i Windy.",
        "Start taksimetra u većini gradova je oko 1€, dok je cena po kilometru od 0.50€ do 1€.",
        "Najpoznatije znamenitosti su: Ostrog, Lovćen, Durmitor, Stari grad Kotor i Sveti Stefan.",
        "Možete koristiti autobuse, taksije ili rent-a-car uslugu za putovanje između gradova.",
        "Nacionalni parkovi u Crnoj Gori su: Durmitor, Biogradska gora, Skadarsko jezero, Lovćen i Prokletije.",
        "Novac možete promeniti u menjačnicama u tržnim centrima ili na aerodromu.",
        "Najpoznatije plaže u Baru su: Veliki Pijesak, Crvena Plaža, Sutomore, Maljevik i Utjeha.",
        "Najbolji restorani u Baru su: Restoran Kalamper, Knjaževa Bašta, Le Petit Bistro i Konoba Spilja.",
        "U Baru možete posetiti Stari grad Bar, tvrđavu Haj Nehaj, Skadarsko jezero i maslinjake Stare Masline.",
        "Gradski prevoz u Baru se sastoji uglavnom od lokalnih autobusa koji povezuju Sutomore, Utjehu i centar grada. Takođe su dostupni i taksiji po pristupačnim cenama."
    ]
}
faq_df = pd.DataFrame(data)  # Konvertujemo podatke u Pandas DataFrame radi lakše pretrage

# Inicijalizacija Telegram bota
TOKEN = os.getenv("TELEGRAM_API_TOKEN")  # Povlačimo API token iz okruženja
bot = telebot.TeleBot(TOKEN)  # Kreiramo bot instancu

# Funkcija za pretragu najboljeg odgovora koristeći sličnost pitanja
def find_best_answer(question):
    matches = get_close_matches(question, faq_df["Pitanje"], n=1, cutoff=0.5)  # Pronalaženje najbližeg pitanja u bazi
    if matches:
        answer = faq_df[faq_df["Pitanje"] == matches[0]]["Odgovor"].values[0]  # Vraćamo odgovarajući odgovor
        return answer
    else:
        return "Nažalost, nemam odgovor na to pitanje. Molim vas pokušajte sa drugačijim formulacijom."

# Postavljanje handlera za primanje poruka od korisnika
@bot.message_handler(func=lambda message: True)
def respond_to_message(message):
    user_question = message.text  # Uzimamo korisničku poruku
    answer = find_best_answer(user_question)  # Pretražujemo najbolji odgovor
    bot.reply_to(message, answer)  # Šaljemo odgovor korisniku

# Pokretanje bota
print("Bot je pokrenut...")  # Štampamo poruku kada se bot pokrene
bot.polling()  # Pokrećemo kontinuirano osluškivanje poruka

# Dummy server da Render zna da je aplikacija aktivna
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Montenegro Tourist Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

# Pokreni Flask server u posebnoj niti PRE nego što startuješ bota
flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

# Pokretanje bota
print("Bot je pokrenut...")  # Štampamo poruku kada se bot pokrene
bot.polling()  # Pokrećemo kontinuirano osluškivanje poruka

