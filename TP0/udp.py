import socket
import struct

def send_message(sock, server_address, message):
    # Send the message to the server
    sock.sendto(message, server_address)

    # Receive the response from the server
    data, server = sock.recvfrom(4096)
    return data

def itr(sock, server_address, id, nonce):
    # Create the message for Individual Token Request
    message = struct.pack('!H12si', 1, id.encode('ascii'), nonce)
    return send_message(sock, server_address, message)

def itv(sock, server_address, sas):
    # Create the message for Individual Token Validation
    id, nonce, token = sas.split(':')
    message = struct.pack('!H12si64s', 3, id.encode('ascii'), int(nonce), token.encode('ascii'))
    return send_message(sock, server_address, message)

def gtr(sock, server_address, sas_list):
    # Create the message for Group Token Request
    message = struct.pack('!H', 5)
    message += struct.pack('!H', len(sas_list))
    for sas in sas_list:
        id, nonce, token = sas.split(':')
        message += struct.pack('!12si64s', id.encode('ascii'), int(nonce), token.encode('ascii'))
    return send_message(sock, server_address, message)

def gtv(sock, server_address, gas):
    # Create the message for Group Token Validation
    sas_list, token = gas.split('+')
    message = struct.pack('!H', 7)
    message += struct.pack('!H', len(sas_list))
    for sas in sas_list:
        id, nonce, token = sas.split(':')
        message += struct.pack('!12si64s', id.encode('ascii'), int(nonce), token.encode('ascii'))
    message += struct.pack('!64s', token.encode('ascii'))
    return send_message(sock, server_address, message)

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Server address
server_address = ('localhost', 12345)  # Replace with actual server address and port

# Student ID and nonce
student_id = 'YourNetID  '  # Fill in your NetID, pad with spaces to make it 12 characters
nonce = 1234  # Replace with your nonce

# Example usage
response = itr(sock, server_address, student_id, nonce)
print(response)

# Close the socket
sock.close()
