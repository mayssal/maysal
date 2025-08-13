# Cahier des charges — BioMatch

## Contexte et objectif
Identifier une personne à partir d’un média (image/vidéo), en croisant la reconnaissance faciale et vocale, puis afficher les données de référence associées en base. L’application est destinée à un administrateur habilité.

## Périmètre
- Entrée: image (portrait) ou vidéo (avec visage et/ou voix)
- Sortie: fiche de la personne identifiée (nom, contacts, notes, etc.)
- Base: table `persons` (schéma minimal fourni), adaptable à une base existante
- Canaux biométriques: visage et voix, pondérés et optionnels

## Exigences fonctionnelles (EF)
- EF1: Ingestion de personnes (image/vidéo) et génération d’empreintes (face/voice)
- EF2: Recherche top-K des correspondances par similarité cosinus
- EF3: Fusion des scores face/voix avec pondération configurable
- EF4: Seuil de confiance minimal configurable
- EF5: Affichage CLI des résultats et détails top-1
- EF6: Journalisation minimale et messages d’erreur clairs

## Exigences techniques (ET)
- ET1: Python 3.10+
- ET2: Modèles pré-entraînés standards (facenet-pytorch, resemblyzer)
- ET3: Gestion vidéo/audio (OpenCV + moviepy/ffmpeg)
- ET4: Stockage embeddings en DB (SQLite par défaut), extensible PostgreSQL
- ET5: Configurable via `config.yaml` et `.env`

## Performance et robustesse
- PR1: Extraction multi-frames pour compenser les images dégradées
- PR2: Prétraitement (amélioration contraste, débruitage léger)
- PR3: Seuils/pondérations ajustables par contexte

## Qualité et sécurité
- Q1: Modularité du code, tests unitaires ciblés (similarité)
- Q2: Respect des lois (RGPD, consentement, finalité)
- Q3: Aucune réidentification non autorisée; traçabilité des données source

## Livrables
- Code source complet (modules, scripts)
- Documentation: architecture, rapports par module, note FTK
- Fichiers de configuration; schéma DB

## Planning indicatif
- Semaine 1: cadrage, architecture, prototype face
- Semaine 2: canal voix + fusion
- Semaine 3: intégration DB, ingestion, CLI
- Semaine 4: documentation, optimisation, durcissement

## Risques
- Données de mauvaise qualité (atténues via prétraitement et multi-frames)
- Dépendances lourdes (CUDA non obligatoire; CPU supporté)
- Contraintes légales: à cadrer avec la conformité et la DPO