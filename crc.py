import numpy as np
from binascii import crc_hqx

def crc16(data):
    data_bytes = bytes(data)
    crc = crc_hqx(data_bytes,0xFFFF)
    
    return crc

print(format(crc16(bytes([254])),'#04X'))


#print(format(crc_hqx(bytes([254]),0xFFFF),'#04X'))