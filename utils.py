import numpy as np
from PIL import Image
import struct
import sys

def crop_image(img_path, xmin, ymin, xmax, ymax):
    img = Image.open(img_path)
    cropped_img = img.crop((xmin, ymin, xmax, ymax))
    return cropped_img
    
def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])

def padhexa(s):
    return '0x' + s[2:].zfill(8)

def embedEncode(embedding):
    # converting a float array to hex string sequence
    return ''.join([padhexa(float_to_hex(embedding[i])) for i in range(embedding.shape[0])])