from PIL import Image

def remove_green_screen(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    width, height = img.size
    pixels = img.load()
    
    # We define background as neon green
    def is_green(color):
        r, g, b, _ = color
        # High green, relative low red/blue
        return g > 150 and r < 180 and b < 100

    # First pass: remove pure neon green
    for x in range(width):
        for y in range(height):
            if is_green(pixels[x, y]):
                pixels[x, y] = (0, 0, 0, 0) # fully transparent
            else:
                # ensure opaque if not green
                r, g, b, a = pixels[x, y]
                pixels[x, y] = (r, g, b, 255)
                
    # Second pass: clean up edges (spill correction)
    # If a pixel is somewhat green-tinted on the edge, neutralize it
    for x in range(1, width-1):
        for y in range(1, height-1):
            if pixels[x, y][3] > 0:
                r, g, b, a = pixels[x, y]
                if g > r and g > b and (pixels[x-1,y][3] == 0 or pixels[x+1,y][3] == 0 or pixels[x,y-1][3] == 0 or pixels[x,y+1][3] == 0):
                    # Edge pixel with green spill, make transparent
                    pixels[x, y] = (0,0,0,0)

    img.save(output_path, "PNG")

base_dir = "/Users/pbabreu/.gemini/antigravity/brain/43f1d9e2-082b-4414-a33b-6cb056040248/"
remove_green_screen(base_dir + "ghost_green_bg_1771630674218.png", "assets/ghost_isolated.png")
remove_green_screen(base_dir + "lourenco_green_bg_1771630689172.png", "assets/lourenco_isolated.png")
remove_green_screen(base_dir + "anesthesiologist_green_bg_1771630702547.png", "assets/anesthesiologist_isolated.png")
remove_green_screen(base_dir + "serumbag_green_bg_1771630720695.png", "assets/serum_bag_isolated.png")
print("Successfully processed green screen images!")
