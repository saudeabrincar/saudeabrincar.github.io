from PIL import Image

def remove_white_bg_floodfill(img_path):
    # We use a flood fill algorithm from the corners to find the exact contiguous white background
    # This prevents removing white from INSIDE the character (like eyes, or the ghost body)
    img = Image.open(img_path).convert("RGBA")
    width, height = img.size
    pixels = img.load()
    
    # Threshold for what we consider "white background"
    def is_white(color):
        return color[0] > 240 and color[1] > 240 and color[2] > 240
        
    # Stack for flood fill
    stack = [(0, 0), (width-1, 0), (0, height-1), (width-1, height-1)]
    visited = set()
    
    while stack:
        x, y = stack.pop()
        if (x, y) in visited:
            continue
            
        if x < 0 or x >= width or y < 0 or y >= height:
            continue
            
        visited.add((x, y))
        
        current_pixel = pixels[x, y]
        if is_white(current_pixel):
            # Make it transparent
            pixels[x, y] = (255, 255, 255, 0)
            
            # Add neighbors
            stack.append((x+1, y))
            stack.append((x-1, y))
            stack.append((x, y+1))
            stack.append((x, y-1))

    # After flood fill, ensure all other pixels are fully opaque
    # to fix the DALL-E generated semi-transparency inside the characters
    for x in range(width):
        for y in range(height):
            if (x, y) not in visited:
                r, g, b, a = pixels[x, y]
                # If it wasn't part of the background, make it 100% opaque
                if a != 0: 
                    pixels[x, y] = (r, g, b, 255)

    img.save(img_path, "PNG")

try:
    # First, let's copy the raw generated versions back to override the bad processing
    import shutil
    shutil.copy("/Users/pbabreu/.gemini/antigravity/brain/43f1d9e2-082b-4414-a33b-6cb056040248/lourenco_isolated_1771628711367.png", "assets/lourenco_isolated.png")
    shutil.copy("/Users/pbabreu/.gemini/antigravity/brain/43f1d9e2-082b-4414-a33b-6cb056040248/ghost_isolated_1771628728485.png", "assets/ghost_isolated.png")
    shutil.copy("/Users/pbabreu/.gemini/antigravity/brain/43f1d9e2-082b-4414-a33b-6cb056040248/anesthesiologist_isolated_1771628743129.png", "assets/anesthesiologist_isolated.png")
    shutil.copy("/Users/pbabreu/.gemini/antigravity/brain/43f1d9e2-082b-4414-a33b-6cb056040248/serum_bag_isolated_1771628769962.png", "assets/serum_bag_isolated.png")

    remove_white_bg_floodfill("assets/lourenco_isolated.png")
    remove_white_bg_floodfill("assets/ghost_isolated.png")
    remove_white_bg_floodfill("assets/anesthesiologist_isolated.png")
    remove_white_bg_floodfill("assets/serum_bag_isolated.png")
    print("Successfully processed images with flood fill algorithm!")
except Exception as e:
    print(f"Error: {e}")
