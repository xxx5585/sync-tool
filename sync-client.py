# sync tool for client
# 1. pip install pynput
# 2. run this script with server ip address

# auther: xxx
# created: June 9, 2023
# changed: Dec 26, 2023



import socket
import time
import sys
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController
from pynput.keyboard import KeyCode
from pynput.keyboard import Controller as KeyController

mouse = MouseController()
keyboard = KeyController()

def operate_mouse(sprit_command):
  global mouse

  if sprit_command[1] == 'move':
    mouse.position = (sprit_command[2], sprit_command[3])

  elif sprit_command[1] == 'click':
    mouse.position = (sprit_command[2], sprit_command[3])
    if sprit_command[4] == 'Pressed':
      if sprit_command[5] == 'Button.left':
        mouse.press(Button.left)
      elif sprit_command[5] == 'Button.right':
        mouse.press(Button.right)
    elif sprit_command[4] == 'Released':
      if sprit_command[5] == 'Button.left':
        mouse.release(Button.left)
      elif sprit_command[5] == 'Button.right':
        mouse.release(Button.right)

  elif sprit_command[1] == 'tscroll':
    mouse.position = (sprit_command[2], sprit_command[3])
    mouse.scroll(sprit_command[4], sprit_command[5])

def operate_keyboard(sprit_command):
  global keyboard

  if sprit_command[1] == 'press':
    #keyboard.press(sprit_command[2])
    keyboard.press(KeyCode(int(sprit_command[2])))

    #if len(sprit_command[2]) == 1:
    #  keyboard.press(sprit_command[2])
    #else:

  elif sprit_command[1] == 'release':
    #keyboard.release(sprit_command[2])
    keyboard.release(KeyCode(int(sprit_command[2])))

    #if len(sprit_command[2]) == 1:
    #  keyboard.release(sprit_command[2])
    #else:



def operate(message):

  commands = message.rsplit('\n')

  for command in commands[:-1]:
    sprit_command = command.rsplit('\t')
    if sprit_command[0] == 'mouse':
      operate_mouse(sprit_command)
    elif sprit_command[0] == 'key':
      operate_keyboard(sprit_command)
    else:
      None


def client(host):

  #host = "0.0.0.0"  # The server's hostname or IP address
  port = 65432  # The port used by the server



  while True:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock.settimeout(100)

    while True:
      print('trying connect server:', host)
      try:
        #print('timeout', sock.gettimeout())
        sock.connect((host, port))
        break
      #except (TimeoutError,OSError:) as e:
      except:
        print('connect time out:', host)
        continue

    print('connected server:', host)

    while True:
      try:
        message_as_bytes = sock.recv(1024)
        if not message_as_bytes:
          break
      except ConnectionResetError as e:
        break
    
      message = message_as_bytes.decode()
      #print(message, end='')
      operate(message)

    print('disconnected server:', host)
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()



def main():

  args = sys.argv

  client_hostname = socket.gethostname()
  client_addr = socket.gethostbyname(client_hostname)
  #print('server host name:', server_hostname)
  print('client ip address:', client_addr)


  ip = ''

  if len(args) < 2:
    ip = input("input server ip address > ")
  else:
    ip = args[1]

  client(ip)
  

  #input()

if __name__ == '__main__':
  main()


