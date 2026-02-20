from PIL import Image
import shutil

def process_image(img_path, original_path):
    # Restore original image
    shutil.copy(original_path, img_path)
    
    img = Image.open(img_path).convert("RGBA")
    width, height = img.size
    pixels = img.load()
    
    # We define background as light colors (paper texture can be off-white)
    def is_bg(color):
        r, g, b, _ = color
        return r > 200 and g > 200 and b > 200

    # Flood fill transparent from corners
    stack = [(0, 0), (width-1, 0), (0, height-1), (width-1, height-1)]
    visited = set()
    
    while stack:
        x, y = stack.pop()
        if (x, y) in visited: continue
        if x < 0 or x >= width or y < 0 or y >= height: continue
        visited.add((x, y))
        
        if is_bg(pixels[x, y]):
            pixels[x, y] = (255, 255, 255, 0)
            stack.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])
            
    # Morphological erosion to eat the halo
    # If a pixel borders transparency and is relatively light, make it transparent
    for _ in range(3): # 3 passes of erosion for a cleaner edge
        img_copy = img.copy()
        pixels_copy = img_copy.load()
        for x in range(1, width-1):
            for y in range(1, height-1):
                if pixels[x, y][3] > 0:
                    r, g, b, a = pixels[x, y]
                    # Check if borders transparency
                    if pixels_copy[x-1,y][3] == 0 or pixels_copy[x+1,y][3] == 0 or pixels_copy[x,y-1][3] == 0 or pixels_copy[x,y+1][3] == 0:
                        # Check if it's light colored (part of the halo/anti-aliasing)
                        if r > 160 and g > 160 and b > 160:
                            pixels[x, y] = (255, 255, 255, 0)

    # Finally, ensure everything that remains is completely opaque
    for x in range(width):
        for y in range(height):
            if pixels[x, y][3] > 0:
                r, g, b, a = pixels[x, y]
                pixels[x, y] = (r, g, b, 255)

    img.save(img_path, "PNG")

original_dir = "/Users/pbabreu/.gemini/antigravity/brain/43f1d9e2-082b-4414-a33b-6cb056040248/"
process_image("assets/lourenco_isolated.png", original_dir + "lourenco_isolated_1771628711367.png")
process_image("assets/ghost_isolated.png", original_dir + "ghost_isolated_1771628728485.png")
process_image("assets/anesthesiologist_isolated.png", original_dir + "anesthesiologist_isolated_1771628743129.png")
process_image("assets/serum_bag_isolated.png", original_dir + "serum_bag_isolated_1771628769962.png")
print("Successfully refined image cutouts!")
