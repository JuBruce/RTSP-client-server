#Client controller file
from socket import *
import sys

arg_list = sys.argv
if len(arg_list) != 4:
    print('Usage: python3 control-client.py <server-ip> <server-port> <receiver-port>')
    sys.exit(0)
server_ip = arg_list[1]
server_port = int(arg_list[2])
receiver_port = arg_list[3]

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

    setup_msg = ('SETUP rtsp://'+server_ip+'/RTSP/2.0\n' +
    'CSeq: 302\nTransport: UDP;unicast;dest_addr:'+receiver_port+'\n' +
    'Sensor:' + sensor_msg)
    client_socket.send(setup_msg.encode())
state =''
while True:
    user_cmd = input()
    user_cmd = user_cmd.upper()
    if user_cmd == 'PLAY':
        state = 'play'
        print('play')
        sensor_msg = get_sensor_data()
        while sensor_msg == '':
            sensor_msg = get_sensor_data()
        play_msg = ('PLAY rtsp://' + server_ip + '/RTSP/2.0\n' +
        'CSeq: 836\n' +
        'Sensor:' + sensor_msg)
        client_socket.send(play_msg.encode())
    elif user_cmd == 'PAUSE':
        state = 'pause'
        print('pause')
        pause_msg = ('PAUSE rtsp://' + server_ip + '/RTSP/2.0\n' +
        'CSeq: 834')
        client_socket.send(pause_msg.encode())
    elif user_cmd == 'SETUP':
        print('TCP connection has already been established.')
    elif user_cmd == 'TEARDOWN':
        print('Ending session')
        teardown_msg = ('TEARDOWN rtsp://' + server_ip + '/RTSP/2.0\n' +
        'CSeq: 892')
        client_socket.send(teardown_msg.encode())
        sys.exit()
    else:
        print('No dice, unknown command.')
