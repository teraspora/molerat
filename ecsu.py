import  sys, socket, threading

DEFAULT_IP = ''
BROADCAST = '255.255.255.255'
THIS_IP = '192.168.8.104'
IP = DEFAULT_IP
PORT = 10000
msg1 = 'Hello Andromeda!'

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
SERVER = (IP, PORT)
print(f'Server address: {SERVER}')
s.bind(SERVER)

def send(msg):
  s.sendto(msg, (BROADCAST, PORT))
    


def receive():
  while True:
    print('Waiting...')
    data, address = s.recvfrom(4096)
    print(f'From {address}: {data}')

send(msg1.encode())

t_rcv = threading.Thread(target=receive, name='t_rcv')
print('Starting rcv thread...')
t_rcv.start()
