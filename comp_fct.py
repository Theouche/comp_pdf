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


def compare_images(img1, img2):
    img1 = np.array(img1)
    img2 = np.array(img2)
    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(gray1, gray2)
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    return diff, thresh

def compare_texts(text1, text2):
    diff = difflib.unified_diff(text1.splitlines(), text2.splitlines(), lineterm='', fromfile='old', tofile='new')
    diff_list = list(diff)

    if not diff_list:
        return None

    html_diff = ['<div class="comparison-section"><pre>']
    for line in diff_list:
        if line.startswith('-'):
            # Rouge pour les lignes disparues (anciennes)
            html_diff.append(f"<span class='diff-removed'>{line}</span>")
        elif line.startswith('+'):
            # Vert pour les nouvelles lignes
            html_diff.append(f"<span class='diff-added'>{line}</span>")
        else:
            html_diff.append(line)
    html_diff.append('</pre></div>')
    return '\n'.join(html_diff)

def extract_images_from_pdf(reader):
    images = convert_from_path(reader.stream.name)
    return images

def extract_pdf_content(reader):
    text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()

    # Extraction des images peut être faite à partir du chemin si nécessaire
    images = convert_from_path(reader.stream.name)  # Utilisation du chemin pour les images
    
    return text, images