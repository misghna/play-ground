import socket

# Set up the UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.settimeout(2)
sock.sendto(
    b'M-SEARCH * HTTP/1.1\r\n'
    b'HOST: 239.255.255.250:1900\r\n'
    b'MAN: "ssdp:discover"\r\n'
    b'MX: 1\r\n'
    b'ST: ssdp:all\r\n'
    b'\r\n',
    ('239.255.255.250', 1900)
)

# Listen for responses
try:
    while True:
        data, addr = sock.recvfrom(1024)
        print(f'Received response from {addr}:\n{data.decode()}')
except socket.timeout:
    print('Discovery complete.')
