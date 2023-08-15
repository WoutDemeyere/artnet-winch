#include <SPI.h>
#include <Ethernet.h>
#include <EthernetUdp.h>
#include <Encoder.h>

#define short_get_high_byte(x) ((HIGH_BYTE & x) >> 8)
#define short_get_low_byte(x)  (LOW_BYTE & x)
#define bytes_to_short(h,l) ( ((h << 8) & 0xff00) | (l & 0x00FF) );



// ----- Artnet config
boolean is_artnet = false;

boolean OpCode_ArtPoll = false;
boolean OpCode_ArtPollReply = false;
boolean OpCode_DMX = false;
boolean OpCode_RDM = false;

byte dmx_buffer[512];


byte mac[] = {0xA8, 0x61, 0x0A, 0xAE, 0x4F, 0xDD} ;
IPAddress ip(169, 254, 10, 50);

unsigned int localPort = 6454;

byte remoteIp[4];
unsigned int remotePort;

const int MAX_BUFFER_UDP = 768;
char packetBuffer[MAX_BUFFER_UDP];


const int max_packet_size = 576;
const int art_net_header_size = 17;

byte ArtPollReply_Buffer[240];
byte ArtDMX_Buffer[300];

long ArtDMX_Bufer[900];

char ArtNetHead[7] = "Art-Net";
char short_name[18] = "TAKEL SPCMKRS 0001";
char long_name[64] = "YEAH FAM IDK A LONG NAME INIT";

char OpHbyteReceive = 0;
char OpLbyteReceive = 0;

short rec_uni = 0;
short Opcode = 0;

short pos_chan = 1;

byte up_chan = 50;
byte down_chan = 51;

byte set_start_chan = 40;
byte set_end_chan = 41;

byte set_zero_chan = 30;

byte set_art_vals_chan = 69;
byte set_art_vals_MSB_chan = 70;
byte set_art_vals_LSB_chan = 71;

byte set_art_vals_SUB_chan = 72;
byte set_art_vals_UNI_chan = 73;

byte universe = 0;
byte subnet = 0;

IPAddress remote;


EthernetUDP Udp;

// ----- Motor config

const byte pwm_pin = 5;
const byte dir_pin = 7;

const byte encA_pin = 3;
const byte encB_pin = 2;

Encoder myEnc(encB_pin, encA_pin);

const int TIME = 35;

int Speed = 0;
int dir = 1;

unsigned int temp_pos;

unsigned int get_val;

boolean change;

int oldPosition  = -999;

long int start_position = 0;
long int end_position = 0;

// ----  Other stuf
boolean move_up = false;
boolean move_down = false;

volatile long int encoder_pos = 0;

byte limit_pin = 8;

bool limit_reached = false;



void setup() {
  Serial.begin(9600);

  pinMode(pwm_pin, OUTPUT);
  pinMode(dir_pin, OUTPUT);

  pinMode(encA_pin, INPUT_PULLUP);
  pinMode(encB_pin, INPUT_PULLUP);

  pinMode(limit_pin, INPUT);

  attachInterrupt(digitalPinToInterrupt(3), encoder, RISING);

  start_udp();

}

void encoder() {
  if (digitalRead(2) == HIGH) {
    encoder_pos--;
  } else {
    encoder_pos++;
  }
}

void loop() {
  limit_reached = digitalRead(limit_pin);

  read_udp();

  check_setup();

  check_ArtPoll();

  Serial.print("Encoder pos: ");
  Serial.print(encoder_pos);
  Serial.print('\t');
  //Serial.println();

  temp_pos = get_val;

  get_val = read_dmx_channel(subnet, universe, pos_chan);

  /*Serial.print("DMX val: ");
    Serial.print(get_val);
    Serial.print('\t');*/
  move_takel(get_val);


  Serial.print("Pos: ");
  Serial.print(encoder_pos);

  Serial.println();

}

