from serial import Serial
import socket
import pickle


def invert_channel(value):
    return 3000 - value


def shrink_channel(value, scale):
    return 1500 + (value - 1500) / scale


def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def clamp(x, in_min, in_max):
    return max(in_min, min(x, in_max))


# establish wireless connect to onboard RaspberryPi
wireless_ip = "10.0.0.2"
routered_ip = "192.168.1.2"

serverAddressPort = (routered_ip, 20001)

bufferSize = 128

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# establish serial connection to Arduino
# reading inputs from GoBilda transmitter
ser = Serial('/dev/cu.usbmodem144401', 115200)

print(ser.name)

if ser.is_open:
    while True:
        values = ser.readline()
        channels = values.split()

        if len(channels) < 6:
            continue

        L_X = int(channels[3])
        L_Y = invert_channel(int(channels[2]))
        R_X = invert_channel(int(channels[0]))
        R_Y = int(channels[1])

        if abs(int(channels[4]) - 2000) < 100:
            SWITCH = "LO"
        elif abs(int(channels[4]) - 1500) < 100:
            SWITCH = "MID"
        elif abs(int(channels[4]) - 1000) < 100:
            SWITCH = "HI"
        else:
            SWITCH = None

        DIAL = int(channels[5])

        # print("L_X {} L_Y {} R_X {} R_Y {} SWITCH {} DIAL {}"
        #       .format(L_X, L_Y, R_X, R_Y, SWITCH, DIAL))

        # forward = R_Y
        # strafe = R_X
        # turn = L_X
        # altitude = L_Y

        forward = R_Y
        strafe = L_X
        turn = R_X
        altitude = L_Y

        speed_modifier = {"LO": 3, "MID": 2, "HI": 1}

        M1 = forward - strafe - shrink_channel(turn, 2) + 3000
        M2 = forward + strafe + shrink_channel(turn, 2) - 3000
        M3 = forward + strafe - shrink_channel(turn, 2)
        M4 = forward - strafe + shrink_channel(turn, 2)
        M5 = altitude
        M6 = altitude
        S1 = DIAL

        M1 = clamp(M1, 1000, 2000)
        M2 = clamp(M2, 1000, 2000)
        M3 = clamp(M3, 1000, 2000)
        M4 = clamp(M4, 1000, 2000)
        M5 = clamp(M5, 1000, 2000)
        M6 = clamp(M6, 1000, 2000)
        S1 = clamp(S1, 1000, 2000)

        M1 = shrink_channel(M1, speed_modifier[SWITCH])
        M2 = shrink_channel(M2, speed_modifier[SWITCH])
        M3 = shrink_channel(M3, speed_modifier[SWITCH])
        M4 = shrink_channel(M4, speed_modifier[SWITCH])

        M1 = map_value(M1, 1000, 2000, 1100, 1900)
        M2 = map_value(M2, 1000, 2000, 1100, 1900)
        M3 = map_value(M3, 1000, 2000, 1100, 1900)
        M4 = map_value(M4, 1000, 2000, 1900, 1100)
        M5 = map_value(M5, 1000, 2000, 1100, 1900)
        M6 = map_value(M6, 1000, 2000, 1100, 1900)

        send_message = pickle.dumps([M1, M2, M3, M4,
                                     M5, M6, 0, 0,
                                     0, 0, 0, 0,
                                     0, 0, 0, S1])

        UDPClientSocket.sendto(send_message, serverAddressPort)

        print("M1 = {:5} \t M2 = {:5} \t M3 = {:5} \t M4 = {:5} \t M5 = {:5} \t M6 = {:5} \t S1 = {:5}"
              .format(M1, M2, M3, M4, M5, M6, S1))

ser.close()
