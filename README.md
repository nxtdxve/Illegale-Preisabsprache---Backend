# Preisverlauf-Backend

## Beschreibung

Dies ist das Backend-Teil für die IDPA-Projektarbeit, das die Verwaltung der Datenbank, Benachrichtigungen und die API-Endpunkte für das Preisverlaufssystem bereitstellt. Dieses Backend dient als Schnittstelle für das Scraper-Modul und das Frontend, um Preisdaten abzufragen und Benachrichtigungen über Preisänderungen zu senden.

## Technologien

- Python 3.12
- Flask
- MongoDB
- Mailtrap
- Requests
- Flask-APScheduler

## Features

- REST API zur Abfrage von Preisdaten, Retailern, zum Empfang von Preisänderungen und zum Abonnieren von E-Mails.
- Versand von E-Mail-Benachrichtigungen bei Preisänderungen über Mailtrap.
- Wöchentliche Updates mit Flask-APScheduler.

## Installation

Klonen Sie das Repository und installieren Sie die benötigten Abhängigkeiten:

```bash
git clone https://github.com/nxtdxve/Illegale-Preisabsprache-Backend.git
cd Illegale-Preisabsprache-Backend
pip install -r requirements.txt
```

## Konfiguration

Stellen Sie sicher, dass Sie eine `.env` Datei im Wurzelverzeichnis Ihres Projekts haben, die die folgenden Umgebungsvariablen definiert:

```env
MONGO_URI="mongodb://localhost:27017/your-database-name"
SECRET_KEY="your-secret-key"
API_KEY="your-api-key-for-scraper-communication"
MAILTRAP_TOKEN="your-mailtrap-token"
```

## Verwendung

Um das Backend zu starten:

```bash
python run.py
```

## API-Dokumentation

Eine Postman-Collection mit allen Endpunkten und benötigten Parametern liegt im Repository unter `tests` bereit. Stellen Sie sicher, dass Sie den `API_KEY` in der Postman-Collection auf Ihren spezifischen API-Schlüssel anpassen.

Die Tests können direkt über die bereitgestellte Postman-Collection ausgeführt werden, indem Sie den `API_KEY` anpassen und auf Run Collection gehen.

## Deployment

Das Projekt wurde auf Heroku gehostet und dafür angepasst.

## Verwandte Projekte

- Frontend: [Illegale Preisabsprache Frontend](https://github.com/nxtdxve/Illegale-Preisabsprache-Frontend)
- Scraper: [Illegale Preisabsprache Scraper](https://github.com/nxtdxve/Illegale-Preisabsprache-Scraper)

## Autoren

- David Zettler
- Ava Reindl
