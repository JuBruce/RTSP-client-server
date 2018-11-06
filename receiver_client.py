from socket import *
import sys
import _thread
import os
from threading import *






arg_list = sys.argv
udp_listen_port = int(arg_list[1])

if len(arg_list) != 2:
    print('Usage: python3 recevier_client.py <udp_port>')

oxygen_bits = ''
temp_bits = ''
press_bits = ''

def UDP_connection(udp_listen_port):
    while True:
        message, address = udp.recvfrom(1024)
        decoded_message = message.decode()
        if decoded_message == 'Teardown called closing connection.':
            sys.exit()
        else:
            tagged_bits = decoded_message.split(';')
            oxygen_reading = ''
            temp_reading =''
            press_reading = ''
            for each in tagged_bits:
                reading = each.split(':')
                read = reading[0].strip()
                if read == '79':
                    oxygen_bits = reading[1]
                    oxygen_bits = int(oxygen_bits,2)
                    oxygen_bits = round(20.0*(oxygen_bits/31.0))
                    oxygen_reading = '79:'
                    i = 20
                    while oxygen_bits != 0:
                        oxygen_reading = oxygen_reading + '*'
                        oxygen_bits = oxygen_bits-1
                        i = i-1
                    while i != 0:
                        oxygen_reading = oxygen_reading + ' '
                        i = i-1
                    oxygen_reading = oxygen_reading +';'
                if read == '84':
                    temp_bits = reading[1]
                    temp_bits = int(temp_bits,2)
                    temp_bits = round(20.0*(temp_bits/255))
                    temp_reading = '84:'
                    i = 20
                    while temp_bits != 0:
                        temp_reading = temp_reading + '*'
                        temp_bits = temp_bits-1
                        i = i-1
                    while i != 0:
                        temp_reading = temp_reading + ' '
                        i = i-1
                    temp_reading = temp_reading +';'
                if read == '80':
                    press_bits = reading[1]
                    press_bits = int(press_bits,2)
                    press_bits = round(20.0*(press_bits/2047))
                    press_reading = '80:'
                    i = 20
                    while press_bits != 0:
                        press_reading = press_reading + '*'
                        press_bits = press_bits-1
                        i = i-1
                    while i != 0:
                        press_reading = press_reading + ' '
                        i = i-1
                    press_reading = press_reading +';'
            print(oxygen_reading +''+ temp_reading +''+ press_reading)





udp = socket(AF_INET, SOCK_DGRAM)
udp.bind(('',udp_listen_port))

udp_thread = Thread(target = UDP_connection(udp_listen_port))
