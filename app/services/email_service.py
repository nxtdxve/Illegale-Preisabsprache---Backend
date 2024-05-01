import requests
import json
from config import Config

def send_email(emails, subject, message, category="Price Change"):
    """
    Versendet eine E-Mail an eine Liste von E-Mail-Adressen.

    :param emails: Eine Liste von E-Mail-Adressen.
    :param subject: Der Betreff der E-Mail.
    :param message: Der Inhalt der E-Mail.
    :param category: Die Kategorie der E-Mail.
    """
    url = "https://bulk.api.mailtrap.io/api/send"
    headers = {
        "Authorization": f"Bearer {Config.MAILTRAP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "from": {"email": "idpa@zettler.dev", "name": "IDPA Price Tracker"},
        "to": [{"email": email} for email in emails],
        "subject": subject,
        "text": message,
        "category": category
    }
    
    # Stelle sicher, dass das Payload als JSON-String formatiert wird
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    # Debug-Ausgabe
    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

""" # Beispiel für den Funktionsaufruf
emails = ["davidzettler@zb1.ch", "ghostjidihd@gmail.com"]
subject = "Ihr aktueller Preisupdate"
message = "Hier ist Ihre Nachricht."
send_email(emails, subject, message) """