#made by Louis Pierre 23317

import socket
import threading
import json


our_player_name = "LOUIS"
SERVER_IP = '192.168.129.62'
SERVER_PORT = 8888

on_right = True  #utiliser pour IA, ne pas changer

def am_i_first_player(state):
    #prend comme valeur entrée le dictionnaire state et revoie si on est le 1er joueur ou non
    list = state["players"]
    if list[0] == our_player_name:
        return True
    else:
        return False

def find_position(state):
    #permet de trouver la postion du joueur et de la restranscrir sur une grille 17X17.
    if am_i_first_player(state):
        number = int(0)
    else :
        number = int(1)
    
    board = state["board"]
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == number:
                return (j, i)

def find_other_position(state):
        #permet de trouver la postion de l'autre joueur et de la restranscrir sur une grille 17X17.
    if not am_i_first_player(state):
        number = int(0)
    else :
        number = int(1)
    
    board = state["board"]
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == number:
                return (j, i)

def what_is_this_box(state, position :tuple): 
    #permet de trouver ce qui se trouve dans le box, renverra un nombre qui permet de determiner ce qu'il se trouve
    #il faut imaginer une grille 17X17 et avec collone comme asisse et ligne ordonnée, le joueur 1 est en bas de la grille le joeur 2 au dessus
    #note: la grille commence avec la position (0,0), comme pour une matrice informatique
    board = state["board"]
    x, y = position
    x = x
    y = y
    return board[y][x]
    
def check_wall_up(state):
    #permet de verifier si un mur se trouve devant le joueur. 
    #par devant cela veut dire selon l'orientation du plateau
    #pour rappel le plateau est orienté tel que le joueur 1 est en bas et le joueur 1 est en haut
    #renvoie True si il n'y a pas de mur, False si il y a un mur
    board = state["board"]
    x,y = find_position(state)
    y = y+1
    if what_is_this_box(state,(x,y)) == 3:
        return True 
    elif what_is_this_box(state,(x,y)) == 4:
        return False
    else : 
        return False

def check_wall_right(state):
    #permet de verifier si un mur se trouve a droite du joeur. 
    #le droite n'est pas relatif au joeur mais bien au plateau
    #return False si il y un mur True si il y n'y en a pas
    board = state["board"]
    x,y = find_position(state)
    x = x+1
    if what_is_this_box(state,(x,y)) == 3:
        return True 
    elif what_is_this_box(state,(x,y)) == 4:
        return False
    else : 
        return False

def check_wall_left(state):
    #permet de verifier si un mur se trouve a gauche du joeur. 
    #le droite n'est pas relatif au joeur mais bien au plateau
    #return False si il y un mur True si il y n'y en a pas
    board = state["board"]
    x,y = find_position(state)
    x = x-1
    if what_is_this_box(state,(x,y)) == 3:
        return True 
    elif what_is_this_box(state,(x,y)) == 4:
        return False
    else : 
        return False

def check_wall_down(state):
    #permet de verifier si un mur se trouve en bas du joueur. 
    #par devant cela veut dire selon l'orientation du plateau
    #pour rappel le plateau est orienté tel que le joueur 1 est en bas et le joueur 1 est en haut
    board = state["board"]
    x,y = find_position(state)
    y = y-1
    if what_is_this_box(state,(x,y)) == 3:
        return True 
    elif what_is_this_box(state,(x,y)) == 4:
        return False
    else : 
        return False

def check_border_right(state):
    #regarde la position si le joeur se trouve en peripherie du plateau
    #cela le previendra de ne pas aller plus loin, sert a ne pas sortir des limites de celui-ci
    #revoie True si il n'est pas en peripherie droite False si non
    x,y = find_position(state)
    if x == 16:
        return False 
    else :
        return True

def check_border_left(state):
    #regarde la position si le joeur se trouve en peripherie du plateau
    #cela le previendra de ne pas aller plus loin, sert a ne pas sortir des limites de celui-ci
    #revoie True si il n'est pas en peripherie gauche False si non
    x,y = find_position(state)
    if x == 0:
        return False 
    else :
        return True

