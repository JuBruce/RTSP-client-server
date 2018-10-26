#Client controller file
from socket import *
import sys

arg_list = sys.argv
if len(arg_list) != 4:
    print('Usage: python3 control-client.py <server-ip> <server-port> <receiver-port>')

server_ip = arg_list[1]
server_port = int(arg_list[2])
receiver_port = int(arg_list[3])

print('Type SETUP to initiate a TCP connection with server.')
print('After SETUP type PLAY or PAUSE at anytime.')

user_cmd = input()
user_cmd = user_cmd.upper()

#gets what data the client wants from the server
def get_sensor_data():
    print('Input what reading you would like displayed.')
    print('79 for Oxygen, 84 for temperature, 80 for pressure, or * for All')
    print('example inputs: 79,84 or 80 or *')
    sensor_data = input()
    sensor_data_check = sensor_data.split(',')
    for each in sensor_data_check:
        if each == '79' or each == '84' or each == '80' or each == '*':
            sensor_data_msg = sensor_data
        else:
            print('Invalid input')
            sensor_data_msg =''
    return sensor_data_msg


if user_cmd == 'SETUP':
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_ip,server_port))
    sensor_msg = get_sensor_data()
    while sensor_msg == '':
        sensor_msg = get_sensor_data()

    setup_msg = 'SETUP rtsp://'+server_ip+'/RTSP/2.0 \nCSeq: 302 \nTransport: UDP;unicast;dest_addr":4588" \nSensor: '+sensor_msg
    client_socket.send(setup_msg.encode())

while True:
    user_cmd = input()
    user_cmd = user_cmd.upper()

if user_cmd == 'PLAY':
    print('play')
elif user_cmd == 'PAUSE':
    print('pause')
else:
    print('Unknow command')
