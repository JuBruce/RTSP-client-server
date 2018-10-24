#server file
from socket import *
import sys
from threading import *
import os
import _thread
from random import randint

########
#  Used for creation of random bin file
# directory = os.getcwd()
# ox_directory = os.path.join(directory+'oxygen.bin')
# temp_directory = os.path.join(directory+'temp.bin')
# pres_directory = os.path.join(directory+'pressure.bin')
# with open('pres_directoy', 'wb') as fout:
#     fout.write(os.urandom(2048)) 
########


######## why use 5 bits?
#Oxygen bit collection
########
# f = open("oxygen.bin", 'rb')
# # read one byte
# byte = f.read(1)
# # convert the byte to an integer representation
# byte = ord(byte)
# # now convert to string of 1s and 0s
# byte = bin(byte)[2:].rjust(8, '0')
# # now byte contains a string with 0s and 1s
# l = list(byte)
# level = ''.join(l[0:5])
# l = l[5:]
# print(int(level,2))
# while byte:
#     if len(l) > 5:
#         level = ''.join(l[0:5])
#         l = l[5:]
#         print(int(level,2))
#         pass
#     byte = f.read(1)
#     if len(byte) < 1:
#         break
#     else:
#         byte = ord(byte)
#         byte = bin(byte)[2:].rjust(8,'0')
#         l += list(byte)
#         level = ''.join(l[0:5])
#         l = l[5:]
#         print(int(level,2))


########## does trivia matter?
#pressure bit collection
##########
f = open('pres.bin','rb')
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
print(int(level,2))
while byte:
    if len(l) > 11:
        level = ''.join(l[0:11])
        l = l[11:]
        print(int(level,2))
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
            print(int(level,2))
            


#########
#temp bit collection
#########
# f = open('temp.bin', 'rb')
# byte = f.read(1)
# byte = int.from_bytes(byte,byteorder='big',signed=True)
# print(byte)
# while byte:
#     byte = f.read(1)
#     if len(byte) < 1:
#         break
#     else:
#         byte = int.from_bytes(byte,byteorder='big',signed=True)
#         print(byte)


