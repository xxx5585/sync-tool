# sync tool for server
# 1. pip install pynput
# 2. run this script

# auther: xxx
# created: June 9, 2023
# changed: Dec 25, 2023



import socket
import threading
from pynput import keyboard
from pynput import mouse



client_sockets = []
lock = threading.Lock()
sync_flg = True
ctrl_flg = False


def on_move(x, y):
  if not sync_flg:
    return

  message = 'mouse\tmove\t{0}\t{1}\n'.format(x,y)

  send_message(message)

def on_click(x, y, button, pressed):
  if not sync_flg:
    return

  message = 'mouse\tclick\t{0}\t{1}\t{2}\t{3}\n'.format(
    x,y,
    'Pressed' if pressed else 'Released',
    button)

  send_message(message)

def on_scroll(x, y, dx, dy):
  if not sync_flg:
    return

  message = 'mouse\tscroll\t{0}\t{1}\t{2}\t{3}\n'.format(x,y,dx,dy)

  send_message(message)


def on_press(key):

  global ctrl_flg

  if key == keyboard.Key.ctrl_l:
    ctrl_flg = True

  if not sync_flg:
    return


  try:
    key_code = key.vk
    #print(1, key_code)
  except AttributeError:
    key_code = key.value.vk
    #print(2, key_code)

  message = 'key\tpress\t{0}\n'.format(key_code)

  '''
  if 'char' in dir(key):
    message = 'key\tpress\t{0}'.format(key.char)
    #if key.char == 'a':
    #  print('you pressed a')

  else:
    message = 'key\tpress\t{0}'.format(key)
  '''

  send_message(message)




def on_release(key):

  global sync_flg
  global ctrl_flg
  message_release_ctrl = ""

  if key == keyboard.Key.ctrl_l:
    ctrl_flg = False

  if key == keyboard.Key.f1 and ctrl_flg:
    if sync_flg:
      message_release_ctrl = 'key\trelease\t{0}\n'.format(keyboard.Key.ctrl_l.value.vk)

    sync_flg = not sync_flg
    print('sync:', 'On' if sync_flg else 'Off')

  elif not sync_flg:
    return


  ## 112 is F1 key
  #if key_code == 112:
  #  sync_flg = not sync_flg
  #  print('sync:', 'On' if sync_flg else 'Off')


  try:
    key_code = key.vk
    #print(1, key_code)
  except AttributeError:
    key_code = key.value.vk
    #print(2, key_code)

  message = 'key\trelease\t{0}\n'.format(key_code)
  message += message_release_ctrl

  '''
  if 'char' in dir(key):
    message = 'key\trelease\t{0}'.format(key.char)
    #if key.char == 'a':
    #  print('you released a')
  else:
    message = 'key\trelease\t{0}'.format(key)
    if key == keyboard.Key.esc:
      # Stop listener
      return False
  '''

  send_message(message)

def send_message(message):
  global count
  global lock
  global sync_flg

  #print(message, end='')

  with lock:
    for (client_socket, addr) in client_sockets[:]:

      message_as_bytes = message.encode()
      try:
        client_socket.send(message_as_bytes)
      except (ConnectionAbortedError, ConnectionResetError) as e:
        print('disconnected client:', addr)
        client_sockets.remove((client_socket, addr))
        client_socket.close()

def main():

  global client_sockets
  global lock

  listener = mouse.Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll)
  listener.start()

  listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
  listener.start()

  #host = socket.gethostname()
  server_hostname = socket.gethostname()
  server_addr = socket.gethostbyname(server_hostname)
  #print('server host name:', server_hostname)
  print('server ip address:', server_addr)
  host = '0.0.0.0'
  port = 65432


  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_socket.bind((host, port))
  server_socket.listen()

  print('waiting clients')
  while True:
    client_socket, addr = server_socket.accept()
    print('connected client:', addr)
    with lock:
      client_sockets.append((client_socket, addr))

  server_socket.close()

if __name__ == '__main__':
  main()
