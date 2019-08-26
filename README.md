# datorklubben-booking

Bokningsystem för datorklubben på Tullinge gymnasium. Grunden kodades under 2018, mindre uppdateringar/förbättringar sedan dess.

Kodat i Python 2.7 och modulen Flask. Se filen `requirements.txt` för alla "dependencies".

Produktionssida fins på [booking.vilhelmprytz.se](https://booking.vilhelmprytz.se).

# Kom igång

1. Installera python 2 moduler med hjälp av pip2. `pip install -r requirements.txt` (i en virtualenv förslagsvis?)
2. Uppdatera konfigurationsvariabler i `config.json` respektive `mysql.json` för att passa setup (använd `development` för att testa utan databas och med begränsad funktionalitet).
3. Förslag i produktion: Använd gunicorn och supervisor för att köra applikationen (agerar som backend) med nginx som frontend (proxy_pass).

## Filstruktur

* `__init__.py` - initera MySQL tables
* `app.py` - huvudfil, där applikationen initieras och Flask endpoints ligger
* `db.py` - funktioner för kommunicering med MySQL
* `swish_qr_generator.py` - funktioner för att generera QR koder (Swish QR)
* `version.py` - variablen byts ut när jag deployar mot min webbserver till Git commit hash

* `mark_booking_as_paid.py` - skript för att markera bokning som betald, endast kommandorad
* `remove_tables.py` - skript för att radera alla tables i MySQL, används när jag debuggar

* `config.json` - JSON fil för generell konfiguration
* `mysql.json` - JSON fil för MySQL-uppgifter