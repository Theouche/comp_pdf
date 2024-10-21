
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
from style_css import add_css_style

def create_output_directory(base_directory):
    # Créer le dossier "rapport_comparaison" s'il n'existe pas
    output_dir = os.path.join(base_directory, "rapport_comparaison")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Créer un sous-dossier avec la date actuelle
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dated_output_dir = os.path.join(output_dir, date_str)
    os.makedirs(dated_output_dir)

    return dated_output_dir


def generate_report(report_content, output_directory):
    report_file = os.path.join(output_directory, "comparison_report.html")
    with open(report_file, 'w') as file:
        print("generation du rapport ....")
        file.write(f"<html><head><title>Rapport de comparaison PDF</title></head>")
        add_css_style(file)  # Ajoute du style CSS pour rendre le rapport plus esthétique
        file.write("<body>")
        file.write(report_content)
        file.write("</body></html>")
    print(f"Rapport généré : {report_file}")

def generate_report_header():
    date_str = datetime.now().strftime("%Y-%m-%d")
    return f"<h1>Comparaison du {date_str}</h1><hr/>"