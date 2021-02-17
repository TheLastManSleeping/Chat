import hashlib
import socket
import threading

msgs = []


def receive(udp_ip, udp_port_1, udp_port_2, last_chat=''):
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_DGRAM)
    sock.bind((udp_ip, udp_port_1))
    while True:
        data, addr = sock.recvfrom(1024)
        text = str(data)[2:-1]
        if text[:3] == 'id:':
            if last_chat == text[3:]:
                for i in msgs:
                    send(UDP_IP, udp_port_2, i.encode('ascii'))
            else:
                msgs.clear()
                last_chat = text[3:]
        elif text == 'id_request':
            send(UDP_IP, udp_port_2, ('id:' + hashlib.sha384(name.encode('ascii')).hexdigest()).encode('ascii'))
        else:
            msgs.append(text)
            print("%s" % text)


def send(udp_ip, udp_port_2, message):
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_DGRAM)
    sock.sendto(message, (udp_ip, udp_port_2))


UDP_IP = "127.0.0.1"
UDP_TESTPORT_1 = 5004
UDP_TESTPORT_2 = 5005
MESSAGE = "Hello, World!"

print('Enter name:')
name = str(input())

t1 = threading.Thread(target=receive, args=(UDP_IP, UDP_TESTPORT_1, UDP_TESTPORT_2))
t1.start()

send(UDP_IP, UDP_TESTPORT_2, ('id:' + hashlib.sha384(name.encode('ascii')).hexdigest()).encode('ascii'))
send(UDP_IP, UDP_TESTPORT_2, 'id_request'.encode('ascii'))

while True:
    MESSAGE = (name + ": " + input()).encode('ascii')
    t2 = threading.Thread(target=send, args=(UDP_IP, UDP_TESTPORT_1, MESSAGE))
    t2.start()
    t2.join()
    t2 = threading.Thread(target=send, args=(UDP_IP, UDP_TESTPORT_2, MESSAGE))
    t2.start()
    t2.join()

