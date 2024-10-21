import os
import shutil
import hashlib
import psycopg2
from datetime import datetime
import PyPDF2
import numpy as np
from pdf2image import convert_from_path
import sys
import difflib
import cv2


# Connexion à la base de données
def connect_db():
    conn = psycopg2.connect(
        dbname="pdf_db",
        user="pdf_user",
        password="pdf_password",
        host="postgres"
    )
    return conn

# Créer la table si elle n'existe pas
def create_table_if_not_exists(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS pdf_files (
                id SERIAL PRIMARY KEY,
                nom_fichier TEXT NOT NULL,
                auteur TEXT,
                date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                hash_contenu TEXT NOT NULL,
                chemin_fichier TEXT NOT NULL,
                dernier_scan TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()

def get_pdf_author(pdf_path):
    try:
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            metadata = reader.metadata
            if metadata and '/Author' in metadata:
                return metadata['/Author']
    except Exception as e:
        print(f"Erreur lors de l'extraction des métadonnées du fichier {pdf_path}: {e}")
    return "Auteur inconnu"

# Calculer le hash SHA-256 d'un fichier PDF
def calculate_pdf_hash(pdf_path):
    hash_sha256 = hashlib.sha256()
    with open(pdf_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

# Vérifier si un fichier est déjà dans la base
def file_in_db(conn, file_path, file_hash):
    with conn.cursor() as cur:
        cur.execute("SELECT id, chemin_fichier FROM pdf_files WHERE nom_fichier = %s OR hash_contenu = %s", (os.path.basename(file_path), file_hash))
        return cur.fetchone()

# Ajouter un nouveau PDF dans la base de données
def add_pdf_to_db(conn, nom_fichier, auteur, chemin_fichier, hash_contenu):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO pdf_files (nom_fichier, auteur, chemin_fichier, hash_contenu) VALUES (%s, %s, %s, %s)", (nom_fichier, auteur, chemin_fichier, hash_contenu))
        conn.commit()

# Mettre à jour les métadonnées si un fichier a changé
def update_pdf_in_db(conn, nom_fichier, hash_contenu):
    with conn.cursor() as cur:
        cur.execute("UPDATE pdf_files SET hash_contenu = %s, dernier_scan = %s WHERE nom_fichier = %s", (hash_contenu, datetime.now(), nom_fichier))
        conn.commit()

# Sauvegarder une copie du PDF
def save_pdf_backup(pdf_path, backup_directory):
    shutil.copy2(pdf_path, os.path.join(backup_directory, os.path.basename(pdf_path)))
