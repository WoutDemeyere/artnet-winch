from repositories.DataRepository import DataRepository
from modules.artnet2 import artnet

from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS

import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess
import netifaces as ni


import time
import threading

# ---- OLED THINGS
disp = Adafruit_SSD1306.SSD1306_128_32(rst=None)

disp.begin()

disp.clear()
disp.display()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))


draw = ImageDraw.Draw(image)

draw.rectangle((0,0,width,height), outline=0, fill=0)


padding = -2
top = padding
bottom = height-padding
x = 0

font = ImageFont.load_default()

ni.ifaddresses('eth0')

# --- ARTNET THINGS

node = artnet(ni.ifaddresses('eth0')[2][0]['addr'], 6454)
dmx_packet = bytearray(512)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hier mag je om het even wat schrijven, zolang het maar geheim blijft en een string is'

socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

# takel_ip = '169.254.10.50'

DataRepository.clear_takels()

# ----- USED SUBS / UNI / CHAN

# -- SET START
SUB_set_start = 0 
UNI_set_start = 1
CHAN_set_start = 40

# -- SET END
SUB_set_end = 0 
UNI_set_end = 1
CHAN_set_end = 41

# -- SET ZERO
SUB_set_zero = 0 
UNI_set_zero = 1
CHAN_set_zero = 30

# -- MOVE UP
SUB_move_up = 0 
UNI_move_up = 1
CHAN_move_up = 50

# -- MOVE DOWN
SUB_move_down = 0 
UNI_move_down = 1
CHAN_move_down = 51

# -- SET ARTNET VALUES
SUB_set_vals = 0 
UNI_set_vals = 1

CHAN_set_vals = 69

CHAN_set_sub = 72
CHAN_set_uni = 73
CHAN_set_chan = 70

VAL_FOR_EXE = 56


def oled_show_info():
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    #cmd = "hostname -I | cut -d\' \' -f1"
    IP_et = ni.ifaddresses('eth0')[2][0]['addr']
    IP_wlan = ni.ifaddresses('wlan0')[2][0]['addr']

    draw.text((x, top),       "IP eth: " + IP_et,  font=font, fill=255)
    draw.text((x, top+16),    "IP wlan: " + IP_wlan, font=font, fill=255)

    disp.image(image)
    disp.display()


@socketio.on('connect')
def initial_connection():
    print('A new client connect')

    socketio.emit('B2F_status_lampen', {'msg': 'Hello there'})

@socketio.on('F2B_change_pos')
def change_pos(data):
    print('change in pos')
    pos = data['pos']
    takel_ip = data['ip']
    
    node.send_channel(takel_ip, 0, 0, 1, int(pos))
    

@socketio.on('F2B_move')
def move_takel(data):
    dr = data['mv']
    takel_ip = data['ip']

    if dr == 'up':
        print('moving up')
        node.send_channel(takel_ip, SUB_move_up, UNI_move_up, CHAN_move_up, VAL_FOR_EXE)
    elif dr == 'down':
        print('moving down')
        node.send_channel(takel_ip, SUB_move_down, UNI_move_down, CHAN_move_down, VAL_FOR_EXE)
    elif dr == 'none':
        print('none')
        node.send_channel(takel_ip, SUB_move_up, UNI_move_up, CHAN_move_up, 0)
        node.send_channel(takel_ip, SUB_move_down, UNI_move_down, CHAN_move_down, 0)

@socketio.on('F2B_set_start')
def set_start(data):
    start = data['start']
    takel_ip = data['ip']
    
    if start:
        print('setting start')
        node.send_channel(takel_ip, SUB_set_start, UNI_set_start, CHAN_set_start, VAL_FOR_EXE)

        #t = threading.Thread(target=node.read_start(0, 0))
        #t.start()
    else:
        # socketio.emit('B2F_new_start', {'slider_val': 0})
        node.send_channel(takel_ip, SUB_set_start, UNI_set_start, CHAN_set_start, 0)

@socketio.on('F2B_set_end')
def set_end(data):
    start = data['end']
    takel_ip = data['ip']
    
    if start:
        print('setting end')
        node.send_channel(takel_ip, SUB_set_end, UNI_set_end, CHAN_set_end, VAL_FOR_EXE)
    else:
        # socketio.emit('B2F_new_end', {'slider_val': 255})
        node.send_channel(takel_ip, SUB_set_end, UNI_set_end, CHAN_set_end, 0)

@socketio.on('F2B_set_art_vals')
def set_art_vals(data):
    takel_ip = data['ip']
    #
    sub = int(data['sub'])
    uni = int(data['uni'])
    chan = int(data['chan'])
    
    print(f'setting artnet vals sub: {sub}  uni: {uni}  chan: {chan}')

    # --- DATABASE PART

    DataRepository.update_chan(takel_ip, chan)
    DataRepository.update_sub(takel_ip, sub)
    DataRepository.update_uni(takel_ip, uni)

    # --- ARTNET PART

    node.send_channel(takel_ip, SUB_set_vals, UNI_set_vals, CHAN_set_vals, VAL_FOR_EXE)
    node.send_channel(takel_ip, SUB_set_vals, UNI_set_vals, CHAN_set_chan, chan)
    node.send_channel(takel_ip, SUB_set_vals, UNI_set_vals, CHAN_set_sub, sub)
    node.send_channel(takel_ip, SUB_set_vals, UNI_set_vals, CHAN_set_uni, uni)
    time.sleep(0.3)
    node.send_channel(takel_ip, SUB_set_vals, UNI_set_vals, CHAN_set_vals, 0)


@socketio.on('F2B_set_zero')
def set_zero(data):
    start = data['set']
    takel_ip = data['ip']
    
    if start:
        print('setting zero')
        node.send_channel(takel_ip, SUB_set_zero, UNI_set_zero, CHAN_set_zero, VAL_FOR_EXE)
    else:
        # socketio.emit('B2F_new_end', {'slider_val': 255})
        node.send_channel(takel_ip, SUB_set_zero, UNI_set_zero, CHAN_set_zero, 0)


@socketio.on('F2B_find_devs')
def get_ip():
    print('Giving IP')

    t = threading.Thread(target=node.callout())
    t.start()

    takels = []

    ips = node.get_ips()

    for i in range(len(ips)):
        print(ips[i])
        DataRepository.add_takel(i, ips[i])
    
    for i in ips:
        takels.append(DataRepository.get_takel_info(i))

    socketio.emit('B2F_devices', takels) 

@socketio.on('F2B_give_takel_id')
def get_ip(data):
    print('Giving takel info')

    idd = int(data['id'])
    takel = DataRepository.get_takel_by_id(idd)

    print(takel)

    socketio.emit('B2F_takel_info', takel) 



DataRepository.add_controller(0, ni.ifaddresses('eth0')[2][0]['addr'])

while 1:
    oled_show_info()
    socketio.run(app, debug=False, host='0.0.0.0')




    

