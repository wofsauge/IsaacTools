import sys
from PIL import Image
from pathlib import Path
import numpy as np
global baseColors, colorVariants, path

#### When using this script without arguments, define a folder path to look for sprites ####
path = None # example: "C:\\Workspace\\test"

#### Color definitions ####
# HEX colors that should be replaced in all spritesheets of the given folder
# baseColors are the default skin colors of isaac. 
# colorVariants are the counterpart colors for each skin color variant of isaac
baseColors = ["e3c6c5", "cf9c9b", "b97371"]
colorVariants = {
    "_black": ["2e2e2e", "232323", "181818"],
    "_blue": ["566c8a", "405066", "2c3747"],
    "_grey": ["a7a7a7", "787878", "545454"],
    "_red": ["992424", "792020", "571717"],
    "_green": ["cbefbf", "9fcf8f", "7ba467"],
    "_white": ["ffffff", "e2e2e2", "c2c2c2"],
}

############### Code #################

def findFiles(folderPath):
    for path in Path(folderPath).rglob("*.png"):
        skip = False
        for k in colorVariants.keys():
            if k in str(path):
                skip = True
                break
        if not skip:
            createSkinVariants(path)

def hex_to_rgb(hex_str: str) -> np.ndarray:
    hex_str = hex_str.strip()

    if hex_str[0] == "#":
        hex_str = hex_str[1:]

    if len(hex_str) != 6:
        raise ValueError("Input #{} is not in #RRGGBB format.".format(hex_str))

    r, g, b = (
        int(hex_str[:2], base=16),
        int(hex_str[2:4], base=16),
        int(hex_str[4:], base=16),
    )
    return np.array([r, g, b, 255])


def convertLookupTables():
    for i in range(0, len(baseColors)):
        baseColors[i] = hex_to_rgb(baseColors[i])
        for k in colorVariants.keys():
            colorVariants[k][i] = hex_to_rgb(colorVariants[k][i])



def createSkinVariants(fileName):
    print("Processing file: ", fileName)
    img = Image.open(fileName)

    in_data = np.asarray(img)
    for colorSuffix in colorVariants.keys():
        out_data = in_data.copy()
        for i in range(0, len(baseColors)):
            oldColor = baseColors[i]
            newColor = colorVariants[colorSuffix][i]
            mask = np.all(out_data == oldColor, axis=-1)
            out_data[mask] = newColor

        out_img = Image.fromarray(out_data)
        out_img.save(str(fileName).replace(".png", colorSuffix + ".png"))


def main():
    convertLookupTables()
    if path is not None:
        findFiles(path)
    elif len(sys.argv) == 2:
        findFiles(*sys.argv[1:])
    else:
        fmt = "Isaac skin color variant generator\nUsage: {} input_folder"
        print(fmt.format(sys.argv[0]))


if __name__ == "__main__":
    main()
