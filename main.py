from PIL import Image, ImageOps, ImageDraw
from sklearn import preprocessing
import numpy as np
import defopt
from operator import itemgetter

# The max diameter of a "pixel" ¯\_(ツ)_/¯
# This will multiply the input image size
pixelDiam = 8.0


def normalize(nparr: np.ndarray, factor:float):
    nparr = nparr/(nparr.max()/factor)
    return nparr


def resize(img: Image.Image, width:int = None, height:int = None):
    if (width == None):
        width = int(img.width / int(pixelDiam))
        height = int(img.height / int(pixelDiam))
    return img.resize((width, height))



def getCircleCoord(pixel, pixelDiam):
    # I'll just always round down for now...
    # next can bias half values in one direction
    
    upperx = int(pixelDiam/2 - pixel/2)
    uppery = upperx
    
    lowerx = int(pixelDiam/2 + pixel/2) 
    lowery = lowerx
    return {
            "upperx": upperx,
            "uppery": uppery,
            "lowerx": lowerx,
            "lowery": lowery
            }


def getCircle(pixel):
    img = Image.new("L", (int(pixelDiam), int(pixelDiam)), 255)
    draw = ImageDraw.Draw(img)

    circleCoords = getCircleCoord(pixel, pixelDiam)
    upperx, uppery, lowerx, lowery = itemgetter('upperx', 'uppery', 'lowerx', 'lowery')(circleCoords)
    draw.ellipse((upperx, uppery, lowerx, lowery), 0)
    return img


def main(path: str):
    """
    Take a black and white image and output circles image
    """
    img = Image.open(path)
    gray_img = ImageOps.grayscale(img)
    gray_img.show()
   
    #resize
    img = resize(gray_img) 
    img.show()

    #invert
    img = ImageOps.invert(img)

    #min/max normalize by pixelDiameter
    nparr = np.array(img)
    scaled = normalize(nparr, pixelDiam)
    img = Image.fromarray(scaled)
    img.show()

    #make each pixel a circle
    new = Image.new("L", (img.width * int(pixelDiam), img.height * int(pixelDiam)))
    for iy, ix in np.ndindex(scaled.shape):
        circle = getCircle(scaled[iy, ix])
        new.paste(circle, (ix * int(pixelDiam), iy * int(pixelDiam)))

    new.show()
    new.save("tmp.jpg")



if __name__ == '__main__':
    defopt.run(main)
