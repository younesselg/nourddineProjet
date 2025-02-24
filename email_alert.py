import smtplib
from email.mime.text import MIMEText

def send_email_alert(subject, message, recipient):
    sender_email = "votre_email@gmail.com"
    sender_password = "VOTRE_MOT_DE_PASSE"

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, msg.as_string())
        server.quit()
        print("✅ E-mail envoyé avec succès !")
    except Exception as e:
        print("❌ Erreur lors de l'envoi de l'e-mail :", e)

# Exemple d'utilisation
send_email_alert("🔥 Alerte Incendie !", "Un incendie a été détecté dans votre région !", "destinataire@example.com")
