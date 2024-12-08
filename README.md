# Projet Métro - README

Ce projet présente une interface de visualisation du réseau de métro parisien, accompagnée de calculs de trajets (Dijkstra) et de la génération d’arbres couvrants (Prim, Kruskal). Le back-end est développé en Python avec Flask, tandis que le front-end utilise uniquement HTML/CSS et JavaScript.

## Prérequis

- **Python 3.8+** (ou version plus récente)
- **pip** (habituellement inclus avec Python)
- **Flask** (installé via `pip`)
- Un navigateur web récent (Chrome, Firefox, etc.)

## Installation

1. **Récupérer le projet**  
   Clonez le dépôt ou téléchargez-le en zip, puis décompressez-le.  
   ```bash
   git clone https://votre-repo-git/metromap.git
   cd metromap
   ```

2. **Environnement virtuel (optionnel, mais recommandé)**  
   Créez et activez un environnement virtuel pour isoler les dépendances :  
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Sur Windows : venv\Scripts\activate
   ```

3. **Installation des dépendances Python**  
   Installez Flask (et autres dépendances si nécessaire) :  
   ```bash
   pip install flask
   ```
   
   Si vous disposez d’un fichier `requirements.txt`, utilisez :  
   ```bash
   pip install -r requirements.txt
   ```

## Lancement du Back-End

1. **Démarrage du serveur Flask**  
   Le projet inclut en général un fichier `app.py` ou `server.py`. Par exemple :  
   ```bash
   python app.py
   ```
   
   Par défaut, Flask lancera le serveur sur `http://127.0.0.1:5000` (ou comme indiqué dans la console).

2. **Vérifier le fonctionnement du Back-End**  
   Ouvrez votre navigateur et accédez à l’URL [http://127.0.0.1:5000](http://127.0.0.1:5000). Vous devriez voir un message ou une page de test indiquant que le serveur est opérationnel.  
   De même, les routes spécifiques (par exemple `/dijkstra?s1=...&s2=...`) devraient renvoyer des données JSON.

## Lancement du Front-End

1. **Fichiers statiques**  
   Le front-end est composé des fichiers HTML, CSS et JS. Par exemple, vous pouvez avoir un `index.html` dans un répertoire `frontend/`.

2. **Ouverture dans le navigateur**  
   Vous pouvez simplement ouvrir `index.html` depuis votre explorateur de fichiers dans votre navigateur, ou utiliser un petit serveur statique (optionnel).  
   
   **Optionnel : serveur statique local**  
   Depuis le répertoire contenant `index.html`, lancez :  
   ```bash
   python -m http.server 8080
   ```  
   Puis ouvrez [http://127.0.0.1:8080](http://127.0.0.1:8080) dans votre navigateur.
   
   **Sinon**, un double-clic sur `index.html` devrait suffire, mais certaines fonctionnalités (comme des requêtes fetch) peuvent nécessiter un serveur local pour fonctionner correctement.

## Interaction Front-End / Back-End

- L’application front-end va envoyer des requêtes (via `fetch()`) au serveur Flask.
- Assurez-vous que l’URL du back-end dans le code front-end est correcte (par exemple `http://127.0.0.1:5000`).
- Lorsque vous sélectionnez deux stations et lancez un calcul d’itinéraire, le front-end va faire une requête AJAX vers le back-end (une route `/dijkstra`) et mettre à jour l’affichage une fois les données reçues.

## Dépannage

- **Problème : Pas de réponse du serveur Flask ?**  
  Vérifiez que le serveur est bien lancé, et que vous utilisez la bonne URL/port.
  
- **Problème : Les données ne s’affichent pas ?**  
  Ouvrez la console du navigateur (F12, onglet Console) pour voir les éventuelles erreurs. Vérifiez également la console où Flask est lancé pour d’éventuels messages d’erreur.

- **Problème : Pas d’installation Python/Flask ?**  
  Assurez-vous d’avoir installé Python 3 et d’avoir ajouté Python et pip à votre PATH. Sur Windows, l’installateur officiel Python propose cette option.

## Conclusion

Une fois tous ces points vérifiés, vous devriez pouvoir :

1. Lancer le serveur Flask.
2. Ouvrir la page front-end.
3. Interagir avec la carte, visualiser l’itinéraire entre deux stations, et voir les résultats renvoyés par le back-end sur la page.