def check_border_behind_player1(state):
    #regarde la position si le joeur se trouve en peripherie du plateau
    #cela le previendra de ne pas aller plus loin, sert a ne pas sortir des limites de celui-ci
    #revoie True si il n'est pas en peripherie False si non
    #sert uniquement au joueur 1 pour ne pas qu'il recule de sa position de depart, cas rare
    x,y = find_position(state)
    if y == 0:
        return False 
    else :
        return True

def check_border_behind_player2(state):
    #regarde la position si le joeur se trouve en peripherie du plateau
    #cela le previendra de ne pas aller plus loin, sert a ne pas sortir des limites de celui-ci
    #revoie True si il n'est pas en peripherie False si non
    #sert uniquement au joueur 2 pour ne pas qu'il recule de sa position de depart, cas rare
    x,y = find_position(state)
    if y == 16:
        return False 
    else :
        return True

def check_box_free(state,box):
    #sert a verifier si la case sur laquelle on veut aller est libre, si il n'y a pas l'autre joeur dessus
    #box est la cordonnée de la nouvelle case
    #return True si la case est libre, False si non
    if find_other_position(state) == box:
        return False
    else:
        return True
    
def check_box_free_up(state):
    #permet de verifier si la case devant le joueur est libre, fonctionne comme les check_wall
    #renvoie True si la case est libre, False si non
    board = state["board"]
    x,y = find_position(state)
    y = y+2
    if check_box_free(state,(x,y)):
        return True
    else:
        return False

def check_box_free_right(state):
    #permet de verifier si la case devant le joueur est libre, fonctionne comme les check_wall
    #renvoie True si la case est libre, False si non
    board = state["board"]
    x,y = find_position(state)
    x = x+2
    if check_box_free(state,(x,y)):
        return True
    else:
        return False

def check_box_free_left(state):
    #permet de verifier si la case devant le joueur est libre, fonctionne comme les check_wall
    #renvoie True si la case est libre, False si non
    board = state["board"]
    x,y = find_position(state)
    x = x-2
    if check_box_free(state,(x,y)):
        return True
    else:
        return False

def check_box_free_down(state):
    #permet de verifier si la case devant le joueur est libre, fonctionne comme les check_wall
    #renvoie True si la case est libre, False si non
    board = state["board"]
    x,y = find_position(state)
    y = y-2
    if check_box_free(state,(x,y)):
        return True
    else:
        return False


def IA(state):
    #retournera une liste avec les nouvelles cordonnées
    global on_right

    if am_i_first_player(state):#joueur 1
        x,y = find_position(state)
        if x == 0:
            on_right = True
            #faire comme pour on right
            if check_wall_up(state) and check_box_free_up(state):
                y = y+2
                return [x,y]
            elif check_wall_right(state) and check_box_free_right(state):
                #move right
                x = x+2
                return [x,y]
            else:
                #giveup
                pass

        elif x == 16:
            on_right == False
            if check_wall_left(state) and check_box_free_left(state):
                #move left
                x = x-2
                return [x,y]
            elif check_wall_down(state) and check_box_free_down(state):
                #move down
                y = y-2
                return [x,y]
            else:
                #giveup
                pass
        
        elif on_right:
            if check_wall_up(state) and check_box_free_up(state):
                #movre up
                y = y+2
                return [x,y]
            elif check_wall_right(state) and check_box_free_right(state):
                #move right
                x = x+2
                return[x,y]
            else:
                #giveup
                pass
        
        elif not on_right:
            if check_wall_left(state) and check_box_free_left(state):
                #move left
                x = x-2
                return [x,y]
            elif check_wall_down(state) and check_box_free_down(state):
                #move down
                y = y-2
                return [x,y]
            else:
                #giveup
                pass

        else:
            #giveup
            pass
    else:#joueur 2
        x,y = find_position(state)
        if x == 0:
            on_right = True
            #faire comme pour on right
            if check_wall_down(state) and check_box_free_down(state):
                #move down
                y = y-2
                return [x,y]
            elif check_wall_right(state) and check_box_free_right(state):
                #move right
                x = x+2
                return [x,y]
            else:
                #giveup
                pass

        elif x == 16:
            on_right == False
            if check_wall_left(state) and check_box_free_left(state):
                #move left
                x = x-2
                return [x,y]
            elif check_wall_up(state) and check_box_free_up(state):
                #move up
                y = y+2
                return [x,y]
            else:
                #giveup
                pass
        
        elif on_right:
            if check_wall_down(state) and check_box_free_down(state):
                #movre down
                y = y-2
                return [x,y]
            elif check_wall_right(state) and check_box_free_right(state):
                #move right
                x = x+2
                return[x,y]
            else:
                #giveup
                pass
        
        elif not on_right:
            if check_wall_left(state) and check_box_free_left(state):
                #move left
                x = x-2
                return [x,y]
            elif check_wall_up(state) and check_box_free_up(state):
                #move up
                y = y+2
                return [x,y]
            else:
                #giveup
                pass

        else:
            #giveup
            pass

       
