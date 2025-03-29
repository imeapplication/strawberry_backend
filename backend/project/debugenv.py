#!/usr/bin/env python
"""
Script de débogage pour vérifier les paramètres Django.
Placez ce fichier dans le répertoire /app de votre container Docker.
"""
import os
import sys
import importlib

print("=== Débogage des paramètres Django ===")

# Vérifier le PYTHONPATH
print(f"PYTHONPATH: {sys.path}")

# Vérifier les variables d'environnement
print(f"DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE', 'NON DÉFINI')}")

# Essayer d'importer le module settings
settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', 'project.settings')
print(f"Tentative d'importation de {settings_module}...")

try:
    settings = importlib.import_module(settings_module)
    print(f"Module de paramètres importé avec succès: {settings}")
    print(f"ALLOWED_HOSTS: {getattr(settings, 'ALLOWED_HOSTS', 'NON DÉFINI')}")
    print(f"DEBUG: {getattr(settings, 'DEBUG', 'NON DÉFINI')}")
except Exception as e:
    print(f"Erreur lors de l'importation du module de paramètres: {e}")

# Vérifier la structure des répertoires
print("\nStructure des répertoires:")
for dirpath, dirnames, filenames in os.walk("/app"):
    print(f"{dirpath}/")
    for f in filenames:
        print(f"  - {f}")

print("\n=== Fin du débogage ===")
