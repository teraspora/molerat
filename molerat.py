# Molerat Messenger
# Author: John Lynch
# April 2019

import socket, threading, os, datetime

# ANSI Colour codes for terminal output
CLR_R  = '\u001B[31m'
CLR_LR = '\u001B[91m'
CLR_LG = '\u001B[92m'
CLR_LY = '\u001B[93m'
CLR_LB = '\u001B[94m'
CLR_LM = '\u001B[95m'
CLR_LC = '\u001B[96m'
RESET  = '\u001B[0m'
REVERSE_VIDEO = "\u001B[7m"

USAGE_INFO = (
      f'\n{CLR_LC}Usage:{CLR_LM}\n\n'
      f'{CLR_LR}Molerat Messenger:{CLR_LM}  A simple UDP subnet messenger program\n'
      f'~~~~~~~ ~~~~~~~~~   ~ ~~~~~~ ~~~ ~~~~~~ ~~~~~~~~~ ~~~~~~~\n'
      f'Requires Python 3: run in terminal: "python3 ecsu.py"\n'
      f'Run it on another computer too, and send text messages back and forth.\n\n'
      f'{CLR_LC}Note:{CLR_LM} the program uses UDP, which does not guarantee delivery;\n'
      f'some messages may therefore not arrive, and so the program should not\n'
      f'be used for critical systems.\n\n'
      f'Enter your name when requested.\n'
      f'Enter messages directly at the prompt, or commands prefixed by a bang ("!").\n\n'
      f'{CLR_LC}Commands:{CLR_LM}\n'
      f'{RESET}!p{CLR_LM}  Print all messages sent and received\n'
      f'{RESET}!n{CLR_LM}  Print general info\n'
      f'{RESET}!q{CLR_LM}  Quit the program\n'
      f'{RESET}!h{CLR_LM}  Print this usage info\n\n'
  )
PROGRAM_NAME = 'Molerat Messenger '

WELCOME_MSG = (
    '\nWelcome to ' + CLR_LR + PROGRAM_NAME + CLR_LM + 
    '- a simple UDP subnet messenger program\n'
    'For help type "!h".\n'
)

def print_in_colour(text, colour_code = CLR_LB):
  """
  Print a string to the terminal in the colour specified by the second argument.
  """
  print(colour_code + text + RESET, end = '')

PROMPT = CLR_LC + datetime.datetime.now().strftime('%H:%M') + CLR_R + ':> ' + RESET
COMMAND_SIGNIFIER = '!'  # if this is first char of input, it signifies a command, not a message
MAGIC='µłeŧþøæ'  # string to separate name and message in a sent packet
BROADCAST = '255.255.255.255'
IP = ''
PORT = 10000
messages_received = []
messages_sent = []

# set up socket and bind to port 10000
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((IP, PORT))

def send(header, msg):
  """
  Given a string, send it as a message, with the given header prepended, to the subnet broadcast address.
  """
  s.sendto((header + msg).encode(), (BROADCAST, PORT))
  messages_sent.append(msg)

def receive():
  """
  Wait to receive messages on port 10000; for each message received, 
  print it and append to list of received messages; then carry on waiting.
  (Run in separate thread)
  """
  while True:
    data, address = s.recvfrom(4096)
    if address != (this_ip, PORT):  # don't reprint msgs sent from here
      data = data.decode()
      [name, msg] = data.split(MAGIC)
      print_in_colour(f'\n{CLR_LR + name}:{CLR_LY} {msg}\n{PROMPT}', CLR_LY)
      messages_received.append((name, msg))
    
def print_messages():
  """
  Print the lists of messages sent and received.
  """
  print_in_colour(f'Sent: {messages_sent}\n', CLR_LM)
  print_in_colour(f'Rcvd: {messages_received}\n', CLR_LR)

def quit():
  """
  Close the socket and quit the program.
  """
  print_in_colour('\n*** Exiting. ***\n', CLR_R)
  s.close()
  os._exit(0)

def process_command(cmd):
  """
  Call the appropriate function to handle command input by user.
  """
  cmd_id = cmd[0]
  if cmd_id in commands:
    commands[cmd_id]()
  else:
    print_in_colour(f'{REVERSE_VIDEO}*** ERROR: !{cmd_id} is not a valid command ***\n', CLR_R)

def print_info():
  """
  Print general info
  """
  num_correspondents = len({a for (a, _) in messages_received})
  info = (
      f'Logged in as {name} to {this_ip}.\n'
      f'Messages: sent {len(messages_sent)}, received {len(messages_received)} '
      f'from {num_correspondents} correspondent{"" if num_correspondents == 1 else "s"}.\n'
  )
  print_in_colour(info, CLR_LG)

def help():
  """
  Print usage info
  """
  print_in_colour(USAGE_INFO, CLR_LM)
      
#######################################################

# To add a new command add here, with code, and implement the function specified
commands = {'p': print_messages, 'q': quit, 'n': print_info, 'h': help}

# Print welcome info
print_in_colour(WELCOME_MSG, CLR_LM)
# get local IP and print it, for user's info
# and so as not to print local origin messages twice
this_ip = os.popen('hostname -I').read()[:-2]
print_in_colour(f'This machine\'s IPv4 address is {this_ip}\n\n', CLR_LG)

# get user's name and pack with MAGIC string to make message header
name = input(CLR_LM + 'Your name?  ' + RESET)
header = name + MAGIC

# Spawn a thread to listen for incoming messages
t_rcv = threading.Thread(target=receive, name='t_rcv')
t_rcv.start()

# Wait for user to enter a command (then process it)
# or a message (then send it)
while True:
  msg = input(PROMPT)
  if msg.startswith(COMMAND_SIGNIFIER):
    process_command(msg[1:])
  else:
    send(header, msg)