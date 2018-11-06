
import re
def validate(usr_input):
    usr_input = usr_input.lower()
    if usr_input.startswith('setup'):
        u_input = usr_input.split('\n')
        cmd = u_input[0]
        sequence_line = u_input[1]
        transport_line = u_input[2]
        sensor_line = u_input[3]
        cmd = cmd.split('/')

        if cmd[0] != 'setup rtsp:':
            return False
        if cmd[3] != 'rtsp':
            return False
        if cmd[4] != '2.0':
            return False
        
        return True
    elif usr_input.startswith('play'):
        u_input = usr_input.split('\n')
        cmd = u_input[0]
        cmd = cmd.split('/')
        sequence_line = u_input[1]
        sensor_line = u_input[2]
        if cmd[0] != 'play rtsp:':
            return False
        if cmd[3] != 'rtsp':
            return False
        if cmd[4] != '2.0':
            return False
        return True
    elif usr_input.startswith('pause'):
        u_input = usr_input.split('\n')
        cmd = u_input[0].split('/')
        if cmd[0] != 'pause rtsp:':
            return False
        if cmd[3] != 'rtsp':
            return False
        if cmd[4] != '2.0':
            return False
        return True
    else:
        print('Validation: invalid command request')
        return False
    
