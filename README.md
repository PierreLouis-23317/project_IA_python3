projet bac 2 ECAM GE
23317
21187


RunnerIA
Description

Notre IA consiste en une sorte de Runner. Nous pouvons visualiser cela comme un plateau 9x9 avec le bas comme la position de départ du joueur 1 et le haut comme la position de départ du joueur 2. Le pion se déplace en ligne droite jusqu'à rencontrer un obstacle. Lorsqu'il rencontre un obstacle, il se déplace sur la droite et continue en ligne droite. Si le pion se trouve à l'extrémité droite de la grille, l'IA active un mode spécial qui le ramène vers la gauche. Dans ce mode, ses seuls mouvements sont d'aller tout droit par rapport à son arrivée ou d'aller à gauche. Une fois revenu à gauche, l'IA reprend sa stratégie initiale. Ainsi, comme nous pouvons le constater, l'IA est 100% prédictible.
Bibliothèques utilisées

    socket :
        Rôle dans le code : La bibliothèque socket est utilisée pour créer et gérer des connexions réseau. Dans le code, nous créons une socket TCP pour communiquer avec le serveur.
          Exemple d'utilisation : socket.socket() pour créer une nouvelle socket, socket.connect() pour établir une connexion avec le serveur.
    threading :
        Rôle dans le code : La bibliothèque threading est utilisée pour gérer les communications réseau dans un thread séparé, afin de ne pas bloquer l'exécution du programme principal.
          Exemple d'utilisation : Nous avons créé un thread pour gérer les communications avec le serveur. Cela permet à notre programme de continuer à fonctionner pendant que les opérations de communication sont en cours.
    json :
        Rôle dans le code : La bibliothèque json est utilisée pour sérialiser et désérialiser les données au format JSON. Dans notre code, on utilise json.dumps() pour convertir les objets Python en chaînes JSON et json.loads() pour convertir les chaînes JSON en objets Python.
          Exemple d'utilisation : nous utilisons json.dumps() pour convertir les messages à envoyer au serveur en format JSON, et json.loads() pour décoder les messages JSON reçus du serveur.
