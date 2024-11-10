from flask import Flask, request, jsonify
import smtplib
from dotenv import load_dotenv
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permette le richieste dal frontend
load_dotenv() #Carica nel progetto tutte le variabili salvate nel file .env

#ELGA CONSULTING s.r.l.
@app.route('/send-email', methods=['POST'])
def send_email():
    EMAIL_ADDRESS = "elisanardi@elgaconsulting.it"
    EMAIL_PASSWORD = "Pizzabuona1!"
    SMTP_SERVER = "smtps.aruba.it"
    SMTP_PORT = 465  # Usa la porta 587 per TLS (STARTTLS)

    data = request.json  # Ricevi i dati in formato JSON
    name = data.get('name')
    surname = data.get('surname')
    email = data.get('email')
    number = data.get('number')
    company_role =  data.get('company_role')
    message = data.get('message')

    # Creazione dell'email
    subject = f"NUOVO MESSAGGIO dal FORM"
    body = f"Nome: {name} {surname}\nRuolo Aziendale: {company_role}\nCellulare: {number}\nEmail: {email}\nMessaggio: {message}"

    # Configurazione del server SMTP
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS  # Può essere il tuo indirizzo o quello del destinatario
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Invia l'email usando SMTP
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            # server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())
        return jsonify({"message": "Email inviata con successo!"}), 200
    except Exception as e:
        print(f"Errore nell'invio dell'email: {e}")
        return jsonify({"error": "Errore durante l'invio dell'email"}), 500
    

#NAZEDA KASHTA FORM 
@app.route('/send-email-nazedaKashta', methods=['POST'])
def send_email_Nazeda_Kashta():
    EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS_NAZEDA_KASHTA')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD_NAZEDA_KASHTA')

    data = request.json  # Ricevi i dati in formato JSON
    name = data.get('name')
    surname = data.get('surname')
    email = data.get('email')
    number = data.get('number')
    message = data.get('message')
    office_selected = data.get('office_selected')
    visit_type = data.get('visit_type')

    # Creazione dell'email
    subject = f"NUOVO MESSAGGIO di VISITA"
    body = f"""<html>
                <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            font-size: 14px;
                            color: #333;
                            line-height: 1.5;
                        }}
                        h2 {{
                            color: #AE803E;
                        }}
                        .section {{
                            margin-bottom: 20px;
                        }}
                        .section strong {{
                            font-weight: bold;
                        }}
                    </style>
                </head>
                <body>
                    <h2>Nuovo messaggio dal form di contatto</h2>
                    
                    <div class="section">
                        <strong>Nome:</strong> {name} <br>
                        <strong>Cognome:</strong> {surname} <br>
                        <strong>Email:</strong> {email} <br>
                        <strong>Numero di telefono:</strong> {number} <br>
                    </div>
                    
                    <div class="section">
                        <strong>Tipo di visita:</strong> {visit_type} <br>
                        <strong>Ufficio selezionato:</strong> {office_selected} <br>
                    </div>
                    
                    <div class="section">
                        <strong>Messaggio:</strong> <br>
                        <p>{message}</p>
                    </div>
                    
                    <p><strong>Nota:</strong> Questo messaggio è stato inviato automaticamente dal form di contatto.</p>
                </body>
                </html>
                """

    # Configurazione del server SMTP
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = EMAIL_ADDRESS  # Può essere il tuo indirizzo o quello del destinatario
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    try:
        # Invia l'email usando SMTP
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())
        return jsonify({"message": "Email inviata con successo!"}), 200
    except Exception as e:
        print(f"Errore nell'invio dell'email: {e}")
        return jsonify({"error": "Errore durante l'invio dell'email"}), 500

if __name__ == '__main__':
    app.run(debug=True)

