from PIL import Image
import shutil

def remove_white_bg_floodfill(img_path):
    img = Image.open(img_path).convert("RGBA")
    width, height = img.size
    pixels = img.load()
    
    def is_white(color):
        return color[0] > 240 and color[1] > 240 and color[2] > 240
        
    stack = [(0, 0), (width-1, 0), (0, height-1), (width-1, height-1)]
    visited = set()
    
    while stack:
        x, y = stack.pop()
        if (x, y) in visited: continue
        if x < 0 or x >= width or y < 0 or y >= height: continue
        visited.add((x, y))
        
        current_pixel = pixels[x, y]
        if is_white(current_pixel):
            pixels[x, y] = (255, 255, 255, 0)
            stack.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])

    for x in range(width):
        for y in range(height):
            if (x, y) not in visited:
                r, g, b, a = pixels[x, y]
                if a != 0: 
                    pixels[x, y] = (r, g, b, 255)

    img.save(img_path, "PNG")

try:
    shutil.copy("/Users/pbabreu/.gemini/antigravity/brain/43f1d9e2-082b-4414-a33b-6cb056040248/ghost_isolated_1771628728485.png", "/Users/pbabreu/saudeabrincar-antigravity/assets/ghost_isolated.png")
    remove_white_bg_floodfill("/Users/pbabreu/saudeabrincar-antigravity/assets/ghost_isolated.png")
    print("Successfully restored ghost!")
except Exception as e:
    print(f"Error: {e}")
