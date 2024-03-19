import socket
import random
import string
import hashlib

def is_prime(n):
    """Check if a number is prime."""
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    max_divisor = int(n ** 0.5) + 1
    for d in range(3, max_divisor, 2):
        if n % d == 0:
            return False
    return True

def generate_random_prime(min_value, max_value):
    """Generate a random prime number within a specified range."""
    while True:
        candidate = random.randint(min_value, max_value)
        if is_prime(candidate):
            return candidate

def generate_public_values():
    # generates public values
    p = generate_random_prime(2,10000000)
    q = generate_random_prime(2,10000000)
    a = int( (p - 1) // q )
    # generate value of h
    h = random.randint(2, p-2)
    g = pow(h, a, p)  
    return (p,q,a,g)


def find_hash(m: string, q: int):
          
    # to bytes
    m = str.encode(m)
         
    hash_value = hashlib.sha1(m).digest()
    # Convert the hash value to an integer
    return int.from_bytes(hash_value, 'big') % q

def sign(q, p, g, x, H):
    k = random.randint(1, q-1)
    
    r = pow(g, k, p) % q
    s = ( pow(k, -1, q) * (H + x * r) ) % q
    return (r, s)



if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 12345))
    print('Connected to server')
    # get the message from the user
    message = input('Enter the message: ')
    # generate public values
    (p,q,a,g) = generate_public_values()
    # generate public values
    print("P: %d, Q: %d, A: %d, G: %d" % (p,q,a,g))
    # generate keys
    private_key = random.randint(1, q-1)
    public_key = pow(g, private_key, p)
    print("Public key: %d" % public_key)
    pub = str(p)+","+str(q)+","+str(a)+","+str(g)+","+str(public_key)
    # send the public values to the server
    s.sendall(pub.encode('utf-8'))    
    # find the hash
    hash_value = find_hash(message, q)
    # sign the message
    signature = sign(q, p, g, private_key, hash_value)
    data = message + "," + str(signature[0]) + "," + str(signature[1])
    # send the message and signature to the server
    s.sendall(data.encode('utf-8'))
    # modify the signature slightly
    signature = (signature[0]+ random.randint(1,1000), signature[1])
    print('Modified signature: ', signature)
    # try to verify the signature again
    data = message + "," + str(signature[0]) + "," + str(signature[1])
    s.sendall(data.encode('utf-8'))
    
    
    
    