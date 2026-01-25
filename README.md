# Simulation Biomécanique & Optimisation d'un Soulevé de Terre (Deadlift)


**Ce projet est une simulation physique "from scratch" modélisant la dynamique d'un corps humain soulevant une charge de 175 kg.**

Il ne s'agit d'une application d'ingénierie combinant **mécanique newtonienne**, **résolution numérique matricielle** et **optimisation algorithmique** pour simuler la physique du mouvement et trouver la meilleure forme de soulevé de terre.

## Résultat du projet

https://private-user-images.githubusercontent.com/75246845/519122384-018999d9-b407-4cab-a683-73287ce033ac.mp4?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NjQxNTI3NzEsIm5iZiI6MTc2NDE1MjQ3MSwicGF0aCI6Ii83NTI0Njg0NS81MTkxMjIzODQtMDE4OTk5ZDktYjQwNy00Y2FiLWE2ODMtNzMyODdjZTAzM2FjLm1wND9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTExMjYlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUxMTI2VDEwMjExMVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTkyOWM4MWZlYmZiYmE2M2YyNDg4ZTYxNTM1OGE0MzEzZGFlNTdmMTg3YThmNzdkMTlkMTZhOTJkNzY5MDBkMDAmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.qOp45T6DWmqifnMOJyPolIUkBFRRC4IajxaQmhn-o94

## Objectifs Techniques

* **Modéliser** un corps humain comme un système poly-articulé (pendule à n branches).
* **Simuler** les forces internes (muscles) et externes (gravité, réaction du sol, charge) sans moteur physique préexistant.
* **Optimiser** la commande motrice via une descente de gradient pour réaliser un mouvement complexe (Deadlift) sans perte d'équilibre.

## Architecture du Moteur Physique

Le noyau du moteur repose sur la théorie du **pendule à n branches**. Le corps est modélisé par quatre segments rigides ($L_i$) reliés par des liaisons pivots parfaites ($O_i$).

### 1. Modélisation Dynamique (Matricielle)
Au lieu d'utiliser une librairie externe, les équations du mouvement sont dérivées du **Principe Fondamental de la Dynamique (PFD)** et du **Théorème du Moment Cinétique (TMC)**. Elles sont alors discrétisées avec la méthode d'Euler, ainsi, à chaque pas de temps ($t \approx 1ms$), le système construit et résout une équation matricielle $AX = B$ à $3n$ inconnues :

### 2. Le Modèle de l'Humain
Les muscles sont modélisés comme des actionneurs exerçant une force dépendant de la géométrie de leurs points d'insertion. Le système gère 5 groupes musculaires majeurs :

| Muscle                   | Os Agoniste | Force Max ($F_{max}$) |
|:-------------------------|:------------|:----------------------|
| **Mollets**              | Tibia       | 10 kN                 |
| **Quadriceps**           | Fémur       | 10 kN                 |
| **Ischio-jambiers**      | Fémur/Dos   | 10 kN                 |
| **Lombaires** (Low back) | Dos         | 10 kN                 |
| **Dorsaux** (Lats)       | Bras        | 2 kN                  |

## Algorithme de Contrôle : Le "Cerveau"

Le défi est de maintenir l'équilibre sous une charge de 175 kg. Le module `brain.py` agit comme le système nerveux central.

### Optimisation par Descente de Gradient
L'algorithme cherche à maximiser une fonction de qualité $Q$ définie sur l'espace des efforts musculaires $[0, 1]^5$. La mise à jour des commandes motrices suit la loi :

$$e_{n+1} = e_n + k\gamma^n \nabla Q(e_n)$$

* **Pas d'apprentissage ($k$) :** Ajusté dynamiquement en fonction du pas de temps ($0.001/t$).
* **Facteur de décroissance ($\gamma$) :** $0.7$, pour stabiliser la convergence.
* **Critère d'arrêt :** Convergence locale lorsque $\|e_n-e_{n-1}\|_\infty < 10^{-3}$.

### Fonction de Coût $Q(e)$
La fonction $Q$ évalue la posture à chaque instant pour garantir la réussite du deadlift. Elle favorise la montée des épaules tout en pénalisant fortement le déséquilibre du centre de gravité et les vitesses excessives.

## Visualisation et Analyse

Le projet inclut des outils d'analyse (`plot.py`) pour valider la cohérence physique :
* **Bilan Énergétique :** Vérification de la conservation ($E_m = E_c + E_p \approx \sum W_{muscles}$).
* **Forces Normalisées :** Visualisation de l'activation musculaire au cours du temps.
