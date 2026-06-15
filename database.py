import sqlite3
import os

DB_FILE = "app.db"

# Catégories médicales disponibles
CATEGORIES = ["Patient", "Fournisseur", "Laboratoire", "Médecin", "Pharmacie", "Autre"]

def get_connection():
    """Retourne une connexion à la base de données SQLite."""
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """Crée les tables et migre les colonnes manquantes (Partie 8 et 9)."""
    conn = get_connection()
    cursor = conn.cursor()

    # Table contacts (structure de base)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            nom       TEXT NOT NULL,
            email     TEXT NOT NULL UNIQUE,
            num       TEXT NOT NULL UNIQUE
        )
    ''')

    # ── Partie 8 : migration douce des nouvelles colonnes ──────────────
    # On ajoute les colonnes uniquement si elles n'existent pas encore.
    existing = {row[1] for row in cursor.execute("PRAGMA table_info(contacts)")}
    new_columns = {
        "categorie":  "TEXT NOT NULL DEFAULT 'Autre'",
        "adresse":    "TEXT DEFAULT ''",
        "fonction":   "TEXT DEFAULT ''",
        "entreprise": "TEXT DEFAULT ''",
    }
    for col, definition in new_columns.items():
        if col not in existing:
            cursor.execute(f"ALTER TABLE contacts ADD COLUMN {col} {definition}")

    # Table admins
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            username      TEXT NOT NULL UNIQUE,
            salt          TEXT NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')

    # Table rendezvous (Partie 9)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rendezvous (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            contact_id INTEGER NOT NULL,
            date       TEXT NOT NULL,
            heure      TEXT NOT NULL,
            UNIQUE(date, heure),
            FOREIGN KEY (contact_id) REFERENCES contacts(id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()

# Initialiser la base de données lors de l'import de ce module
init_db()

