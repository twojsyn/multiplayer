import random
import pickle
import socket
from _thread import *
from player import Player
from constants import *

# Tworzenie gniazda sieciowego (socket) z rodzajem AF_INET (IPv4) i typem SOCK_STREAM (TCP)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Próba powiązania gniazda z adresem IP serwera i portem
try:
    s.bind((SERVER, PORT))

except socket.error as e:
    str(e)

# Nasłuchiwanie połączeń przychodzących z maksymalnie 2 klientami
s.listen(10)
print("Waiting for a connection, server Started")

players = []


# Definicja funkcji obsługującej klienta
def threaded_client(conn, player_number):
    # Wysłanie informacji o nawiązaniu połączenia z klientem
    conn.send(pickle.dumps(players[player_number]))

    reply = ""
    while True:
        try:
            # Odczytanie danych od klienta
            data = pickle.loads(conn.recv(2048))
            players[player_number] = data

            # Dekodowanie danych do formatu utf-8
            players[player_number] = data

            # Sprawdzenie, czy odebrano jakieś dane
            if not data:
                print("Disconnected")
                break
            else:
                reply = players

                # Wyświetlenie otrzymanych danych
                print(f"Received: {reply}")
                # Przesłanie tych samych danych z powrotem do klienta
                print(f"Sending: {reply}")

            conn.sendall(pickle.dumps(reply))
        except:
            break
    # Wyświetlenie komunikatu o utraceniu połączenia z klientem i zamknięcie połączenia

    print("Lost connection")
    try:
        players.pop(player_number)
    except:
        conn.close()

currentPlayer = 0
# Nieskończona pętla while, w której serwer przyjmuje nowych klientów i tworzy dla nich nowe wątki
while True:
    conn, addr = s.accept()
    print(f"Connected to: {addr}.")

    #Dodawanie nowego gracza
    randColor = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    players.append(Player(0, 60 * currentPlayer, 50, 50, randColor))

    start_new_thread(threaded_client, (conn,currentPlayer))
    currentPlayer += 1