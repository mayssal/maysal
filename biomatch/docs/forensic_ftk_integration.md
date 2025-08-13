# Intégration FTK (Forensic Toolkit)

Ce document décrit comment intégrer BioMatch dans un flux d’investigation avec FTK.

## Exports depuis FTK
- Extraire les médias pertinents (photos, vidéos) vers un dossier de travail
- Lorsque possible, exporter aussi des images clés (keyframes) et segments audio

## Pré-traitements
- Si nécessaire, convertir/normaliser les vidéos (container mp4, codec h264) et l’audio (WAV 16 kHz PCM)
- Contrôler les métadonnées (horodatage, source) pour la traçabilité

## Ingestion dans BioMatch
- Pour enrichir la base de référence: `scripts/ingest_person.py --name ... --image ... --video ...`
- Les empreintes faciales et/ou vocales sont calculées et stockées en base

## Requête / Identification
- Fournir un média extrait de FTK à `app.main`: `python -m app.main --input chemin\vers\media --use-face --use-voice`
- BioMatch renvoie les meilleurs candidats avec leur fiche

## Bonnes pratiques forensiques
- Préserver l’intégrité: travailler sur des copies, conserver les hachages
- Chaîne de conservation: documenter toutes les opérations (export, conversion, identification)
- Répétabilité: conserver versions des outils, paramètres et modèles

BioMatch n’agit pas comme un outil forensique certifié mais peut s’intégrer au processus d’analyse pour l’étape d’identification biométrique. Assurez-vous de respecter vos procédures légales et internes.