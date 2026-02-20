from PIL import Image

def clean_ghost_shadow(img_path):
    img = Image.open(img_path).convert("RGBA")
    width, height = img.size
    pixels = img.load()
    
    # We remove the grey shadow that was left around the ghost from the drop shadow of the drawing
    for x in range(width):
        for y in range(height):
            if pixels[x, y][3] > 0:
                r, g, b, a = pixels[x, y]
                # If it's a very light grey pixel, mostly transparent (shadow edge)
                if r > 210 and g > 210 and b > 210:
                    pixels[x, y] = (255, 255, 255, 0)

    img.save(img_path, "PNG")

clean_ghost_shadow("assets/ghost_isolated.png")
print("Cleaned ghost shadow!")
