import socket
import select

from .ArtPackets import ArtPacket

import time
import threading

OpCodes = {'ArtPoll':0x2000, 'ArtPollReply':0x2100, 'ArtAddress':0x6000, 'ArtInput':0x7000, 'ArtDMX':0x5000, 'ArtNzs':0x5100, 'ArtSync':0x5200}


class artnet:
    def __init__(self, local_ip, local_port):
        self.port = local_port
        self.pi_ip = local_ip

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.socket.bind((self.pi_ip, self.port))
        self.socket.setblocking(0)
        self.socket.settimeout(3)

        self.takels = ['192.169.1.69']

        self.rec_data = 0
        self.rec_ip = 0

        self.Op_is_ArtPollReply = False
        self.Op_is_ArtDMX = False

        self.dmx_packet = bytearray(512)

        self.seq = 0
        self.phy = 0
        self.subn= 0
        self.univ= 0
        self.length= 0 

        self.dmx_buffer = bytearray(512)


    def get_OpCode(self, packet):
        opcode = hex((packet[9] << 8) | packet[8])
        return opcode

    def callout(self):
        self.send_ArtPoll()
        #while 1:
        print('HELLO THERE')

        
        rec_data, rec_ip = self.socket.recvfrom(1024)

        #OpCode = self.get_OpCode(self.rec_data)
        OpCode = (rec_data[9] << 8) | rec_data[8]

        print(rec_data)

        if OpCode == OpCodes['ArtPoll']:
            self.send_ArtPollReply()
            self.Op_is_ArtDMX = False

        elif OpCode ==OpCodes['ArtPollReply']:
            takel = ArtPacket.decode_ArtPollReply(rec_data)
            takel['ip'] = rec_ip[0]

            if takel['ip'] not in self.takels:
                print('GOT TAKEL')
                self.takels.append(takel['ip'])

            
            print(self.takels)
            self.Op_is_ArtDMX = False
        elif OpCode == 0x5000:
            pass
                
            
    
        
    def read_channel(self, sub, uni, chan):
        rec_data, rec_ip = self.socket.recvfrom(1024)

        OpCode = (rec_data[9] << 8) | rec_data[8]

        if OpCode == OpCodes['ArtDMX']:
            self.seq, self.phy, self.subn, self.univ, self.length, self.dmx_buffer = ArtPacket.decode_ArtDMX(self.rec_data)
        
        if sub == self.subn and uni == self.univ:
            for i in range(self.length):
                if i == chan:
                    return dmx_buffer[i]
    
    def read_start(self, sub, uni):
        rec_data, rec_ip = self.socket.recvfrom(1024)

        print(rec_data)

        OpCode = (rec_data[9] << 8) | rec_data[8]

        if OpCode == OpCodes['ArtDMX']:
            self.seq, self.phy, self.subn, self.univ, self.length, self.dmx_buffer = ArtPacket.decode_ArtDMX(self.rec_data)
        
        if sub == self.subn and uni == self.univ:          
            byte1 =  self.dmx_buffer[80]
            byte2 =  self.dmx_buffer[81]
            byte3 =  self.dmx_buffer[82]
            byte4 =  self.dmx_buffer[83]

        print(byte1)
        print(byte2)
        print(byte3)
        print(byte4)

    def send_ArtPoll(self):
        ArtPollPacket = ArtPacket.encode_ArtPoll()
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket.sendto(ArtPollPacket, ('255.255.255.255', self.port))
        print('sending ArtPoll')
    
    def send_ArtPollReply(self):
        ArtPollReplyPacket = ArtPacket.encode_ArtPollReply(self.pi_ip)
        self.socket.sendto(ArtPollReplyPacket, (self.rec_ip, self.port))
    
    def send_channel(self, ip, sub, uni, chan, val):
        for i in range(512):
            if i == chan:
                self.dmx_packet[i] = val
    
        encoded_packet = ArtPacket.encode_ArtDMX(sub, uni, len(self.dmx_packet), self.dmx_packet)
        self.socket.sendto(encoded_packet, (ip, self.port))
    
    def get_ips(self):
        return self.takels
    

    