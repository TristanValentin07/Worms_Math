import sys
import pygame

def load_map(file_path):
    blocks = []
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()

                if not line:
                    continue

                material, width, height, x, y = line.split(",")
                width, height, x, y = int(width), int(height), int(x), int(y)

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
