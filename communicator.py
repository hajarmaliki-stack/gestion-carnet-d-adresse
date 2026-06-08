"""
communicator.py - Module de communication (Email & WhatsApp)
Partie 7 : Interaction avec les contacts depuis l'application médicale.
"""

import smtplib
import urllib.parse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv


# ─────────────────────────────────────────────
#  Configuration SMTP (Gmail)
#  Remplir avec vos vraies informations
# ─────────────────────────────────────────────
load_dotenv()

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.getenv("SMTP_USER")           # adresse Gmail
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")   # Votre mot de passe d'application Gmail
     


def send_email(to_address: str, subject: str, body: str,
               from_address: str = None) -> dict:
    """
    Envoie un email via SMTP (Gmail).

    Args:
        to_address  : Adresse email du destinataire
        subject     : Objet de l'email
        body        : Corps du message (texte ou HTML)
        from_address: Adresse expéditeur (utilise SMTP_USER par défaut)

    Returns:
        dict: {"success": bool, "message": str}
    """
    sender = from_address or SMTP_USER

    if not sender or not SMTP_PASSWORD:
        return {
            "success": False,
            "message": (
                "Configuration SMTP manquante. "
                "Veuillez renseigner SMTP_USER et SMTP_PASSWORD dans communicator.py."
            )
        }

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = to_address

        # Corps texte brut
        part_text = MIMEText(body, "plain", "utf-8")
        # Corps HTML (mise en forme soignée)
        html_body = f"""
        <html>
          <body style="font-family:Arial,sans-serif;color:#333;max-width:600px;margin:auto;">
            <div style="background:#1a73e8;padding:20px;border-radius:8px 8px 0 0;">
              <h2 style="color:#fff;margin:0;">📋 Carnet d'Adresses Médical</h2>
            </div>
            <div style="border:1px solid #e0e0e0;padding:24px;border-radius:0 0 8px 8px;">
              {body.replace(chr(10), '<br>')}
            </div>
            <p style="text-align:center;font-size:12px;color:#888;margin-top:12px;">
              Message envoyé automatiquement depuis l'application médicale.
            </p>
          </body>
        </html>
        """
        part_html = MIMEText(html_body, "html", "utf-8")

        msg.attach(part_text)
        msg.attach(part_html)

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(sender, SMTP_PASSWORD)
            server.sendmail(sender, to_address, msg.as_string())

        return {"success": True, "message": f"Email envoyé avec succès à {to_address}."}

    except smtplib.SMTPAuthenticationError:
        return {
            "success": False,
            "message": "Échec d'authentification SMTP. Vérifiez vos identifiants."
        }
    except smtplib.SMTPException as e:
        return {"success": False, "message": f"Erreur SMTP : {str(e)}"}
    except Exception as e:
        return {"success": False, "message": f"Erreur inattendue : {str(e)}"}


def get_whatsapp_link(phone_number: str, message: str) -> str:
    """
    Génère un lien WhatsApp Web pour envoyer un message à un numéro.

    Le numéro doit être au format international (ex: +212612345678).
    Si le numéro commence par 06/07 (format marocain), il est converti automatiquement.

    Args:
        phone_number : Numéro de téléphone du contact
        message      : Message pré-rempli

    Returns:
        str: URL WhatsApp Web avec le message encodé
    """
    # Normalisation du numéro vers le format international
    number = phone_number.strip().replace(" ", "").replace("-", "")

    # Format marocain : 06XXXXXXXX → +212 6XXXXXXXX
    if number.startswith("06") or number.startswith("07"):
        number = "+212" + number[1:]
    elif number.startswith("0"):
        number = "+212" + number[1:]
    elif not number.startswith("+"):
        number = "+" + number

    encoded_message = urllib.parse.quote(message)
    return f"https://wa.me/{number.replace('+', '')}?text={encoded_message}"


# ─────────────────────────────────────────────
#  Templates de messages médicaux prédéfinis
# ─────────────────────────────────────────────

MEDICAL_TEMPLATES = {
    "confirmation_rdv": {
        "label": "Confirmation de rendez-vous",
        "subject": "Confirmation de votre rendez-vous médical",
        "body": (
            "Madame/Monsieur {nom},\n\n"
            "Nous avons le plaisir de vous confirmer votre rendez-vous médical.\n\n"
            "📅 Date : {date}\n"
            "🕐 Heure : {heure}\n"
            "📍 Lieu : {lieu}\n\n"
            "Merci de vous présenter 10 minutes avant l'heure prévue.\n"
            "En cas d'empêchement, veuillez nous contacter dès que possible.\n\n"
            "Cordialement,\nL'équipe médicale"
        )
    },
    "rappel_rdv": {
        "label": "Rappel de rendez-vous",
        "subject": "Rappel : votre rendez-vous médical demain",
        "body": (
            "Madame/Monsieur {nom},\n\n"
            "Ceci est un rappel pour votre rendez-vous médical prévu demain.\n\n"
            "📅 Date : {date}\n"
            "🕐 Heure : {heure}\n\n"
            "N'oubliez pas d'apporter votre carnet de santé et vos ordonnances.\n\n"
            "Cordialement,\nL'équipe médicale"
        )
    },
    "demande_resultats": {
        "label": "Demande de résultats (laboratoire)",
        "subject": "Demande de résultats d'analyses",
        "body": (
            "Madame/Monsieur,\n\n"
            "Nous vous contactons au sujet des analyses effectuées par notre patient(e) "
            "{nom} le {date}.\n\n"
            "Pourriez-vous nous faire parvenir les résultats dans les meilleurs délais ?\n\n"
            "Merci de votre collaboration.\n\n"
            "Cordialement,\nDr. {medecin}\nService médical"
        )
    },
    "ordonnance": {
        "label": "Envoi d'ordonnance",
        "subject": "Votre ordonnance médicale",
        "body": (
            "Madame/Monsieur {nom},\n\n"
            "Veuillez trouver ci-joint votre ordonnance médicale.\n\n"
            "📝 Traitement prescrit : {traitement}\n"
            "⏳ Durée : {duree}\n\n"
            "En cas de questions, n'hésitez pas à nous contacter.\n\n"
            "Cordialement,\nDr. {medecin}"
        )
    },
    "personnalise": {
        "label": "Message personnalisé",
        "subject": "",
        "body": ""
    }
}