void start_udp() {
  Ethernet.begin(mac, ip);
  Udp.begin(localPort);
}

void read_udp() {
  int packetSize = Udp.parsePacket();

  remote = Udp.remoteIP();
  remotePort = Udp.remotePort();
  Udp.read(packetBuffer, MAX_BUFFER_UDP);

  is_artnet = true;

  for (int i = 0; i < 7; i++) {
    if (char(packetBuffer[i]) != ArtNetHead[i]) {
      is_artnet = 0;
      //Serial.println("ERR IN HEADER");
      break;
    }
  }

  if (is_artnet) {
    Opcode = bytes_to_short(packetBuffer[9], packetBuffer[8]);

    if (Opcode == 0x5000) {
      OpCode_DMX = true; OpCode_ArtPoll = false; OpCode_ArtPollReply = false; OpCode_RDM = false;
    }

    if (Opcode == 0x2000) {
      OpCode_DMX = false; OpCode_ArtPoll = true; OpCode_ArtPollReply = false; OpCode_RDM = false;
    }
  }
}

void check_ArtPoll() {
  if (OpCode_ArtPoll) {
    Serial.println("Received Poll");
    encode_ArtPollReply();
    delay(40);
  }

  OpCode_ArtPoll = false;
}

void encode_ArtPollReply() {
  for (int i = 0; i < 7; i++) {
    ArtPollReply_Buffer[i] = ArtNetHead[i];
  }

  ArtPollReply_Buffer[8] = 0x00;
  ArtPollReply_Buffer[9] = 0x21;

  for (byte i = 14; i < 25; i++) {
    ArtPollReply_Buffer[i] = 0x00;
  }

  for (byte i = 26; i < 44; i++) {
    ArtPollReply_Buffer[i] = short_name[i];
  }

  for (byte i = 44; i < 108; i++) {
    ArtPollReply_Buffer[i] = long_name[i];
  }

  for (byte i = 108; i < 200; i++) {
    ArtPollReply_Buffer[i] = 0x00;
  }

  for (byte i = 201; i < 207; i++) {
    ArtPollReply_Buffer[i] = 0x00;
  }

  for (byte i = 207; i <= 213; i++) {
    ArtPollReply_Buffer[i] = 0x00;
  }

  Udp.beginPacket(remote, remotePort);
  Udp.write(ArtPollReply_Buffer, 240);
  Udp.endPacket();
}

void send_dmx_channel(short sub, short uni, short chan, short val) {
  for (byte i = 0; i < 7; i++) {
    ArtDMX_Buffer[i] = ArtNetHead[i];
  }

  ArtDMX_Buffer[8] = 0x00;
  ArtDMX_Buffer[9] = 0x50;

  ArtDMX_Buffer[10] = 0;
  ArtDMX_Buffer[11] = 14;

  ArtDMX_Buffer[12] = 0;

  ArtDMX_Buffer[13] = 0;

  ArtDMX_Buffer[14] = 0;

  ArtDMX_Buffer[15] = 0;

  ArtDMX_Buffer[16] = 0x20;
  ArtDMX_Buffer[17] = 0x0;

  for (int i = 18; i < 300; i++) {
    if (i == chan) {
      ArtDMX_Buffer[i] = val;
    }
  }

  Udp.beginPacket(remote, remotePort);
  Udp.write(ArtDMX_Buffer, 530);
  Udp.endPacket();
}


void read_dmx_packet(short sub, short uni) {
  //short sel_uni = ((sub * 16) + uni);
  if (OpCode_DMX) {
    //rec_uni = bytes_to_short(packetBuffer[15], packetBuffer[14])

    short rec_sub = packetBuffer[14] & 0xF0;
    short rec_uni = packetBuffer[14] & 0x0F;

    if (rec_uni == uni && rec_sub == sub) {
      for (int i = 0; i < 512; i++) {
        dmx_buffer[i] = byte(packetBuffer[i + art_net_header_size + 1]);
      }
    }
  }
}

