def load_map(file_path):
    blocks = []
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                # Split line into components
                parts = line.split(",")
                if len(parts) != 5:
                    print(f"Error: Malformed line: {line}")
                    continue
                material, width, height, x, y = parts
                # Mark "dirt.jpeg" blocks as indestructible
                destructible = "dirt.jpeg" not in material
                blocks.append({
                    "material": material,
                    "width": int(width),
                    "height": int(height),
                    "x": int(x),
                    "y": int(y),
                    "destructible": destructible  # Add destructible flag
                })
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except ValueError as e:
        print(f"Error: {e}")
    return blocks