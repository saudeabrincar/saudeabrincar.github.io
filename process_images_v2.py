from PIL import Image

def remove_white_bg(img_path):
    img = Image.open(img_path).convert("RGBA")
    datas = img.getdata()
    
    newData = []
    # For colored pencil drawings on white, we only want to remove true/near true white
    # The previous script was too aggressive. Let's make it very precise.
    for item in datas:
        # Check if pixel is VERY close to white (e.g. above 250 for all RGB)
        if item[0] > 250 and item[1] > 250 and item[2] > 250:
            # We must set alpha to 0 for these white pixels
            newData.append((255, 255, 255, 0)) 
        else:
            # Keep the original pixel EXACTLY as it is, fully opaque (alpha=255)
            # DALL-E sometimes generates slight transparency, force 255
            newData.append((item[0], item[1], item[2], 255))
            
    img.putdata(newData)
    img.save(img_path, "PNG")

try:
    # First, let's copy the raw generated versions back to override the bad processing
    import shutil
    shutil.copy("/Users/pbabreu/.gemini/antigravity/brain/43f1d9e2-082b-4414-a33b-6cb056040248/lourenco_isolated_1771628711367.png", "assets/lourenco_isolated.png")
    shutil.copy("/Users/pbabreu/.gemini/antigravity/brain/43f1d9e2-082b-4414-a33b-6cb056040248/ghost_isolated_1771628728485.png", "assets/ghost_isolated.png")
    shutil.copy("/Users/pbabreu/.gemini/antigravity/brain/43f1d9e2-082b-4414-a33b-6cb056040248/anesthesiologist_isolated_1771628743129.png", "assets/anesthesiologist_isolated.png")
    shutil.copy("/Users/pbabreu/.gemini/antigravity/brain/43f1d9e2-082b-4414-a33b-6cb056040248/serum_bag_isolated_1771628769962.png", "assets/serum_bag_isolated.png")

    remove_white_bg("assets/lourenco_isolated.png")
    remove_white_bg("assets/ghost_isolated.png")
    remove_white_bg("assets/anesthesiologist_isolated.png")
    remove_white_bg("assets/serum_bag_isolated.png")
    print("Successfully processed images with v2 script!")
except Exception as e:
    print(f"Error: {e}")
