import socket
import secrets

P = 350
G = 10


def sender():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 4200))

        a = secrets.randbelow(P - 1)  # Sender's private key
        A = pow(G, a, P)  # Sender's public key

        print("Sending public key A:", A)

        # Send public key (g^a) to receiver
        s.sendall(A.to_bytes((P.bit_length() + 7) // 8, byteorder='big'))

        # Receive receiver's public key (B)
        B_bytes = s.recv(2048)  # Adjust buffer size based on p's bit length
        B = int.from_bytes(B_bytes, byteorder='big')
        print("Bob's Fake generated public key: ", B)


if __name__ == '__main__':
    sender()
