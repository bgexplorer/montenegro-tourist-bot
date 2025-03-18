import telebot  # Biblioteka za rad sa Telegram botom
import os  # Modul za rad sa sistemskim varijablama
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
        "Gde mogu da promenim novac u Podgorici?"
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
        "Novac možete promeniti u menjačnicama u tržnim centrima ili na aerodromu."
    ]
}
faq_df = pd.DataFrame(data)  # Konvertujemo podatke u Pandas DataFrame radi lakše pretrage

# Inicijalizacija Telegram bota
TOKEN = "OVDE_UNESI_SVOJ_TOKEN"  # Ovde unesi svoj API token iz BotFather-a
bot = telebot.TeleBot(TOKEN)  # Kreiramo bot instancu

# Funkcija za pretragu najboljeg odgovora koristeći sličnost pitanja
def find_best_answer(question):
    matches = get_close_matches(question, faq_df["Pitanje"], n=1, cutoff=0.5)  # Pronalaženje najbližeg pitanja u bazi
    if matches:
        answer = faq_df[faq_df["Pitanje"] == matches[0]]["Odgovor"].values[0]  # Vraćamo odgovarajući odgovor
        return answer
    else:
        return "Nažalost, nemam odgovor na to pitanje. Molim vas pokušajte sa drugačijim formulacijom."

# Funkcija za prikaz interaktivnog menija
@bot.message_handler(commands=['menu'])
def send_menu(message):
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("Top 5 plaža", callback_data="plaze")
    btn2 = InlineKeyboardButton("Top znamenitosti", callback_data="znamenitosti")
    btn3 = InlineKeyboardButton("Kontakt taksi", callback_data="taksi")
    btn4 = InlineKeyboardButton("Vremenska prognoza", callback_data="vreme")
    
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    
    bot.send_message(message.chat.id, "Izaberite opciju:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "plaze":
        bot.send_message(call.message.chat.id, "Najpoznatije plaže su: Jaz, Mogren, Bečići, Drobni Pijesak i Plavi Horizonti.")
    elif call.data == "znamenitosti":
        bot.send_message(call.message.chat.id, "Top znamenitosti: Ostrog, Kotor, Lovćen, Durmitor, Sveti Stefan.")
    elif call.data == "taksi":
        bot.send_message(call.message.chat.id, "Preporučeni taksiji: Red Taxi (Podgorica) +382 67 019 019, City Taxi (Budva) +382 33 19700.")
    elif call.data == "vreme":
        bot.send_message(call.message.chat.id, "Vremensku prognozu možete pogledati na https://meteo.co.me")

# Postavljanje handlera za primanje poruka od korisnika
@bot.message_handler(func=lambda message: True)
def respond_to_message(message):
    user_question = message.text  # Uzimamo korisničku poruku
    answer = find_best_answer(user_question)  # Pretražujemo najbolji odgovor
    bot.reply_to(message, answer)  # Šaljemo odgovor korisniku

# Pokretanje bota
print("Bot je pokrenut...")  # Štampamo poruku kada se bot pokrene
bot.polling()  # Pokrećemo kontinuirano osluškivanje poruka
