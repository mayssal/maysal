# Rapport — Intégration et réglages

## Chaîne bout en bout
- Ingestion: calcul d’empreintes face/voix et insertion DB
- Requête: extraction (frames/audio) -> embeddings -> matching -> affichage

## Réglages
- Seuil minimal (`matching.min_confidence`): 0.30–0.50 selon tolérance aux faux positifs
- Pondérations (`face_weight`, `voice_weight`): adapter selon disponibilité/qualité des canaux
- Échantillonnage vidéo: augmenter `max_frames` si nécessaire (temps de calcul ↑)

## Base de données
- SQLite par défaut (fichier `biomatch.db`)
- PostgreSQL recommandé en production (index, scalabilité)

## Journalisation et audit
- Conserver les appels (date, média, scores) selon vos politiques
- Contrôle d’accès administrateur et chiffrement des secrets

## Tests et validation
- Tests unitaires: similarité/matching
- Évaluer sur un jeu de données interne ou public anonymisé