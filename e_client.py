import  sys, socket
BROADCAST = '255.255.255.255'
MAGIC='µłeŧþøæ'  # string to separate name and message in a sent packet

IP = BROADCAST
PORT = 10000
SERVER = (IP, PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

while True:
  msg = input("::>  ")
  s.sendto(('Client' + MAGIC + msg).encode(), SERVER)
  