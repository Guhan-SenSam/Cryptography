import socket
import threading
import secrets

P = 225
G = 14

def proxy_data(source, destination):
    while True:
        data = source.recv(1024)
        if not data:
            break
        
        c = secrets.randbelow(P - 1)
        C = pow(G, c, P)
        
        print(f"Sending Fake public key: ", C)
        # Send public key (g^b) to sender
        destination.sendall(C.to_bytes((P.bit_length() + 7) // 8, byteorder='big'))

def main():
    alice_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bob_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    alice_socket.bind(('localhost', 4200))
    bob_socket.bind(('localhost', 5200))
    alice_socket.listen(5)
    bob_socket.listen(5)
    alice_conn, alice_addr = alice_socket.accept()
    bob_conn, bob_addr = bob_socket.accept()
    print("Attacker connected to Alice and Bob.")

    # Using threads we can manage multiple connections at once
    t1 = threading.Thread(target=proxy_data, args=(alice_conn, bob_conn))
    t2 = threading.Thread(target=proxy_data, args=(bob_conn, alice_conn))
    t1.start()
    t2.start()

if __name__ == "__main__":
    main()