def send_message(sock, message):
    # Envoie un message JSON au serveur
    json_message = json.dumps(message)
    message_length = len(json_message).to_bytes(4, byteorder='big')  # Utilisez un entête de 4 octets pour la longueur du message
    sock.sendall(message_length)
    sock.sendall(json_message.encode())

    # Reçoit un message JSON du serveur
    message_length = int.from_bytes(sock.recv(4), byteorder='big')  # Reçoit l'entête contenant la longueur du message
    json_message = sock.recv(message_length).decode()
    return json.loads(json_message)
def receive_message(sock):
    # Reçoit un message JSON du serveur
    message_length = int.from_bytes(sock.recv(4), byteorder='big')  # Reçoit l'entête contenant la longueur du message
    json_message = sock.recv(message_length).decode()
    return json.loads(json_message)
def main():
    # Crée une socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Se connecte au serveur
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print("Connecté au serveur.")
        #envoyer l'inscription
        inscription = {}
        inscription["request"] = "subscribe"
        inscription["port"] = SERVER_PORT
        inscription["name"] = "Louis"
        inscription["matricules"] = ["23317", "21187"]
        json_data = json.dumps(inscription)

        send_message(client_socket, json_data)

        while True:

            # Reçoit et affiche la réponse du serveur
            response = receive_message(client_socket)
            if response["response"] == "ok":
                pass
            elif response["request"] == "ping":
                message = {}
                message["response"] = "pong"
                send_message(client_socket,message)
            elif response["request"] == "play":
                state = response["state"]
                move = IA(state)
                move_message = {"type": "move", "position": move}  # Créer le message du mouvement
                send_message(client_socket, move_message)


            print("Réponse du serveur:", response)

    except ConnectionRefusedError:
        print("Connexion refusée. Vérifiez que le serveur est en cours d'exécution.")
    except Exception as e:
        print("Une erreur s'est produite :", e)
    finally:
        # Ferme la connexion
        client_socket.close()

if __name__ == "__main__":
    main()








#inscription
#inscription = {}
#inscription["request"] = "subscribe"
#inscription["port"] = 8888
#inscription["name"] = "Louis"
#inscription["matricules"] = ["23317", "67890"]

#client_socket.sendall(inscription)

#thread_reception = threading.Thread(target=receive_message)
#thread_reception.start()

#while True:
#    received_message = receive_message(client_socket)
#    if received_message["request"] == "ping":
#        response = {}
#        response["response"] = "pong"
#        send_message(client_socket, response)
#    if received_message["request"] == "play":
#        state = received_message["state"]
#        response = {}
#        response["response"] = "move"
#        move = {}
#        move["type"] = "pawn"
#        shot_played = IA(state)
#        move["position"] = shot_played
#        response["move"] = move
#        send_message(client_socket,response)



#à suprimer a la fin, debugage
#state = {}
#state["players"] = ["LOUIS","HSL"]
#state["current"] = 0
#state["blockers"] = [10, 10]
#state["board"] = [[2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 0.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0],[3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 4.0, 5.0, 4.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0],[2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0],[3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0],[2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0],[3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0],[2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0],[3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0],[2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0],[3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0],[2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0],[3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0],[2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0],[3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0],[2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0],[3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 5.0, 3.0],[2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 1.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0]]

#print(what_is_this_box(state,(8,0)))
#print(find_position(state))
#print(check_wall_straight(state))
#print(check_wall_right(state))
#print(check_wall_left(state))
#print(check_border_behind_player1(state))