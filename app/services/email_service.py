import requests
import json
from config import Config

def send_email(emails, subject, message, category="Price Change"):
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