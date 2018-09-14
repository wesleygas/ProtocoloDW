# ProtocoloDW

HEAD -  20b:

1[0] byte para tamanho -> Max payload size 128 bytes
2[1:3] bytes para package number (max 65535)  Max file size 16.7mb
2[3:5] byte para o total de pacotes 
1[5] byte  para tipo da mensagem:
1[6:8] byte para Erro de envio/Pacote esperado
4[8:12] bytes para o CRC
    
    Tipos:
        1 - (Client) Server, você me ouve?
        2 - (Server) Sim,estou te ouvindo, você me ouve? 
        3 - (Client) Sim, eu também te ouço, vou começar a transmitir!
        4 - (Client) Dados
        5 - (Server) ACK - Tudo ok com a mensagem recebida
        6 - (Server) NACK - Algum erro aconteceu com a mensagem
        7 - (Ambos)  Quero fechar a conexão = "Tchau"
        8 - (Server) Pacote errado: (Inclui o pacote esperado no seu Head[6:7])

STUFFING: 

0xEF (EstufFing) || 239 || 1110 1111

TAIL/EOP:

0xBEBADA || 190 186 218  (Pq é legal e dá pra ler facil)

CRC poly:

0xA001
