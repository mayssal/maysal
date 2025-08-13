# BioMatch: Reconnaissance faciale et vocale (Image/Video -> Base de données)

BioMatch est un programme Python professionnel qui identifie une personne à partir d’une image ou d’une vidéo en utilisant la reconnaissance faciale et/ou vocale, puis affiche les données associées depuis votre base de données. Il est conçu pour être clair, robuste, extensible et exploitable par un administrateur.

- Entrée: image (.jpg, .png, …) ou vidéo (.mp4, .avi, …)
- Sortie: fiche de la personne correspondante (nom, email, téléphone, adresse, notes, …) récupérée depuis la base
- Robustesse: prétraitements d’images, extraction multi-images, embedding deep learning, fusion des scores face/voix
- Modulaire: modules séparés (face, voice, matching, DB, CLI, utils)
- Docs fournies: cahier des charges, architecture (diagrammes mermaid), rapports par module, note d’intégration FTK


## 1) Prérequis

- Windows 10/11 64-bit
- Visual Studio Code (VSCode) avec l’extension Python
- Python 3.10+ 64-bit (recommandé via Anaconda/Miniconda)
- ffmpeg installé et présent dans le PATH (pour l’audio/vidéo)
  - via Chocolatey: `choco install ffmpeg` (PowerShell admin)
  - ou télécharger depuis `https://ffmpeg.org/` et ajouter le dossier `bin` au PATH


## 2) Installation (Windows + VSCode)

1. Ouvrir le dossier du projet dans VSCode.
2. Créer un environnement Python (recommandé conda):
   - PowerShell/Terminal VSCode:
     - `conda create -n biomatch python=3.11 -y`
     - `conda activate biomatch`
3. Installer les dépendances:
   - `pip install --upgrade pip`
   - `pip install -r requirements.txt`
4. Copier `.env.example` en `.env` et adapter la variable `DATABASE_URL` à votre base (SQLite par défaut):
   - Exemple: `DATABASE_URL=sqlite:///./biomatch.db`
5. Initialiser le schéma si vous utilisez SQLite local:
   - `python -m app.db.db_client --init-db`


## 3) Configuration

- `config.yaml` contient les paramètres: seuils de similarité, pondération face/voix, échantillonnage vidéo.
- Variables d’environnement (`.env`): `DATABASE_URL`, éventuellement d’autres secrets (PostgreSQL, etc.).


## 4) Ingestion de personnes dans la base

Pour ajouter une personne (avec image/vidéo pour empreintes biométriques):

```bash
conda activate biomatch
python scripts/ingest_person.py \
  --name "Jean Dupont" \
  --email "jean.dupont@example.com" \
  --phone "+33 6 12 34 56 78" \
  --address "10 rue de la Paix, Paris" \
  --notes "Employé - badge 123" \
  --image "C:/chemin/vers/photo.jpg" \
  --video "C:/chemin/vers/video.mp4"
```

- Vous pouvez fournir uniquement `--image` ou uniquement `--video`, ou les deux. Si `--video` est fourni, les algorithmes extraient des frames (visage) et l’audio (voix) pour enrichir la fiche.


## 5) Reconnaissance (recherche d’un match)

```bash
conda activate biomatch
python -m app.main --input "C:/chemin/vers/probe.mp4" --use-face --use-voice
```

Options utiles:
- `--media-type {auto,image,video}`: force le type du média
- `--use-face / --use-voice`: activer/désactiver un canal
- `--topk 5`: afficher les 5 meilleurs scores
- `--min-confidence 0.35`: seuil minimal affiché

La sortie affiche la meilleure correspondance et les données associées. Si aucun score n’est jugé suffisant, un message « aucun match fiable » est renvoyé.


## 6) Intégration FTK (Forensic Toolkit)

Voir `docs/forensic_ftk_integration.md` pour:
- Export des preuves (images/vidéos) depuis FTK
- Automatisation d’extraction d’images/audio
- Chargement des résultats dans BioMatch pour identification


## 7) Diagrammes, cahier des charges, rapports

- `docs/cahier_des_charges.md`: besoins, contraintes, risques, livrables
- `docs/architecture.md`: diagrammes mermaid (composants, séquences), flux de données
- `docs/rapport_face.md`, `docs/rapport_voice.md`, `docs/rapport_integration.md`: explications détaillées, seuils, tuning


## 8) Limitations et considérations éthiques/légales

- Respecter les lois locales (RGPD, consentement, finalité, minimisation des données)
- Éviter les usages non autorisés et documenter la base de références (provenance, consentement)
- Les performances dépendent de la qualité du média; des prétraitements et des paramètres sont proposés pour les cas dégradés.


## 9) Structure du projet

```
biomatch/
  app/
    db/
    recognition/
    ui/
  docs/
  scripts/
  tests/
```


## 10) Dépannage rapide

- Erreur d’import de `torch`/`facenet_pytorch`/`resemblyzer`: vérifier l’environnement conda et réinstaller `pip install -r requirements.txt`
- ffmpeg introuvable: installer ffmpeg et ajouter au PATH, puis redémarrer le terminal
- Aucun match trouvé: ajuster `config.yaml` (seuils, pondérations), vérifier la présence d’empreintes face/voix en base


Bon usage et n’hésitez pas à adapter les modules et paramètres à votre contexte métier.