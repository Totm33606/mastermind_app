# 🧠 Mastermind et Algorithme Génétique 🎮

Bienvenue dans le dépôt Git du jeu **Mastermind**, un projet captivant où le jeu Mastermind est résolu à l'aide d'un algorithme génétique.

---

## 📖 Description

Mastermind est un jeu classique où le joueur doit deviner une combinaison secrète de couleurs en un nombre limité de tentatives.  
Dans ce dépôt, nous proposons deux implémentations différentes du jeu Mastermind avec deux librairies différentes : 

- `PyGame`  
- `Tkinter`  

Dans ces deux versions, le jeu est résolu par un **algorithme génétique**, qui s'inspire des principes de l'évolution naturelle pour trouver les meilleures solutions.

### Fonctionnalités
- 🕹 **Deux versions du jeu Mastermind** : Découvrez et comparez les deux versions.
- 🤖 **Résolution par algorithme génétique** : Des stratégies d'optimisation puissantes et innovantes.
- ⚡ **Simulation rapide** : Génération, sélection, mutation et crossover pour une bonne efficacité.
- 🔧 **Personnalisation** : Ajustez les paramètres pour expérimenter avec l'algorithme.

---

## 🛠 Installation

### Pré-requis
Vous aurez besoin d'Anaconda pour les étapes qui suivront. Vous pouvez le télécharger
dés à présent [ici](https://www.anaconda.com/products/distribution).

### Étapes d'installation
Nous vous proposons de passer par un environnement virtuel, avec Anaconda.
Commencez par cloner le dépôt distant puis suivez les étapes ci-dessous :
```bash
git clone https://github.com/Totm33606/mastermind_app.git
cd mastermind_app
conda create --name env_mastermind python=3.8 # Création de l'environnement
conda activate env_mastermind # Activation de l'environnement
pip install -r requirements.txt # Installation des dépendances
```
Une fois cela fait, vous êtes désormais prêts à jouer ! 

### Lancer une partie
Pour la version `PyGame` :
```bash
python mastermindv1_pygame.py
```

### Versions utilisées pour le développement
- `Python 3.12.3`
- `PyGame 2.6.1`
- `Tkinter 8.6`

---

## ✨ Auteurs et Contacts

Cette application a été développée dans le cadre d'un projet, par des étudiants ingénieurs,
et encadrée par des membres de **ANITI** et de **La Compagnie du Code**.

Développeurs :
- Thomas Chambon : t_chambo@insa-toulouse.fr
- Adam Medbouhi : medbouhi@insa-toulouse.fr

Encadrants : 
- Marjorie Allain-Moulet : marjorie.allain-moulet@cs-soprasteria.com
- Nicolas Decoster : nicolas.decoster@mailbox.org