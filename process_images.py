from PIL import Image

def remove_white_bg(img_path):
    img = Image.open(img_path).convert("RGBA")
    datas = img.getdata()
    
    newData = []
    for item in datas:
        # Check if the pixel is close to white (allow some tolerance for DALL-E anti-aliasing)
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            newData.append((255, 255, 255, 0)) # transparent
        else:
            newData.append(item)
            
    img.putdata(newData)
    img.save(img_path, "PNG")

remove_white_bg("assets/lourenco_isolated.png")
remove_white_bg("assets/ghost_isolated.png")
remove_white_bg("assets/anesthesiologist_isolated.png")
remove_white_bg("assets/serum_bag_isolated.png")
print("Successfully processed images!")
