#server file
from socket import *
import sys
from threading import *
import os
import _thread
from random import randint
from select import select
from time import sleep




arg_list = sys.argv
if len(arg_list) != 5:
    print('Usage: python3 server.py <server port> <oxygen_file.bin> <tempeture_file.bin> <pressure_file.bin>')
    sys.exit(0)

server_port = int(arg_list[1])
oxygen_file = arg_list[2]
tempeture_file = arg_list[3]
pressure_file = arg_list[4]

#make sure all file are .bin files
o_check = oxygen_file.split('.')
t_check = tempeture_file.split('.')
p_check = pressure_file.split('.')

if o_check[1] != 'bin' and t_check[1] != 'bin' and p_check[1] != 'bin':
    print('Usage: python3 server.py <server port> <oxygen_file.bin> <tempeture_file.bin> <pressure_file.bin>')
    print('All files must be bin files')
    sys.exit(0)

f_oxyegen = open(oxygen_file, 'rb')
f_pressure = open(pressure_file,'rb')
f_temp = open(tempeture_file, 'rb')
# get_data reads in from each .bin file
oxygen_level = ''
temp_level = ''
pressure_level = ''
def get_data():
    global oxygen_level
    global temp_level
    global pressure_level
    while True:
        sleep(3)
        ######## 
        #Oxygen bit collection
        ########
        # read one byte
        byte = f_oxyegen.read(1)
        # convert the byte to an integer representation
        byte = ord(byte)
        # now convert to string of 1s and 0s
        oxygen_level = '79:' + bin(byte)[5:].rjust(5, '0')
        
        

        ##########
        #pressure bit collection
        ##########
        byte = f_pressure.read(1)
        byte = ord(byte)
        byte = bin(byte)[2:].rjust(8, '0')
        l = list(byte)
        byte = f_pressure.read(1)
        byte = ord(byte)
        byte = bin(byte)[2:].rjust(8,'0')
        l = l+list(byte)
        l = ''.join(l[5:])
        pressure_level = '80:'+l

        

        #########
        #temp bit collection
        #########
        byte = f_temp.read(1)
        byte = ord(byte)
        byte = bin(byte)[2:].rjust(8,'0')
        temp_level = '84:' + byte




#reads in data from control client
def clientthread(conn,port):
    receiver_port = ''
    sentence = conn.recv(1024).decode()
    cmd = sentence.split('\n')
    cmd = cmd[0]
    cmd = cmd.split(' ')
    print(cmd[0])
    conn.setblocking(0)
    while True:
        try:
            data = conn.recv(1024)
            print(data)
            sentence = data.decode()
        except BlockingIOError:
            pass
        if sentence.startswith('SETUP'):
            user_input = sentence.split('\n')
            setup_line = user_input[0]
            seq_line = user_input[1]
            transport_line = user_input[2]
            sensor_line = user_input[3]
            rcv = transport_line.split(":")
            sleep(3)
            print(oxygen_level + ';' + temp_level + ';' + pressure_level)

        elif sentence.startswith('PLAY'):
            print("play")
            sleep(3)
            print(oxygen_level + ';' + temp_level + ';' +pressure_level)
        elif sentence.startswith('PAUSE'):
            print('pause')
        # while play == True:
        #     levels = get_data()
        #     #send over udp
        #     while pause == True:
        #         pass

_thread.start_new_thread(get_data,())
#setup for TCP connection
tcp = socket(AF_INET, SOCK_STREAM)
tcp.bind(('',server_port))
tcp.listen(5)

input = [tcp]
while True:
    inputready,outputready,exceptready = select(input,[],[])

    for s in inputready:
        if s == tcp:
            conn, addr = tcp.accept()
            _thread.start_new_thread(clientthread,(conn,server_port))

        else:
            print ("unknown socket:", s)