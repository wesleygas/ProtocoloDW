# ProtocoloDW

HEAD -  20b (ou 10b) :

2 bytes para tamanho -> Max payload size 65kb
2 bytes para package count (0-255 de 0-255) -> Max file size 16.7mb 

STUFFING: 

0xEF (EstufFing) || 239 || 1110 1111

TAIL/EOP:

0xBABACA (Pq é legal e dá pra ler facil)