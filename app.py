from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
import os
from auth import Authenticator
from adresse_book import AdressBook
from contact import Contact
from communicator import send_email, get_whatsapp_link
from database import CATEGORIES

app = Flask(__name__)
app.secret_key = 'super_secret_key_student_project'

auth = Authenticator()
book = AdressBook()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if auth.verify_credentials(username, password):
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash("Identifiants incorrects", "error")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    query      = request.args.get('search', '')
    categorie  = request.args.get('categorie', '')

    if query:
        contacts = book.search_contact(query)
    elif categorie:
        contacts = book.filter_by_category(categorie)
    else:
        book.load_contacts()
        contacts = book.contacts

    return render_template('index.html',
                           contacts=contacts,
                           search_query=query,
                           active_category=categorie,
                           categories=CATEGORIES)

@app.route('/add', methods=['POST'])
def add():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    nom        = request.form.get('nom',        '').strip()
    email      = request.form.get('email',      '').strip()
    numero     = request.form.get('numero',     '').strip()
    categorie  = request.form.get('categorie',  'Autre').strip()
    adresse    = request.form.get('adresse',    '').strip()
    fonction   = request.form.get('fonction',   '').strip()
    entreprise = request.form.get('entreprise', '').strip()

    try:
        new_contact = Contact(nom, email, numero,
                              categorie, adresse, fonction, entreprise)
        if book.add_contact(new_contact):
            flash("Contact ajouté avec succès", "success")
        else:
            flash("Ce contact (nom ou numéro) existe déjà", "error")
    except AssertionError as e:
        flash(str(e), "error")

    return redirect(url_for('index'))

@app.route('/delete/<nom>', methods=['POST'])
def delete(nom):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    if book.remove_contact(nom):
        flash("Contact supprimé avec succès", "success")
    else:
        flash("Contact introuvable", "error")
        
    return redirect(url_for('index'))

@app.route('/edit/<old_nom>', methods=['POST'])
def edit(old_nom):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    new_nom     = request.form.get('nom',        '').strip()
    new_email   = request.form.get('email',      '').strip()
    new_numero  = request.form.get('numero',     '').strip()
    categorie   = request.form.get('categorie',  'Autre').strip()
    adresse     = request.form.get('adresse',    '').strip()
    fonction    = request.form.get('fonction',   '').strip()
    entreprise  = request.form.get('entreprise', '').strip()

    try:
        new_contact = Contact(new_nom, new_email, new_numero,
                              categorie, adresse, fonction, entreprise)
        if book.update_contact(old_nom, new_contact):
            flash("Contact mis à jour avec succès", "success")
        else:
            flash("Erreur lors de la mise à jour (doublon possible)", "error")
    except AssertionError as e:
        flash(str(e), "error")

    return redirect(url_for('index'))

@app.route('/export')
def export():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    filename = "contacts.csv"
    if book.export_to_csv(filename):
        return send_file(filename, as_attachment=True)
    else:
        flash("Erreur lors de l'exportation", "error")
        return redirect(url_for('index'))

# ─────────────────────────────────────────────────────────────
# Partie 7 : Communication Email & WhatsApp
# ─────────────────────────────────────────────────────────────

@app.route('/communicate/<nom>')
def communicate(nom):
    """Page de communication (email + WhatsApp) pour un contact."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # Rechercher le contact en base
    contacts = book.search_contact(nom)
    if not contacts:
        flash(f"Contact '{nom}' introuvable.", "error")
        return redirect(url_for('index'))

    contact = contacts[0]

    # Générer le lien WhatsApp avec message de confirmation par défaut
    default_msg = (
        f"Bonjour {contact.nom}, nous confirmons votre rendez-vous médical. "
        "Merci de votre confiance."
    )
    wa_link = get_whatsapp_link(contact.num, default_msg)

    return render_template(
        'compose_email.html',
        contact=contact,
        wa_link=wa_link,
    )


@app.route('/send_email/<nom>', methods=['POST'])
def send_email_route(nom):
    """Envoie un email à un contact."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    to_email = request.form.get('to_email', '').strip()
    subject  = request.form.get('subject', '').strip()
    body     = request.form.get('body', '').strip()

    if not to_email or not subject or not body:
        flash("Veuillez remplir tous les champs avant d'envoyer.", "error")
        return redirect(url_for('communicate', nom=nom))

    result = send_email(to_email, subject, body)

    if result['success']:
        flash(f"✅ {result['message']}", "success")
    else:
        flash(f"❌ {result['message']}", "error")

    return redirect(url_for('communicate', nom=nom))


if __name__ == '__main__':
    app.run(debug=True)
