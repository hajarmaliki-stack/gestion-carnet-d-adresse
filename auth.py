import hashlib
import secrets
from database import get_connection

class Authenticator:
    def __init__(self):
        self._initialize_credentials()

    def _hash_password(self, password, salt):
        """Hash un mot de passe avec SHA-256 et un salt."""
        return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

    def _initialize_credentials(self):
        """Crée un compte admin par défaut si la table est vide."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM admins")
        if cursor.fetchone()[0] == 0:
            salt = secrets.token_hex(16)
            hashed_password = self._hash_password("admin", salt)
            
            cursor.execute(
                "INSERT INTO admins (username, salt, password_hash) VALUES (?, ?, ?)",
                ("admin", salt, hashed_password)
            )
            conn.commit()
            
        conn.close()

    def verify_credentials(self, username, password):
        """Vérifie si les identifiants sont corrects."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT salt, password_hash FROM admins WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return False
            
        salt, stored_hash = row
        return self._hash_password(password, salt) == stored_hash

    def change_password(self, new_password, username="admin"):
        """Permet de changer le mot de passe."""
        conn = get_connection()
        cursor = conn.cursor()
        
        salt = secrets.token_hex(16)
        hashed_password = self._hash_password(new_password, salt)
        
        cursor.execute(
            "UPDATE admins SET salt = ?, password_hash = ? WHERE username = ?",
            (salt, hashed_password, username)
        )
        conn.commit()
        conn.close()
