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

def add_css_style(file):
    """Ajoute le style CSS au fichier HTML."""
    file.write("""
    <style>
    body {
        font-family: Arial, sans-serif;
        margin: 20px;
        background-color: #f4f4f9;
    }
    h1 {
        color: #c00000; /* Rouge sombre pour Assystem */
        text-align: center;
        font-size: 2em;
    }
    h2 {
        color: #333;
        border-bottom: 2px solid #333;
        padding-bottom: 10px;
        text-align: left;
    }
    .comparison-section {
        background-color: #f9f9f9;
        padding: 10px;
        border: 1px solid #ccc;
        margin-bottom: 20px;
    }
    .diff-added {
        color: green;
        font-weight: bold;
    }
    .diff-removed {
        color: red;
        font-weight: bold;
    }
    hr {
        border: 2px solid #000;
        margin: 20px 0;
    }
    </style>
    """)