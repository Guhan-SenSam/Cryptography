# server code
from copy import deepcopy
import socket
import hashlib

p = 283
q = 47

def hash(m, q):          
    hash_value = hashlib.sha1(m).digest()
    # Convert the hash value to an integer
    return int.from_bytes(hash_value, 'big') % q

def verify_signature(p, q, g, y, r, s, H):
    # verify the signature
    w = pow(s, -1, q)
    u1 = (H * w) % q
    u2 = (r * w) % q
    v = ( pow(g, u1, p) * pow(y, u2, p) ) % p % q
    print('v:', v)
    print('r:', r)
    return v == r


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 12345))
    s.listen(1)
    conn, addr = s.accept()
    print('Connected by', addr)
    # receive the public values from the client
    data = conn.recv(1024).decode('utf-8')
    print('Received', data)
    # get the modified signature from the client
    mod_data = conn.recv(1024).decode('utf-8')
    print('Received modified Data', mod_data)
    # split the data
    data = data.split(',')
    p = int(data[0])
    q = int(data[1])
    a = int(data[2])
    g = int(data[3])
    se_public_key = int(data[4])
    # receive the message and signature from the client
    data = conn.recv(1024).decode('utf-8')
    print('Received', data)
    # hash the message
    message = data.split(',')[0]
    signature = (int(data.split(',')[1]), int(data.split(',')[2]))
    H = hash(message.encode('utf-8'), q)
    # verify the signature
    if verify_signature(p, q, g, se_public_key, signature[0], signature[1], H):
        print('Signature verified')
    else:
        print('Signature not verified')
    # verify the modified signature
    mod_signature = (int(mod_data.split(',')[1]), int(mod_data.split(',')[2]))
    if verify_signature(p, q, g, se_public_key, mod_signature[0], mod_signature[1], H):
        print('Modified signature verified')
    else:
        print('Modified signature not verified')
    
    
        