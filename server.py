#server file
from socket import *
import sys
from threading import *
import os
import _thread
from random import randint
from select import select

arg_list = sys.argv
if len(arg_list) != 5:
    print('Usage: python3 server.py <server port> <oxygen_file.bin> <tempeture_file.bin> <pressure_file.bin>')
    sys.exit(0)
server_port = int(arg_list[1])
oxygen_file = arg_list[2]
tempeture_file = arg_list[3]
pressure_file = arg_list[4]

o_check = oxygen_file.split('.')
t_check = tempeture_file.split('.')
p_check = pressure_file.split('.')

if o_check != 'bin' and t_check != 'bin' and p_check != 'bin':
    print('Usage: python3 server.py <server port> <oxygen_file.bin> <tempeture_file.bin> <pressure_file.bin>')
    print('All files must be bin files')
    sys.exit(0)
########
#  Used for creation of random bin file
# directory = os.getcwd()
# ox_directory = os.path.join(directory+'oxygen.bin')
# temp_directory = os.path.join(directory+'temp.bin')
# pres_directory = os.path.join(directory+'pressure.bin')
# with open('pres_directoy', 'wb') as fout:
#     fout.write(os.urandom(2048)) 
########

def get_data():
    ######## why use 5 bits?
    #Oxygen bit collection
    ########
    f = open(oxygen_file, 'rb')
    # read one byte
    byte = f.read(1)
    # convert the byte to an integer representation
    byte = ord(byte)
    # now convert to string of 1s and 0s
    byte = bin(byte)[2:].rjust(8, '0')
    # now byte contains a string with 0s and 1s
    l = list(byte)
    level = ''.join(l[0:5])
    l = l[5:]
    oxygen_level = int(level,2)
    while byte:
        if len(l) > 5:
            level = ''.join(l[0:5])
            l = l[5:]
            oxygen_level = int(level,2)
            pass
        byte = f.read(1)
        if len(byte) < 1:
            break
        else:
            byte = ord(byte)
            byte = bin(byte)[2:].rjust(8,'0')
            l += list(byte)
            level = ''.join(l[0:5])
            l = l[5:]
            oxygen_level = int(level,2)


    ########## does trivia matter?
    #pressure bit collection
    ##########
    f = open(pressure_file,'rb')
    byte = f.read(1)
    byte = ord(byte)
    byte = bin(byte)[2:].rjust(8, '0')
    l = list(byte)
    byte = f.read(1)
    byte = ord(byte)
    byte = bin(byte)[2:].rjust(8,'0')
    l = l+list(byte)
    level = ''.join(l[0:11])
    l = l[11:]
    pressure_level = int(level,2)
    while byte:
        if len(l) > 11:
            level = ''.join(l[0:11])
            l = l[11:]
            pressure_level = int(level,2)
            pass
        byte = f.read(1)
        if len(byte) < 1:
            break
        else:
            byte = f.read(1)
            byte = ord(byte)
            byte = bin(byte)[2:].rjust(8, '0')
            l = l + list(byte)
            byte = f.read(1)
            if len(byte) < 1:
                break 
            else:
                byte = ord(byte)
                byte = bin(byte)[2:].rjust(8,'0')
                l = l+list(byte)
                level = ''.join(l[0:11])
                l = l[11:]
                pressure_level = int(level,2)


    #########
    #temp bit collection
    #########
    f = open(tempeture_file, 'rb')
    byte = f.read(1)
    byte = int.from_bytes(byte,byteorder='big',signed=True)
    temp_level = byte
    while byte:
        byte = f.read(1)
        if len(byte) < 1:
            break
        else:
            byte = int.from_bytes(byte,byteorder='big',signed=True)
            temp_level = byte

    return oxygen_level, temp_level, pressure_level  

def clientthread():
    while play == True:
        levels = get_data()
        #send over udp
        while pause == True:
            pass


tcp = socket(AF_INET, SOCK_STREAM)
tcp.bind(('',server_port))
tcp.listen(5)

input = [tcp]
while True:
    inputready,outputready,exceptready = select(input,[],[])

    for s in inputready:
        if s == tcp:
            conn, addr = tcp.accept()
            _thread.start_new_thread(clientthread ,(conn,server_port))


        else:
            print ("unknown socket:", s)