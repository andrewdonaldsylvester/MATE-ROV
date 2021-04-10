import socket
import time
import pickle
import pygame

# M1-----M2
# |      |
# |      |
# M3-----M4

# M1, M4 /
# M2, M3 \

pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()


def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def clamp(x, in_min, in_max):
    return max(in_min, min(x, in_max))


msgFromClient = "Hello UDP Server"

bytesToSend = str.encode(msgFromClient)

wireless_ip = "10.0.0.2"
routered_ip = "192.168.1.2"

serverAddressPort = (routered_ip, 20001)

bufferSize = 128

# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket

while True:
    pygame.event.get()

    L_X = round(100 * joystick.get_axis(0)) / 100
    L_Y = round(100 * joystick.get_axis(1)) / 100
    R_X = round(100 * joystick.get_axis(2)) / 100
    R_Y = round(100 * joystick.get_axis(5)) / 100
    L_T = round(100 * joystick.get_axis(3)) / 100
    R_T = round(100 * joystick.get_axis(4)) / 100

    L_X_PWM = map_value(L_X, -1, 1, 1000, 2000)
    L_Y_PWM = map_value(L_Y, 1, -1, 1000, 2000)
    R_X_PWM = map_value(R_X, -1, 1, 1000, 2000)
    R_Y_PWM = map_value(R_Y, 1, -1, 1000, 2000)
    L_T_PWM = map_value(L_T, -1, 1, 1000, 2000)
    R_T_PWM = map_value(R_T, -1, 1, 1000, 2000)

    M1 = L_Y_PWM + L_X_PWM + R_X_PWM - 3000
    M2 = L_Y_PWM - L_X_PWM - R_X_PWM + 3000
    M3 = L_Y_PWM - L_X_PWM + R_X_PWM
    M4 = L_Y_PWM + L_X_PWM - R_X_PWM
    M5 = 3000 - R_Y_PWM - 200*joystick.get_hat(0)[0]
    M6 = 3000 - R_Y_PWM + 200*joystick.get_hat(0)[0]
    S1 = L_T_PWM
    S2 = R_T_PWM

    M1 = clamp(M1, 1000, 2000)
    M2 = clamp(M2, 1000, 2000)
    M3 = clamp(M3, 1000, 2000)
    M4 = clamp(M4, 1000, 2000)
    M5 = clamp(M5, 1000, 2000)
    M6 = clamp(M6, 1000, 2000)
    S1 = clamp(S1, 1000, 2000)
    S2 = clamp(S2, 1000, 2000)

    M1 = map_value(M1, 1000, 2000, 1900, 1100)
    M2 = map_value(M2, 1000, 2000, 1900, 1100)
    M3 = map_value(M3, 1000, 2000, 1900, 1100)
    M4 = map_value(M4, 1000, 2000, 1900, 1100)
    M5 = map_value(M5, 1000, 2000, 1100, 1900)
    M6 = map_value(M6, 1000, 2000, 1100, 1900)
    S1 = map_value(S1, 1000, 2000, 2000, 1000)
    S2 = map_value(S2, 1000, 2000, 2000, 1000)

    send_message = pickle.dumps([M1, M2, M3, M4,
                                 0,  0,  M5, M6,
                                 0,  0,  S1, S2,
                                 0,  0,  0,  0])

    UDPClientSocket.sendto(send_message, serverAddressPort)
    # msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    time.sleep(0.1)

    print("M1 = {:5} \t M2 = {:5} \t M3 = {:5} \t M4 = {:5} \t M5 = {:5} \t M6 = {:5} \t S1 = {:5} \t S2 = {:5}"
          .format(M1, M2, M3, M4, M5, M6, S1, S2))

