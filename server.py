#server file
from socket import *
import sys
from threading import *
import os
import _thread
from random import randint
from select import select
from time import sleep
import server_validation


#######
#Server setup
#######
arg_list = sys.argv
if len(arg_list) != 5:
    print('Usage: python3 server.py <server port> <oxygen_file.bin> <tempeture_file.bin> <pressure_file.bin>')
    sys.exit(0)

#grab arg list
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

#open files
f_oxyegen = open(oxygen_file, 'rb')
f_pressure = open(pressure_file,'rb')
f_temp = open(tempeture_file, 'rb')

#Global variables that are get by get_data()
oxygen_level = ''
temp_level = ''
pressure_level = ''

#######
#continious read from bin files
#######
def get_data():
    global oxygen_level
    global temp_level
    global pressure_level

    while True:
        sleep(3)
        #Oxygen bit collection
        byte = f_oxyegen.read(1)
        #convert byte to int
        byte = ord(byte) 
        #convert into to a bit array and drop unused bits
        #and put it into a string
        oxygen_level = '79:' + bin(byte)[5:].rjust(5, '0') 
        
        #pressure bit collection
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

        #temp bit collection
        byte = f_temp.read(1)
        byte = ord(byte)
        byte = bin(byte)[2:].rjust(8,'0')
        temp_level = '84:' + byte


#reads in data from control client
def clientthread(conn,port,addr):
    receiver_port = ''
    udp = socket(AF_INET,SOCK_DGRAM)


    while True:
        user_input = conn.recv(1024)
        user_input = user_input.decode()
        validate = server_validation.validate(user_input)
        if validate == True:
            break

    conn.setblocking(0)

    while True:
        try:
            data = conn.recv(1024)
            print(data)
            if data:
                user_input = data.decode()
        except BlockingIOError:
            pass
        if user_input.startswith('SETUP'):
            u_input = user_input.split('\n')
            setup_line = u_input[0]
            seq_line = u_input[1]
            transport_line = u_input[2]
            transport_line_array = transport_line.split(':')
            udp_port = int(transport_line_array[2])
            sensor_line = u_input[3]
            rcv = transport_line.split(":")
            sleep(3)
            sensor_line = sensor_line.split(':')
            requested_stream = sensor_line[1].split(',')
            requested = []
            for each in requested_stream:
                requested.append(each)
            
            responce = ''
            requested.sort()
            
            for each in requested:   
                if each == '79':
                    responce = responce + oxygen_level + '; '
                if each == '84':
                    responce = responce + temp_level + '; '
                if each == '80':
                    responce = responce + pressure_level + '; '
                if each == '*':
                    responce = (oxygen_level + ';' + temp_level + ';' + pressure_level)
                    break

            udp.sendto(responce.encode(), (addr[0],udp_port))
        elif user_input.startswith('PLAY'):
            u_input = user_input.split('\n')
            sensor_line = u_input[2].split(':')
            requested_stream = sensor_line[1].split(',')
            sleep(3)
            requested = []
            for each in requested_stream:
                requested.append(each)
            responce = ''
            requested.sort()
            for each in requested:
                if each == '79':
                    responce = responce + oxygen_level + '; '
                if each == '84':
                    responce = responce + temp_level + '; '
                if each == '80':
                    responce = responce + pressure_level + '; '
                if each == '*':
                    responce = (oxygen_level + ';' + temp_level + ';' + pressure_level)
                    break

            udp.sendto(responce.encode(), (addr[0],udp_port))

        elif user_input.startswith('PAUSE'):
            pass
        elif user_input.startswith('TEARDOWN'):
            responce = 'Teardown called closing connection.'
            udp.sendto(responce.encode(), (addr[0],udp_port))
            conn.close()
            break


            


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
            print(addr)
            _thread.start_new_thread(clientthread,(conn,server_port,addr))
            
        else:
            print ("unknown socket:", s)