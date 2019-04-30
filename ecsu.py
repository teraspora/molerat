import  sys, socket, threading, os

# Colour codes
CLR_R  = '\u001B[31m'
CLR_LR = '\u001B[91m'
CLR_LG = '\u001B[92m'
CLR_LY = '\u001B[93m'
CLR_LB = '\u001B[94m'
CLR_LM = '\u001B[95m'
CLR_LC = '\u001B[96m'
RESET  = '\u001B[0m'

def print_in_colour(text, colour_code):
  print(colour_code + text + RESET)

PROMPT = CLR_R + '::>  ' + RESET
COMMAND_SIGNIFIER = '!'
MAGIC='µłeŧþøæ'  # string to separate name and message in a sent packet
DEFAULT_IP = ''
BROADCAST = '255.255.255.255'
IP = DEFAULT_IP
PORT = 10000
messages_received = []
messages_sent = []

this_ip = os.popen('hostname -I').read()[:-2]
print(f'This machine\'s IPv4 address is {this_ip}')

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
SERVER = (IP, PORT)
s.bind(SERVER)

def send(header, msg):
  s.sendto((header + msg).encode(), (BROADCAST, PORT))
  messages_sent.append(msg)

def receive():
  while True:
    data, address = s.recvfrom(4096)
    if address != (this_ip, PORT):  # don't reprint msgs sent from here
      data = data.decode()
      [name, msg] = data.split(MAGIC)
      print_in_colour(f'\n{name}: {msg}', CLR_LY)
      print(PROMPT)
      messages_received.append((name, msg))
    
def print_messages():
  print_in_colour(f'Sent: {messages_sent}', CLR_LM)
  print_in_colour(f'Rcvd: {messages_received}', CLR_LR)

def quit():
  print_in_colour('\n*** Exiting. ***', CLR_R)
  s.close()
  os._exit(0)

def process_command(cmd):
  cmd_id = cmd[0]
  commands[cmd_id]()

#######################################################
# add a command here and implement the fundction specified
commands = {'p': print_messages, 'q': quit}

header = input(CLR_LG + 'Your name?  ' + RESET) + MAGIC
t_rcv = threading.Thread(target=receive, name='t_rcv')
print_in_colour('Starting rcv thread...', CLR_LR)
t_rcv.start()

# Wait for user to enter a command (then process it)
# or a message (then send it)
while True:
  msg = input(PROMPT)
  if msg.startswith(COMMAND_SIGNIFIER):
    process_command(msg[1:])
  else:
    send(header, msg)