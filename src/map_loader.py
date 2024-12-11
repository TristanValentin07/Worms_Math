import sys
import pygame

def load_map(file_path):
    """
    Charge une carte à partir d'un fichier texte et retourne une liste de blocs.
    """
    blocks = []

    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                # Supprimer les espaces ou sauts de ligne
                line = line.strip()

                # Ignorer les lignes vides
                if not line:
                    continue

                # Découper les paramètres
                material, width, height, x, y = line.split(",")
                width, height, x, y = int(width), int(height), int(x), int(y)

                # Ajouter un dictionnaire représentant le bloc
                blocks.append({
                    "material": material,
                    "width": width,
                    "height": height,
                    "x": x,
                    "y": y
                })

    except FileNotFoundError:
        print(f"Erreur : le fichier {file_path} est introuvable.")
    except ValueError as e:
        print(f"Erreur de formatage dans le fichier : {e}")

    return blocks
