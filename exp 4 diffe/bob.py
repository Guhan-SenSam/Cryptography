import socket
import secrets

P = 225
G = 14

def receiver():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 5200))

        b = secrets.randbelow(P - 1)  # Receiver's private key
        B = pow(G, b, P)  # Receiver's public key

        print("Sending public key B:", B)

        # Receive sender's public key (A)
        A_bytes = s.recv(2048)  # Adjust buffer size based on p's bit length
        A = int.from_bytes(A_bytes, byteorder='big')

        # Send public key (g^b) to sender
        s.sendall(B.to_bytes((P.bit_length() + 7) // 8, byteorder='big'))

        print("Alice's Fake generated public key: ", A)


if __name__ == '__main__':
    receiver()
