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
from db_fct import *
from comp_fct import *
from report_fct import *

# Comparer deux PDF : un dans pdf-backups et un dans pdf-copies
def compare_pdfs(pdf_path, backup_pdf_path, output_directory):
    pdf1_name = os.path.basename(pdf_path)
    pdf2_name = os.path.basename(backup_pdf_path)
    
    try:
        with open(pdf_path, 'rb') as f1, open(backup_pdf_path, 'rb') as f2:
            reader1 = PyPDF2.PdfReader(f1)
            reader2 = PyPDF2.PdfReader(f2)

            # Initialiser le contenu du rapport HTML
            report_content = f"<h2>Comparaison entre {pdf1_name} et {pdf2_name}</h2>\n"

            # Comparer le texte
            for page_num in range(min(len(reader1.pages), len(reader2.pages))):
                page1_text = reader1.pages[page_num].extract_text()
                page2_text = reader2.pages[page_num].extract_text()

                # Comparaison des textes des deux pages
                text_diff = compare_texts(page2_text, page1_text)
                if text_diff:
                    report_content += f"<h4>Différences textuelles détectées sur la page {page_num + 1} :</h4>\n"
                    report_content += f"<pre>{text_diff}</pre>\n"
                else:
                    report_content += f"<p>Aucune différence textuelle détectée sur la page {page_num + 1}.</p>\n"

            # Comparer les images
            current_images = extract_images_from_pdf(reader1)
            backup_images = extract_images_from_pdf(reader2)
            report_content += "<h3>Différences d'images :</h3>\n<ul>"
            for page_num in range(min(len(current_images), len(backup_images))):
                diff_image, threshold_image = compare_images(current_images[page_num], backup_images[page_num])
                if np.any(threshold_image):

                    # Créer un sous-répertoire pour les images de différences
                    image_output_directory = os.path.join(output_directory, f"images_diff_{os.path.splitext(pdf1_name)[0]}")
                    if not os.path.exists(image_output_directory):
                        os.makedirs(image_output_directory)

                    image_filename = f"diff_page_{page_num + 1}.png"
                    image_path = os.path.join(image_output_directory, image_filename)
                    cv2.imwrite(image_path, threshold_image)

                    relative_image_path = os.path.relpath(image_path, output_directory) 
                    report_content += f'<li>Différence détectée sur la page {page_num + 1}. <a href="{relative_image_path}">Voir l\'image de la différence</a></li>\n'
                else:
                    report_content += f"<li>Aucune différence d'image détectée sur la page {page_num + 1}.</li>\n"
            report_content += "</ul>"

            return report_content
    except Exception as e:
        return f"<p>Erreur lors de la comparaison entre {pdf1_name} et {pdf2_name} : {str(e)}</p>\n"


# Traiter chaque PDF localement
def process_local_pdfs(pdf_directory, backup_directory, conn):
    report_content = ""
    report_content = generate_report_header()
    output_dir = create_output_directory(pdf_directory)
    print("\n\n########## NEW COMPARISON ##########\n\n")
    for file in os.listdir(pdf_directory):  # Parcours uniquement les fichiers dans le répertoire
        if file.endswith('.pdf'):
            pdf_path = os.path.join(pdf_directory, file)
            pdf_hash = calculate_pdf_hash(pdf_path)

            pdf_author = get_pdf_author(pdf_path)

            # Vérifie si le fichier est déjà dans la base
            db_record = file_in_db(conn, pdf_path, pdf_hash)
            if db_record:
                file_id, saved_file_path = db_record
                backup_pdf_path = os.path.join(backup_directory, os.path.basename(saved_file_path))

                # Si une version sauvegardée existe, comparer avec la version actuelle
                if os.path.exists(backup_pdf_path):
                    print(f"Comparaison for : {file}")
                    report_content += compare_pdfs(pdf_path, backup_pdf_path, output_dir)
                    update_pdf_in_db(conn, file, pdf_hash)
                    save_pdf_backup(pdf_path, backup_directory)
    
                else:
                    print(f"Sauvegarde manquante, création pour : {file}")
                    save_pdf_backup(pdf_path, backup_directory)
            else:
                # Nouveau fichier PDF
                print(f"Nouveau PDF : {file}")
                add_pdf_to_db(conn, file, pdf_author, pdf_path, pdf_hash)
                save_pdf_backup(pdf_path, backup_directory)
                report_content += f"<p>Nouveau PDF détecté : {file}</p>\n"
            report_content += "<hr style='border: 2px solid #000; margin: 20px 0;' />"
    
    #Finaliser la creation du rapport
    print("\n\n########## END COMPARISON ##########\n\n")    
    generate_report(report_content, output_dir)

if __name__ == "__main__":
    conn = connect_db()
    create_table_if_not_exists(conn)
    process_local_pdfs("/app/data", "/app/pdf-backups", conn)
    conn.close()
