import  sys, socket, threading

PROMPT = '::>  '
COMMAND_SIGNIFIER = '!'
MAGIC='µłeŧþøæ'  # string to separate name and message in a sent packet
DEFAULT_IP = ''
BROADCAST = '255.255.255.255'
IP = DEFAULT_IP
PORT = 10000
messages_received = []
messages_sent = []

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
SERVER = (IP, PORT)
s.bind(SERVER)

def send(header, msg):
  s.sendto((header + msg).encode(), (BROADCAST, PORT))
  messages_sent.append(msg)

def receive():
  while True:
    # print(PROMPT)
    data, address = s.recvfrom(4096)
    data = data.decode()
    [name, msg] = data.split(MAGIC)
    print(f'\n{name}: {msg}\n' + PROMPT)
    messages_received.append((name, msg))
    
def print_messages():
  print(f'Sent: {messages_sent}')
  print(f'Rcvd: {messages_received}')

def quit():
  print('\n*** Exiting. ***')
  s.close()
  sys.exit()

def process_command(cmd):
  cmd_id = cmd[0]
  commands[cmd_id]()

#######################################################
commands = {'p': print_messages, 'q': quit}

header = input('Your name?  ') + MAGIC
t_rcv = threading.Thread(target=receive, name='t_rcv')
print('Starting rcv thread...')
t_rcv.start()

# Wait for user to enter a command (then process it)
# or a message (then send it)
while True:
  msg = input(PROMPT)
  if msg.startswith(COMMAND_SIGNIFIER):
    process_command(msg[1:])
  else:
    send(header, msg)