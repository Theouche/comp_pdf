# Utiliser une image de base Python légère
FROM python:3.12-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Mettre à jour les dépôts et installer les dépendances système (y compris libGL)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    poppler-utils \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*  # Nettoyer le cache APT

# Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste des fichiers du projet dans le conteneur
COPY . .

# Définir la commande par défaut
CMD ["python", "main.py"]

