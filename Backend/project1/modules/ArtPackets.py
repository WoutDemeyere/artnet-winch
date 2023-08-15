class ArtPacket:

    # ----- Need to add protver chek (Maybe OpCode 2)
    @staticmethod
    def decode_ArtDMX(packet):

        dmx_buffer = bytearray(512)

        sequence = packet[12]
        physical = packet[13]

        subnet = packet[14] & 0xF0
        univer = packet[14] & 0x0F

        len_hex = packet[16:18]
        length = int.from_bytes(len_hex, byteorder='big')

        for i in range(length):
            dmx_buffer[i] = packet[i+17]         #Make this cleaner

        return sequence, physical, subnet, univer, length, dmx_buffer
    
    @staticmethod
    def encode_ArtDMX(sub, uni, length, dmx_data):
        assert sub >= 0 and sub <= 15    
        assert uni >= 0 and uni <= 15     
        
        packet_buffer = bytearray()

        packet_buffer.extend(bytearray('Art-Net', 'utf-8'))
        packet_buffer.append(0x0)

        # --- OpCode
        packet_buffer.append(0x00)
        packet_buffer.append(0x50)

        # --- Protver
        packet_buffer.append(0x00)
        packet_buffer.append(14)

        # --- Sequence
        packet_buffer.append(0x00)

        # --- Physical
        packet_buffer.append(0x00)

        # --- Subnet
        packet_buffer.append(sub)

        # --- Universe
        packet_buffer.append(uni)

        # --- length
        packet_buffer.append(0x20)
        packet_buffer.append(0x0)

        # --- DMX PACKET
        packet_buffer.extend(dmx_data)

        return packet_buffer
    
    @staticmethod
    def encode_ArtPoll():
        packet_buffer = bytearray()

        packet_buffer.extend(bytearray('Art-Net', 'utf-8'))
        packet_buffer.append(0x0)

        # --- OpCode
        packet_buffer.append(0x00)
        packet_buffer.append(0x20)

        # --- Protver
        packet_buffer.append(0x00)
        packet_buffer.append(14)

        # --- Flags
        packet_buffer.append(0x00)

        # --- Priority
        packet_buffer.append(0x00)

        return packet_buffer
    
    @staticmethod
    def encode_ArtPollReply(ip):
        short_name = 'RAPSBERRY PI      '

        long_name = f'SPACEMAKERS - RASPI HOIST SYSTEM - {ip}              '

        packet_buffer = bytearray()

        packet_buffer.extend(bytearray('Art-Net', 'utf-8'))
        packet_buffer.append(0x0)

        # --- OpCode
        packet_buffer.append(0x00)


        # --- IP of PI
        packet_buffer.extend(bytearray(ip, 'utf-8'))

        # --- Ethernet Port
        packet_buffer.append(0x36)
        packet_buffer.append(0x19)

        # --- Protver
        packet_buffer.append(0x00)
        packet_buffer.append(0x00)

        # --- NetSwitch & SubSwitch ports (not realy sure)
        packet_buffer.append(0x00)
        packet_buffer.append(0x00)

        # --- OEM
        packet_buffer.append(0x10)
        packet_buffer.append(0x10)

        # --- Ubea
        packet_buffer.append(0x00)

        # --- Status
        packet_buffer.append(0x00)

        # --- EstaMan
        packet_buffer.append(0x00)
        packet_buffer.append(0x00)

        # --- Short Name
        packet_buffer.append(bytearray(short_name, 'utf-8'))

        # --- Long Name
        packet_buffer.append(bytearray(long_name, 'utf-8'))

        # --- NodeReport NEEDS FIXIN 
        nodereport = bytearray(64)
        packet_buffer.extend(nodereport)

        # --- Num ports
        packet_buffer.append(0x00)
        packet_buffer.append(0x04)

        # --- Port Types
        packet_buffer.append(0x00)

        # --- GONNE ADD REST LATER
        packet_buffer.extend(bytearray(60))


        return packet_buffer

    @staticmethod
    def decode_ArtPollReply(packet):
        ip = packet[10:13]
        #ip.decode("hex")

        port_numb = hex((packet[15] << 8) | packet[14])

        short_n = packet[26:43]

        print(type(short_n))
        #short_n.decode('ascii')
        print(short_n)

        #bytes.fromhex(str(short_n)).decode('utf-8')
        #short_n.decode('hex')
        #short_name = ''
        
        # for i in short_name:
        #     short_name.append(i.decode("ascii"))

        long_name = packet[44:107]
        #long_name.decode("hex")

        takel_mac = packet[201:206]

        bindIP = packet[207:210]

        takel = {'ip':0, 'port_numb': port_numb, 'sn': short_n, 'ln': long_name, 'mac': takel_mac, 'bindIP': bindIP}

        return takel
        