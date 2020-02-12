# Git et GitHub : utilisation de base
1. Avoir un compte git

2. Pour placer le repo dans le dossier que vous souhaitez, il faut d'abord se déplacer là où vous voulez. Exemple : "cd C:/user/Documents"

3. En ligne de commande, taper : "git clone https://github.com/CTomm/ECORCE.git". Et voilà vous avez les fichiers !

4. Quand vous avez fait des modifs : 
    * En ligne de commande, aller dans le dossier où vous avez cloné le repo. Exemple : "cd C:/user/Documents/ProjetLeaflet"
    * Taper "git add MonFicher.js"
    *  Taper "git commit -m "Description rapide de mes modifs"
    * Taper "git push" -> c'est là où ça part vraiment sur github
    *  Entrer ses identifiants GitHub

5. Quand quelqu'un d'autre a fait des modifs :
    * En ligne de commande, aller dans le dossier où vous avez cloné le repo. Exemple : "cd C:/user/Documents/ProjetLeaflet"
    * Taper "git pull"

6. À tout moment, on peut taper "git status" pour connaitre l'état de notre répertoire local par rapport au repo en ligne
