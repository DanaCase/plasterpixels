from PIL import Image, ImageOps, ImageDraw
from sklearn import preprocessing
import numpy as np
import defopt

# The max diameter of a "pixel" ¯\_(ツ)_/¯
# This will multiply the input image size
pixelDiam = 30.0


def normalize(nparr: np.ndarray, factor:float):
    nparr = nparr/(nparr.max()/factor)
    return nparr


def getCircle(pixel):
    img = Image.new("L", (int(pixelDiam), int(pixelDiam)))
    draw = ImageDraw.Draw(img)

    # I'll just always round down for now...
    # next can bias half values in one direction
    upperx = int(pixelDiam - pixel/2)
    uppery = upperx
    draw.ellipse((upperx, uppery, upperx * 2, uppery * 2), 255)
    return img


def main(path: str):
    """
    Take a black and white image and output circles image
    """
    img = Image.open(path)
    gray_img = ImageOps.grayscale(img)
    gray_img.show()
   
    #resize
    img = gray_img.resize((int(img.width / int(pixelDiam)), int(img.height / int(pixelDiam))))
    img.show()

    #min/max normalize by pixelDiameter
    nparr = np.array(img)
    scaled = normalize(nparr, pixelDiam)
    img = Image.fromarray(scaled)
    img.show()
    #make each pixel a circle
    
    # Ok this rotates the image 90 degrees
    new = Image.new("L", (img.width * int(pixelDiam), img.height * int(pixelDiam)))
    for iy, ix in np.ndindex(scaled.shape):
        circle = getCircle(scaled[iy, ix])
        new.paste(circle, (iy * int(pixelDiam), ix * int(pixelDiam)))

    new.show()
    new.save("tmp.jpg")



if __name__ == '__main__':
    defopt.run(main)
