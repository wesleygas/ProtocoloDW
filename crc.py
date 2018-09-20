import numpy as np
from binascii import crc_hqx

def crc16(data):
    crc = crc_hqx(data,0xFFFF)
    
    return crc