int read_dmx_channel(short sub, short uni, short channel) {
  //short sel_uni = ((sub * 16) + uni);
  if (OpCode_DMX) {
    short rec_sub = packetBuffer[14];// & 0xF0;
    short rec_uni = packetBuffer[15];// & 0x0F;

    if (rec_uni == uni && rec_sub == sub) {
      for (int i = 0; i < 512; i++) {
        if (i == channel) {
          return byte(packetBuffer[i + art_net_header_size + 1]);
        }
      }
    }
  }
}

void check_setup() {

  byte set_start = read_dmx_channel(0, 1, set_start_chan);

  byte set_end = read_dmx_channel(0, 1, set_end_chan);

  byte set_zero = read_dmx_channel(0, 1, set_zero_chan);

  byte set_art_vals = read_dmx_channel(0, 1, set_art_vals_chan);




  if (set_zero == 56) {
    encoder_pos = 0;
  }

  if (set_start == 56) {
    start_position = encoder_pos;

    byte byte1 = start_position & 0xF000;
    byte byte2 = start_position & 0x0F00;
    byte byte3 = start_position & 0x00F0;
    byte byte4 = start_position & 0x000F;
    
    send_dmx_channel(0, 0, 80, byte1);
    send_dmx_channel(0, 0, 81, byte2);
    send_dmx_channel(0, 0, 82, byte3);
    send_dmx_channel(0, 0, 83, byte4);
  }

  if (set_end == 56) {
    end_position = encoder_pos;
    //send_dmx_channel(0, 0, 81, 56);
  }

  if (set_art_vals == 56) {
    Serial.println("Setting Artnet Values");
    byte MSB = read_dmx_channel(0, 1, set_art_vals_MSB_chan);
    //int LSB = read_dmx_channel(0, 0, set_art_vals_LSB_chan);

    subnet = read_dmx_channel(0, 1, set_art_vals_SUB_chan);
    universe = read_dmx_channel(0, 1, set_art_vals_UNI_chan);

    //int channel = (MSB << 8) || LSB;

    Serial.print(MSB);
    Serial.print('\t');
    pos_chan = MSB;
  }
}

void move_takel(int val) {

  byte up_val = read_dmx_channel(0, 1, up_chan);
  byte down_val = read_dmx_channel(0, 1, down_chan);

  if (down_val == 56) {
    move_up = false;
    move_down = true;
  } else if (down_val != 56) {
    move_down = false;
  }

  if (up_val == 56) {
    move_up = true;
    move_down = false;
  } else if (up_val != 56) {
    move_up = false;
  }

  if (temp_pos != get_val && !move_down && !move_up) {
    change = true;
  }

  int mapped_pos = map(get_val, 0, 255, end_position, start_position);

  Serial.print("Mapped pos: ");
  Serial.print(mapped_pos);
  Serial.print('\t');

  Serial.print("Start position: ");
  Serial.print(start_position);
  Serial.print('\t');

  Serial.print("End position: ");
  Serial.print(end_position);
  Serial.print('\t');

  if (change == true && !move_down && !move_up) {

    if (encoder_pos >= mapped_pos) {

      turn(0, 127);

      delay(TIME);

      if (encoder_pos <= mapped_pos) {
        change = false;
        turn(0, 0);
      }

    } else if (encoder_pos <= mapped_pos) {

      turn(1, 127);

      delay(TIME);

      if (encoder_pos >= mapped_pos) {
        change = false;
        turn(1, 0);
      }

    }
  } else if (move_up && !move_down) {
    turn(0, 195);
  } else if (!move_up && move_down) {
    turn(1, 127);
  } else if (!change && !move_down && !move_up) {
    turn(0, 0);
  }
}

void turn(byte dir, byte spd) {
  analogWrite(pwm_pin, spd);
  digitalWrite(dir_pin, dir);
}
